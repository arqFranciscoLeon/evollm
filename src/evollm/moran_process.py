import argparse
import axelrod as axl
import csv
import pprint
import matplotlib.pyplot as plt
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path
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


if __name__ == "__main__":
  parsed_args = parse_arguments()

  # N.B. create separate instances for each player, not copies!
  algos = algorithms.load_algorithms(parsed_args.algo, parsed_args.keep_top, parsed_args.keep_bottom)
  classes = algorithms.create_classes(algos)
  players = [cls() for cls, count in zip(classes, parsed_args.initial_pop) for _ in range(count)]
  print(players)

  if parsed_args.plot:
    mp = axl.MoranProcess(
        players,
        seed=1,
        turns=algos[0].rounds,
        noise=algos[0].noise,
        game=common.get_game(algos[0].game))

    populations = mp.play()
    ax = mp.populations_plot()

    fig = ax.get_figure()
    fig.set_size_inches(3, 2)

    ax.set_title('Population by iteration', fontsize=8)
    # ax.set_title(None)
    ax.set_xlabel(ax.get_xlabel(), fontsize=8)
    ax.set_ylabel(ax.get_ylabel(), fontsize=8)

    # ax.legend(labels=['Aggressive', 'Cooperative', 'Neutral'], bbox_to_anchor=(0, 1.3), loc='upper left', ncol=3, frameon=False, columnspacing=0.5, fontsize=9)
    ax.legend(labels=['Aggressive', 'Cooperative', 'Neutral'], loc='lower center', fontsize=8)

    ax.set_ylim(0, 12)
    ax.set_yticks(np.arange(0, 12 + 1, 4))

    fig = ax.get_figure()
    fig.savefig("results/example_moran.png", dpi=500, bbox_inches='tight')
  else:
    def run_moran_process(seed):
      try:
        mp = axl.MoranProcess(
            players,
            seed=seed,
            turns=algos[0].rounds,
            noise=algos[0].noise,
            game=common.get_game(algos[0].game))

        populations = mp.play()
        # pprint.pprint(populations)
        winner = mp.winning_strategy_name
        print(winner, len(mp))
        return winner
      except Exception as exc:
        import logging
        logging.getLogger(__name__).warning(
            "Moran iteration with seed=%s failed: %s: %s — skipping.",
            seed, type(exc).__name__, exc,
        )
        print(f"[WARN] seed={seed} failed ({type(exc).__name__}: {exc}) — skipped")
        return None

    seeds = np.random.randint(0, np.iinfo(np.int32).max, size=parsed_args.iterations)

    if parsed_args.processes > 1:
      with Pool(processes=parsed_args.processes) as pool:
        results = pool.map(run_moran_process, seeds)
    else:
      results = []
      for i in range(parsed_args.iterations):
        results.append(run_moran_process(seeds[i]))

    failed = results.count(None)
    if failed:
        print(f"[WARN] {failed} iteration(s) failed and were skipped out of {len(results)} total.")
    results = [r for r in results if r is not None]

    winner_counts = {}
    for winner in results:
        winner_counts[winner] = winner_counts.get(winner, 0) + 1

    print(winner_counts)

    # ── Normalizar claves a actitud base ─────────────────────────────────────
    # mp.winning_strategy_name devuelve el __repr__ del jugador, que para
    # StrategySampler es "LLM: Aggressive (ours)", "LLM: Cooperative (ours)",
    # o "LLM: Neutral (ours)". Mapeamos a las claves simples que usa el resto
    # del código.
    attitudes = ["Aggressive", "Cooperative", "Neutral"]
    normalized_counts: dict[str, int] = {att: 0 for att in attitudes}
    for name, count in winner_counts.items():
        for att in attitudes:
            if att in name:
                normalized_counts[att] += count
                break

    # ── Guardar resultados en disco ───────────────────────────────────────────
    algo_name = Path(parsed_args.algo).stem
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    total = sum(normalized_counts.values())

    # 1. Último resultado para este módulo (sobrescribe la ejecución anterior)
    latest_path = results_dir / f"{algo_name}_moran.csv"
    with open(latest_path, "w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=["Actitud", "Victorias", "Porcentaje"])
        writer.writeheader()
        for att in attitudes:
            count = normalized_counts[att]
            writer.writerow({
                "Actitud": att,
                "Victorias": count,
                "Porcentaje": round(100 * count / total, 2) if total else 0,
            })

    # 2. Historial acumulado (una fila por ejecución, nunca se borra)
    history_path = results_dir / "moran_history.csv"
    history_exists = history_path.exists()
    fieldnames_h = [
        "fecha", "algo", "iteraciones",
        "pop_agresivos", "pop_cooperativos", "pop_neutrales",
        "Aggressive", "Cooperative", "Neutral",
        "pct_Aggressive", "pct_Cooperative", "pct_Neutral",
    ]
    with open(history_path, "a", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_h)
        if not history_exists:
            writer.writeheader()
        writer.writerow({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "algo": algo_name,
            "iteraciones": parsed_args.iterations,
            "pop_agresivos": parsed_args.initial_pop[0],
            "pop_cooperativos": parsed_args.initial_pop[1],
            "pop_neutrales": parsed_args.initial_pop[2],
            "Aggressive": normalized_counts["Aggressive"],
            "Cooperative": normalized_counts["Cooperative"],
            "Neutral": normalized_counts["Neutral"],
            "pct_Aggressive": round(100 * normalized_counts["Aggressive"] / total, 2) if total else 0,
            "pct_Cooperative": round(100 * normalized_counts["Cooperative"] / total, 2) if total else 0,
            "pct_Neutral": round(100 * normalized_counts["Neutral"] / total, 2) if total else 0,
        })

    print(f"Resultados guardados en {latest_path} y {history_path}")

  # for row in mp.score_history:
  #   print([round(element, 1) for element in row])

  # plt.show()

  # for _ in range(1000):  # Run for 1000 steps
  #     next(mp)
  #     if mp.fixation_check():
  #         break

  # # Analyze population state
  # population_makeup = mp.population_distribution()
  # print(f"After {mp.time_steps} steps, population makeup: {population_makeup}")
