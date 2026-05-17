import argparse
import ast
import logging
import os
import textwrap
from io import TextIOWrapper

import axelrod as axl

from evollm import algorithms, common, llm_clients, prompts
from evollm.common import Attitude
from evollm.llm_clients import LLMClient

# Configure logging — INFO+ to file, WARNING+ also to console
_log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_file_handler = logging.FileHandler("create_strategies.log", mode="w", encoding="utf8")
_file_handler.setFormatter(_log_formatter)
_console_handler = logging.StreamHandler()
_console_handler.setFormatter(_log_formatter)
_console_handler.setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, handlers=[_file_handler, _console_handler])
logger = logging.getLogger(__name__)

logging.getLogger("openai._base_client").setLevel(logging.WARN)
logging.getLogger("httpx").setLevel(logging.WARN)


def generate_strategies(client: LLMClient, attitude: Attitude, temp: float,
                        game: axl.Game, rounds: int, noise: float,
                        refine: bool = False,
                        prose: bool = False) -> tuple[str, str]:

  messages = []

  game_information = prompts.create_game_information(game, rounds, noise)

  if prose:
    system, prompt, actions = prompts.create_first_prose_prompt(attitude, noise)

    messages += [{"role": "user", "content": prompt}]
    logger.info("Prompt:\n:%s", prompt)
    print(f"    [1/5] Generando descripción inicial ({attitude})...")
    response = get_response(client, system, messages, temp)
    logger.info("Response:\n:%s", response)

    initial_strategy = response

    messages += [{"role": "assistant", "content": response}]

    prompt = prompts.create_second_prose_prompt(actions, game_information)
  else:
    initial_strategy = ""
    system, prompt = prompts.create_default_prompt(attitude, game_information)

  messages += [{"role": "user", "content": prompt}]
  logger.info("Prompt:\n:%s", prompt)
  print(f"    [2/5] Generando estrategia ({attitude})...")
  response = get_response(client, system, messages, temp)
  logger.info("Response:\n:%s", response)

  if refine:
    messages += [{"role": "assistant", "content": response}]
    prompt = prompts.create_first_refine_prompt()

    messages += [{"role": "user", "content": prompt}]
    logger.info("Prompt:\n:%s", prompt)
    print(f"    [3/5] Refinando — crítica ({attitude})...")
    response = get_response(client, system, messages, temp / 2)
    logger.info("Response:\n:%s", response)

    messages += [{"role": "assistant", "content": response}]
    prompt = prompts.create_second_refine_prompt()

    messages += [{"role": "user", "content": prompt}]
    logger.info("Prompt:\n:%s", prompt)
    print(f"    [4/5] Refinando — reescritura ({attitude})...")
    response = get_response(client, system, messages, 0)
    logger.info("Response:\n:%s", response)

  return initial_strategy, response


def test_algorithm(algorithm: str):

  def is_safe_ast(node):
    """Check if the AST node is considered safe."""
    # yapf: disable
    allowed_nodes = (
        ast.Return, ast.UnaryOp, ast.BoolOp, ast.BinOp, ast.FunctionDef,
        ast.If, ast.IfExp, ast.And, ast.Or, ast.Not, ast.Eq, ast.Try, ast.ExceptHandler, ast.Raise, ast.Del, ast.Delete,
        ast.Compare, ast.USub, ast.In, ast.NotIn, ast.Is, ast.IsNot, ast.For, ast.Pass, ast.Break,
        ast.List, ast.Dict, ast.Tuple, ast.Constant, ast.Set,
        ast.arg, ast.Name, ast.arguments, ast.keyword, ast.Expr, ast.Attribute,
        ast.Call, ast.Store, ast.Slice, ast.Subscript, ast.Load,
        ast.GeneratorExp, ast.comprehension, ast.ListComp, ast.Lambda,
        ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Pow, ast.Mod,
    )
    # yapf: enable

    if not isinstance(node, allowed_nodes):
      raise ValueError(
          f"Unsafe node type: {type(node).__name__}\nnode:\n{ast.unparse(node)}"
      )
    for child in ast.iter_child_nodes(node):
      if not is_safe_ast(child):
        raise ValueError(
            f"Unsafe node type: {type(child).__name__}\nnode:\n{ast.unparse(child)}"
        )
    return True

  try:
    tree = ast.parse(algorithm)
    # Check if the tree has exactly one child
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
      raise ValueError(
          "Algorithm contains more than just a single function definition")

    for node in ast.iter_child_nodes(tree.body[0]):
      is_safe_ast(node)
  except AttributeError as e:
    print(f"AttributeError: {str(e)}")
    raise ValueError(
        f"Algorithm contains potentially unsafe constructs:\n{algorithm}"
    ) from e
  except ValueError as e:
    print(f"ValueError: {str(e)}")
    raise ValueError(
        f"Algorithm contains potentially unsafe constructs:\n{algorithm}"
    ) from e
  except SyntaxError as e:
    print(f"SyntaxError: {str(e)}")
    raise ValueError(f"Algorithm has syntax errors:\n{algorithm}") from e


def strip_code_markers(s):
  s = s.replace("```python", "")
  s = s.replace("```", "")
  return s.strip()


def fix_common_mistakes(s):
  s = s.replace("axl.D", "axl.Action.D")
  s = s.replace("axl.C", "axl.Action.C")
  s = s.replace("Action.DEFECT", "Action.D")
  s = s.replace("Action.COOPERATE", "Action.C")
  s = s.replace("history.count(axl.Action.D)", "history.defections")
  s = s.replace("history.count(axl.Action.C)", "history.cooperations")
  s = s.replace("history.defections()", "history.defections")
  s = s.replace("history.cooperations()", "history.cooperations")
  s = s.replace("_random.rand()", "_random.random()")
  s = s.replace("_random.integers", "_random.randint")
  s = s.replace("match_length", "match_attributes['length']")
  s = s.replace(
      "self.total_scores(self.history, opponent.history)\n",
      "self.score, opponent.score\n",
  )
  return s


def sanitize_unicode_operators(s: str) -> str:
  s = s.replace("\u2192", "->")   # →
  s = s.replace("\u2265", ">=")   # ≥
  s = s.replace("\u2264", "<=")   # ≤
  s = s.replace("\u2260", "!=")   # ≠
  s = s.replace("\u00d7", "*")    # ×
  s = s.replace("\u00f7", "/")    # ÷
  return s


def add_indent(text: str) -> str:
  return "\n".join("  " + line for line in text.splitlines())


def generate_algorithm(client: LLMClient, strategy: str, game: axl.Game,
                       rounds: int, noise: float, refine: bool = False) -> str:

  system = (
      "You are an AI assistant with expertise in game theory and programming. "
      "Your task is to implement the strategy description provided by the user as an algorithm."
  )
  prompt = prompts.create_algorithm_prompt(strategy, game, rounds, noise)

  messages = [{"role": "user", "content": prompt}]
  logger.info("Prompt:\n:%s", prompt)
  print(f"    [5/5] Generando algoritmo Python...")
  response = get_response(client, system, messages, 0)
  logger.info("Response:\n:%s", response)

  if refine:
    messages += [{"role": "assistant", "content": response}]
    prompt = (
        "Please assess whether this implementation is correct and faithful to "
        "the strategy description. Detail any improvements or corrections."
    )

    messages += [{"role": "user", "content": prompt}]
    logger.info("Prompt:\n:%s", prompt)
    response = get_response(client, system, messages, 0)
    logger.info("Response:\n:%s", response)

    messages += [{"role": "assistant", "content": response}]
    prompt = (
        "Now, rewrite the algorithm taking into account the feedback. "
        "Only include python code in your response."
    )

    messages += [{"role": "user", "content": prompt}]
    logger.info("Prompt:\n:%s", prompt)
    response = get_response(client, system, messages, 0)
    logger.info("Response:\n:%s", response)

  algorithm = strip_code_markers(response)
  algorithm = fix_common_mistakes(algorithm)
  algorithm = sanitize_unicode_operators(algorithm)
  test_algorithm(algorithm)
  algorithm = add_indent(algorithm)
  return algorithm


def format_comment(text, width=78):
  wrapped = textwrap.wrap(text, width=width)
  return "\n".join("# " + line for line in wrapped)


def write_class(initial_description: str, description: str, attitude: Attitude,
                n: int, game: axl.Game, rounds: int, noise: float,
                algorithm: str) -> str:
  return f"""{format_comment(initial_description)}

{format_comment(description)}

class {attitude}_{n}(LLM_Strategy):
  n = {n}
  attitude = Attitude.{str(attitude).upper()}
  game = '{game.name}'
  rounds = {rounds}
  noise = {noise}

  @auto_update_score
{algorithm}"""


def generate_class(text_file: TextIOWrapper, strategy_client: LLMClient,
                   algorithm_client: LLMClient, attitude: Attitude, n: int,
                   temp: float, game: axl.Game, rounds: int, noise: float,
                   refine: bool = False, prose: bool = False,
                   max_retries: int = 3):
  last_error: Exception | None = None
  for attempt in range(1, max_retries + 1):
    try:
      initial_strategy, strategy = generate_strategies(
          strategy_client, attitude, temp, game, rounds, noise,
          refine=refine, prose=prose)
      algorithm = generate_algorithm(algorithm_client, strategy, game, rounds,
                                     noise, refine=False)
      text_file.write(
          "\n\n" + write_class(initial_strategy, strategy, attitude, n, game,
                               rounds, noise, algorithm))
      return
    except (ValueError, RuntimeError) as e:
      last_error = e
      print(f"  Intento {attempt}/{max_retries} fallido para {attitude}_{n}: {e!s:.120}")
      logger.warning("Attempt %d/%d failed for %s_%d: %s", attempt, max_retries, attitude, n, e)
  raise ValueError(
      f"No se pudo generar {attitude}_{n} tras {max_retries} intentos"
  ) from last_error


def get_response(client: LLMClient, system: str,
                 messages: list[dict[str, str]], temp: float) -> str:
  return llm_clients.get_response(client, system, messages, temp)


def parse_arguments() -> argparse.Namespace:
  """Parse command line arguments."""

  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
      "--strategy_llm",
      type=str,
      required=True,
      choices=["openai", "anthropic", "google", "openrouter"],
      help=(
          "Which LLM provider to use for strategy generation "
          "('openrouter' = Chinese frontier models via the "
          "OpenAI-compatible gateway)"))
  parser.add_argument(
      "--model",
      type=str,
      default=None,
      help=(
          "Specific model override (e.g. gpt-4o, o4-mini, claude-sonnet-4-5, "
          "claude-opus-4-0, gemini-2.0-flash). "
          "If omitted, the provider default is used."
      ))
  parser.add_argument(
      "--converter_model",
      type=str,
      default=llm_clients.FIXED_CONVERTER_MODEL,
      help=(
          "Registry key of the FIXED model used to convert every model's "
          "natural-language strategy into Python (decoupled from generation). "
          f"Pre-registered default: '{llm_clients.FIXED_CONVERTER_MODEL}'. "
          "Override only for the pre-registered robustness re-conversion check."
      ))
  parser.add_argument(
      "--n",
      type=int,
      required=True,
      help="Number of strategies of each attitude to create")
  parser.add_argument(
      "--temp",
      type=common.temp_arg,
      default=0.7,
      help="Temperature of the LLM")
  parser.add_argument(
      "--game",
      type=str,
      default="classic",
      help="Name of the game to play")
  parser.add_argument(
      "--rounds", type=int, default=1000, help="Number of rounds in a match")
  parser.add_argument(
      "--noise",
      type=common.noise_arg,
      default=0,
      help="Probability that an action is flipped")
  parser.add_argument(
      "--resume", action="store_true", help="If generation crashed, continue")
  parser.add_argument(
      "--algo",
      type=str,
      required=True,
      help="Name of the python module to save the LLM strategies")
  parser.add_argument(
      "--refine",
      action="store_true",
      help="Whether to ask the LLM to critique and rewrite its strategy.")
  parser.add_argument(
      "--prose",
      action="store_true",
      help="Whether to obfuscate that the strategy is for IPD.")

  return parser.parse_args()


def create_strategies(args: argparse.Namespace):
  llm_clients.load_api_keys()

  model_key = llm_clients.resolve_model(args.strategy_llm, args.model)
  strategy_client = llm_clients.make_client(model_key)

  # Conversion (NL → Python) is held constant across all generators so that
  # provider identity is not confounded with coding ability — see
  # PHASE2_PREREG.md §2 (Option A). Reuse the strategy client only when the
  # generator already *is* the fixed converter.
  if args.converter_model == model_key:
    algorithm_client = strategy_client
  else:
    algorithm_client = llm_clients.make_client(args.converter_model)

  print(
      f"  Generación: {model_key}  |  Conversión (fija): "
      f"{args.converter_model}")
  logger.info(
      "Strategy generation model: %s | Fixed conversion model: %s",
      model_key, args.converter_model)

  if args.resume:
    algos = algorithms.load_algorithms(args.algo)
    done_classes = set([(c.attitude, c.n) for c in algos])
  else:
    if os.path.exists(f"{args.algo}.py"):
      assert False, (
          f"{args.algo}.py exists and will be overwritten, "
          "delete or rename the file")

    done_classes = set([])

    with open(f"{args.algo}.py", "w", encoding="utf8") as f:
      f.write("""import axelrod as axl

from evollm.common import Attitude, auto_update_score, LLM_Strategy""")

  strategies_to_create: list[tuple[Attitude, int]] = [
      (a, n)
      for n in range(1, 1 + args.n)
      for a in Attitude
      if (a, n) not in done_classes
  ]
  game = common.get_game(args.game)

  with open(f"{args.algo}.py", "a", encoding="utf8") as f:
    for a, n in strategies_to_create:
      print(f"Generando estrategia {a} {n}/{args.n}...")
      generate_class(f, strategy_client, algorithm_client, a, n, args.temp,
                     game, args.rounds, args.noise, args.refine, args.prose)


if __name__ == "__main__":
  parsed_args = parse_arguments()
  create_strategies(parsed_args)
