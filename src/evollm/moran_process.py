import argparse
from multiprocessing import Pool

import axelrod as axl
import matplotlib.pyplot as plt  # noqa: F401 — pyplot import configures the backend
import numpy as np

from evollm import common
from evollm import algorithms


def parse_arguments() -> argparse.Namespace:
  """Parse command line arguments."""
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
      "--algo",
      type=str,
      required=True,
      help="Name of the python module with the LLM algorithms")
  parser.add_argument(
      "--initial_pop",
      nargs=3,
      type=int,
      required=True,
      help="Initial Number of aggressive, cooperative and neutral players")
  parser.add_argument(
      "--iterations",
      type=int,
      default=100,
      help="Number of times to run the simulation")
  parser.add_argument(
      "--keep_top",
      type=common.temp_arg,
      default=0,
      help="Use algorithms from this top percentile (0 is best performing)")
  parser.add_argument(
      "--keep_bottom",
      type=common.temp_arg,
      default=1,
      help="Use algorithms up to this bottom percentile (1 is worst performing)")
  parser.add_argument(
      "--processes",
      type=common.positive_int,
      default=1,
      help="Number of processes to run simultaneously")
  parser.add_argument(
      "--plot",
      action="store_true",
      help="Plot an example trajectory instead")

  return parser.parse_args()


def build_moran_process(players, reference_algo, seed: int) -> axl.MoranProcess:
  return axl.MoranProcess(
      players,
      seed=seed,
      turns=reference_algo.rounds,
      noise=reference_algo.noise,
      game=common.get_game(reference_algo.game))


def run_moran_process(seed: int, players, reference_algo) -> str:
  """Run one Moran process to fixation and return the winning strategy name.

  N.B. run_hetzner.py parses the per-iteration line printed here; keep the
  stdout format stable.
  """
  mp = build_moran_process(players, reference_algo, seed)
  mp.play()
  print(mp.winning_strategy_name, len(mp))
  return mp.winning_strategy_name


class _Runner:
  """Picklable adapter so Pool.map can carry the players along.

  WARNING: --processes > 1 relies on the 'fork' start method: the strategy
  classes are created dynamically and cannot be pickled under 'spawn'
  (the default on Windows/macOS and Python 3.14+ Linux). For robust
  parallelism, prefer running several --processes 1 invocations as separate
  subprocesses, as run_hetzner.py does.
  """

  def __init__(self, players, reference_algo):
    self.players = players
    self.reference_algo = reference_algo

  def __call__(self, seed: int) -> str:
    return run_moran_process(seed, self.players, self.reference_algo)


def plot_example_trajectory(players, reference_algo):
  mp = build_moran_process(players, reference_algo, seed=1)
  mp.play()
  ax = mp.populations_plot()

  fig = ax.get_figure()
  fig.set_size_inches(3, 2)

  ax.set_title('Population by iteration', fontsize=8)
  ax.set_xlabel(ax.get_xlabel(), fontsize=8)
  ax.set_ylabel(ax.get_ylabel(), fontsize=8)
  ax.legend(labels=['Aggressive', 'Cooperative', 'Neutral'],
            loc='lower center', fontsize=8)
  ax.set_ylim(0, 12)
  ax.set_yticks(np.arange(0, 12 + 1, 4))

  fig.savefig("results/example_moran.png", dpi=500, bbox_inches='tight')


def main():
  parsed_args = parse_arguments()

  # N.B. create separate instances for each player, not copies!
  algos = algorithms.load_algorithms(
      parsed_args.algo, parsed_args.keep_top, parsed_args.keep_bottom)
  classes = algorithms.create_classes(algos)
  players = [cls() for cls, count in zip(classes, parsed_args.initial_pop)
             for _ in range(count)]
  print(players)

  if parsed_args.plot:
    plot_example_trajectory(players, algos[0])
    return

  seeds = np.random.randint(0, 2**31 - 1, size=parsed_args.iterations)
  runner = _Runner(players, algos[0])

  if parsed_args.processes > 1:
    with Pool(processes=parsed_args.processes) as pool:
      results = pool.map(runner, seeds)
  else:
    results = [runner(seed) for seed in seeds]

  winner_counts = {}
  for winner in results:
    winner_counts[winner] = winner_counts.get(winner, 0) + 1

  print(winner_counts)


if __name__ == "__main__":
  main()
