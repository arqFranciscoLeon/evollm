This repository accompanies the paper "Will Systems of LLM Agents Lead to Cooperation: An Investigation into a Social Dilemma".

- [AAMAS 2025 extended abstract](https://ifaamas.csc.liv.ac.uk/Proceedings/aamas2025/pdfs/p2786.pdf)
- [Full paper on arXiv](https://arxiv.org/pdf/2501.16173)

---

> **Cross-provider n=500 extension (2026).**
> [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20248614.svg)](https://doi.org/10.5281/zenodo.20248614)
> This fork extends the benchmark to four 2025–2026 frontier models at
> n=500 Moran iterations. See **[`EXTENSION.md`](./EXTENSION.md)** for the
> scientific overview and **[`REPRODUCE.md`](./REPRODUCE.md)** to verify the
> results in ~1 minute (`python reproduce_tables.py`).
> Paper: [arXiv:2605.29874](https://arxiv.org/abs/2605.29874).

> **Phase 2 — Chinese frontier models under a fixed converter (2026).**
> A second study asks whether the cooperative bias holds in a different
> alignment lineage, and whether the four Chinese labs behave as one bloc.
> It removes a confound in the phase above: instead of letting each model
> convert its own natural-language strategies into code, one fixed converter
> (GPT-5.4 Mini) does it for every lab, so cross-lab comparisons measure
> generation alone.
>
> This release adds the 24 Chinese strategy libraries (DeepSeek V4 Pro,
> Qwen3-Max, Kimi K2.5, GLM-5.1), the 12 head-to-head matrices, the n=500
> equilibria for all 48 conditions, and the pre-registered converter
> robustness check (the `*_robust.py` libraries and their re-run). The
> pre-registration, including every ante-hoc amendment and the exact served
> model identifiers, is in **[`PHASE2_PREREG.md`](./PHASE2_PREREG.md)**;
> `python reproduce_tables.py` recomputes H5 and H6 alongside the Phase 1
> tables.
>
> Phase 3 is pre-registered but not yet run:
> **[`PHASE3_PREREG.md`](./PHASE3_PREREG.md)**, together with the adversarial
> review it was put through before any data was collected.

---

This project is being extended to multi-player games: public goods game, collective risk dilemma and a common pool resource / fisheries game, in my other repo [emergent_llm](github.com/willis-richard/emergent_llm).

## Installation

Install the dependencies using conda

```shell
conda create -f environment.yml
```

Activate the environment and add the repo to the PYTHONPATH

```shell
conda activate evollm
export PYTHONPATH="$(pwd)/src"
```

## Prompts
[prompts](./src/evollm/prompts.py) contains the prompts used to generate the strategies.

## Strategies

[strategies](./strategies) contains the generated strategies used in the paper, except for the ChatGPT-4o strategies using the Refine prompt with noise, which have been accidentally lost. Each strategy includes both the natural language descriptions and the implemented algorithm. For the 'prose' prompt, we include both the high-level scenario strategy and the subsequent iterated normal-form game specific strategy.

## Results

[results](./results) contains the results shown in the paper

## Experiments

In order to rerun the analysis from the paper, follow these steps. To see the options, use `--help` on any of the scripts. You will need to configure the openai or anthropic API, and set the corresponding environmental variable `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`.

Create strategies, for example to use Claude 3.5 Sonnet with 10% noise and prose prompts to create 25 strategies for each attitude (75 in total):
```shell
python3 src/evollm/create_strategies.py --strategy_llm anthropic --n 25 --temp 0.7 --algo my_strategies --prose --noise 0.1
```

Inspect the strategies and then test they run. Either fix any broken strategies, or delete them and re-run create_strategies.py with the same algo name to regenerate the deleted strategies
```shell
python3 tests/test_create_strategies.py --algo my_strategies
```

Rank the strategies in Beaufils tournament using
```shell
python3 src/evollm/rank_strategies.py --algo my_strategies
```

Compare the head-to-head performance of the Attitude-Agents with
```shell
python3 src/evollm/head_to_head.py --algo my_strategies --h2h
```

and assess the Attiude-Agents' performance in the Beaufils tournament with
```shell
python3 src/evollm/head_to_head.py --algo my_strategies
```
