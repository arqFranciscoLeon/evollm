import argparse
import re
from collections import defaultdict

import axelrod as axl
import pandas as pd

from evollm import algorithms
from evollm import common


def parse_arguments() -> argparse.Namespace:
  """Parse command line arguments."""

  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
      "--algo",
      type=str,
      required=True,
      help="Name of the python module to call the LLM algorithms")

  return parser.parse_args()


def rank_strategies(args: argparse.Namespace):
  classes = [axl.Cooperator,
          axl.Defector,
          axl.Random,
          axl.TitForTat,
          axl.Grudger,
          axl.CyclerDDC,
          axl.CyclerCCD,
          axl.GoByMajority,
          axl.SuspiciousTitForTat,
          axl.Prober,
          # axl.OriginalGradual,
          axl.WinStayLoseShift,
          ]

  players = [c() for c in classes]
  algo_results: dict[str, dict] = defaultdict(dict)
  ranks = defaultdict(list)

  algos = algorithms.load_algorithms(args.algo)
  max_n = max(a.n for a in algos)

  for n in range(1, max_n + 1):
    for a in algorithms.create_classes(algos, suffix=f"_{n}"):
      strategy = a()
      print(strategy.strategies)
      tournament = axl.Tournament(players + [strategy],
                                  turns=algos[0].rounds,
                                  repetitions=3,
                                  noise=algos[0].noise,
                                  seed=1,
                                  game=common.get_game(algos[0].game))
      results = tournament.play(processes=None)
      algo_results[strategy.name][n] = results.scores[-1][0]
  for k, v in algo_results.items():
    sorted_s = pd.Series(v).sort_values(ascending=False)
    print(k, sorted_s, sep="\n")
    for n in range(max_n):
      ranks[k].append(f"{k}_{sorted_s.index[n]}")

  write_ranks(f"{args.algo}.py", ranks)


def write_ranks(path: str, ranks: dict[str, list[str]]):
  """Write the ranks lists into the strategy module, idempotently.

  Any existing *_ranks definitions are removed first, so re-running the
  ranking replaces them instead of appending duplicates.
  """
  with open(path, encoding="utf8") as f:
    source = f.read()

  source = re.sub(
      r"\n*^(?:Aggressive|Cooperative|Neutral)_ranks\s*=\s*\[[^\]]*\]\n?",
      "", source, flags=re.M).rstrip("\n") + "\n"

  with open(path, "w", encoding="utf8") as f:
    f.write(source)
    for k in ranks:
      f.write(f"\n\n{k}_ranks = [\n")
      for r in ranks[k]:
        f.write(f"'{r}',\n")
      f.write("]")
    f.write("\n")


if __name__ == "__main__":
  parsed_args = parse_arguments()

  rank_strategies(parsed_args)
