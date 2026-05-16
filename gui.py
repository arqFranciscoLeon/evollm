"""
EvoLLM — Interfaz Gráfica
Simulador evolutivo del Dilema del Prisionero con estrategias de LLM
"""

import ast
import io
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Rutas del proyecto
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent
RESULTS_DIR = PROJECT_ROOT / "results"
STRATEGIES_DIR = PROJECT_ROOT / "strategies"
SRC_DIR = PROJECT_ROOT / "src"
SRC_CREATE = PROJECT_ROOT / "src" / "evollm" / "create_strategies.py"
SRC_MORAN = PROJECT_ROOT / "src" / "evollm" / "moran_process.py"
SRC_H2H = PROJECT_ROOT / "src" / "evollm" / "head_to_head.py"

# Añadir src/ al path para poder importar evollm
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from evollm import llm_clients  # noqa: E402

# Cargar API keys desde .env si existe
llm_clients.load_api_keys()

# ---------------------------------------------------------------------------
# Listas de módulos disponibles (se recalcula en cada carga de página)
# ---------------------------------------------------------------------------
STRATEGY_MODULES = sorted([p.stem for p in STRATEGIES_DIR.glob("*.py")])

# ---------------------------------------------------------------------------
# Etiquetas de visualización
# ---------------------------------------------------------------------------
ATTITUDE_LABELS = {
    "Aggressive": "Agresivo",
    "Cooperative": "Cooperativo",
    "Neutral": "Neutral",
}

ATTITUDE_COLORS = {
    "Aggressive": "#EF553B",
    "Cooperative": "#00CC96",
    "Neutral": "#636EFA",
    "Agresivo": "#EF553B",
    "Cooperativo": "#00CC96",
}

# Nombres legibles para los módulos de estrategias
MODULE_LABELS: dict[str, str] = {
    # ── Modelos del paper original ────────────────────────────────────────────
    "anthropic_default":       "Claude 3.5 Sonnet [paper] — Prompt directo",
    "anthropic_default_noise": "Claude 3.5 Sonnet [paper] — Directo + ruido",
    "anthropic_prose":         "Claude 3.5 Sonnet [paper] — Escenario prosa",
    "anthropic_prose_noise":   "Claude 3.5 Sonnet [paper] — Prosa + ruido",
    "anthropic_refine":        "Claude 3.5 Sonnet [paper] — Refinado",
    "anthropic_refine_noise":  "Claude 3.5 Sonnet [paper] — Refinado + ruido",
    "openai_default":          "GPT-4o-latest [paper] — Prompt directo",
    "openai_default_noise":    "GPT-4o-latest [paper] — Directo + ruido",
    "openai_prose":            "GPT-4o-latest [paper] — Escenario prosa",
    "openai_prose_noise":      "GPT-4o-latest [paper] — Prosa + ruido",
    "openai_refine":           "GPT-4o-latest [paper] — Refinado",
    "openai_refine_noise":     "GPT-4o-latest [paper] — Refinado + ruido",
    # ── Modelos nuevos OpenAI (abril 2026) ────────────────────────────────────
    "openai_gpt54mini_default":       "GPT-5.4 Mini — Prompt directo",
    "openai_gpt54mini_default_noise": "GPT-5.4 Mini — Directo + ruido",
    "openai_gpt54mini_prose":         "GPT-5.4 Mini — Escenario prosa",
    "openai_gpt54mini_refine":        "GPT-5.4 Mini — Refinado",
    # ── Modelos nuevos Anthropic (abril 2026) ─────────────────────────────────
    "anthropic_sonnet46_default":       "Claude Sonnet 4.6 — Prompt directo",
    "anthropic_sonnet46_default_noise": "Claude Sonnet 4.6 — Directo + ruido",
    "anthropic_sonnet46_prose":         "Claude Sonnet 4.6 — Escenario prosa",
    "anthropic_sonnet46_refine":        "Claude Sonnet 4.6 — Refinado",
    # ── Google Gemini ─────────────────────────────────────────────────────────
    "gemini_25_flash_default":       "Gemini 2.5 Flash — Prompt directo",
    "gemini_25_flash_default_noise": "Gemini 2.5 Flash — Directo + ruido",
    "gemini_25_flash_prose":         "Gemini 2.5 Flash — Escenario prosa",
    "gemini_25_flash_refine":        "Gemini 2.5 Flash — Refinado",
    "gemini_31_pro_default":         "Gemini 3.1 Pro Preview — Prompt directo",
    "gemini_31_pro_default_noise":   "Gemini 3.1 Pro Preview — Directo + ruido",
    "gemini_31_pro_prose":           "Gemini 3.1 Pro Preview — Escenario prosa",
    "gemini_31_pro_refine":          "Gemini 3.1 Pro Preview — Refinado",
}

# Prefijo de archivo sugerido para cada modelo (tab Generar)
MODEL_FILE_PREFIXES: dict[str, str] = {
    # Originales del paper
    "chatgpt-4o-latest": "openai",
    "claude-3-5-sonnet":  "anthropic",
    # Nuevos (abril 2026)
    "gpt-5.4-mini":           "openai_gpt54mini",
    "claude-sonnet-4-6":      "anthropic_sonnet46",
    "gemini-2.5-flash":       "gemini_25_flash",
    "gemini-3.1-pro-preview": "gemini_31_pro",
}

# ---------------------------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="EvoLLM — Simulador del Dilema del Prisionero",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  .log-box {
    font-family: 'Courier New', monospace;
    font-size: 12px;
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 12px;
    border-radius: 6px;
    max-height: 300px;
    overflow-y: auto;
    white-space: pre-wrap;
    line-height: 1.4;
  }
  .metric-label { font-size: 13px; color: #888; }
  .metric-value { font-size: 28px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Estado de sesión
# ---------------------------------------------------------------------------
st.session_state.setdefault("moran_winner_counts", {})
st.session_state.setdefault("moran_last_algo", "")
st.session_state.setdefault("moran_plot_ready", False)
st.session_state.setdefault("torneo_last_algo", "")
st.session_state.setdefault("torneo_last_mode", "")


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------

def get_subprocess_env() -> dict:
    """Entorno con PYTHONPATH apuntando a src/ y variables de API keys."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    return env


def run_subprocess_streaming(cmd: list[str]):
    """Ejecuta un comando y hace yield de cada línea de salida.

    Finaliza con '__returncode__:{code}' como señal de retorno.
    """
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=get_subprocess_env(),
        cwd=str(PROJECT_ROOT),
    )
    for line in proc.stdout:
        yield line.rstrip()
    proc.wait()
    yield f"__returncode__:{proc.returncode}"


def parse_winner_counts(output_lines: list[str]) -> dict:
    """Extrae el dict de ganadores de la salida de moran_process.py."""
    for line in reversed(output_lines):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                return ast.literal_eval(line)
            except Exception:
                pass
    return {}


def parse_matrices_txt(
    filepath: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Parsea un archivo *_matrices.txt y retorna (cooperation_df, payoffs_df, summary_df)."""
    text = filepath.read_text(encoding="utf-8")
    sections: dict[str, str] = {}

    markers = ["Normalised cooperation:", "Payoffs:", "Results Summary:"]
    positions = []
    for m in markers:
        idx = text.find(m)
        if idx != -1:
            positions.append((idx, m))
    positions.sort()

    for i, (pos, marker) in enumerate(positions):
        start = pos + len(marker)
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        sections[marker] = text[start:end].strip()

    def read_df(key: str) -> pd.DataFrame:
        raw = sections.get(key, "")
        if not raw:
            return pd.DataFrame()
        try:
            return pd.read_csv(
                io.StringIO(raw), sep=r"\s{2,}", engine="python", index_col=0
            )
        except Exception:
            return pd.DataFrame()

    cooperation_df = read_df("Normalised cooperation:")
    payoffs_df = read_df("Payoffs:")

    summary_raw = sections.get("Results Summary:", "")
    try:
        summary_df = pd.read_csv(
            io.StringIO(summary_raw), sep=r"\s{2,}", engine="python"
        )
    except Exception:
        summary_df = pd.DataFrame()

    return cooperation_df, payoffs_df, summary_df


def make_heatmap(
    df: pd.DataFrame,
    title: str,
    colorscale: str = "RdYlGn",
    fmt: str = ".3f",
) -> go.Figure:
    """Retorna figura Plotly de heatmap con anotaciones numéricas."""
    if df.empty:
        return go.Figure()

    cols = [ATTITUDE_LABELS.get(c, c) for c in df.columns]
    rows = [ATTITUDE_LABELS.get(r, r) for r in df.index]
    values = df.values

    annotations = []
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            annotations.append(
                dict(
                    x=col,
                    y=row,
                    text=format(values[i, j], fmt),
                    showarrow=False,
                    font=dict(color="black", size=14),
                )
            )

    fig = go.Figure(
        data=go.Heatmap(
            z=values,
            x=cols,
            y=rows,
            colorscale=colorscale,
            zmin=0 if "RdYlGn" in colorscale else None,
            zmax=1 if "RdYlGn" in colorscale else None,
            showscale=True,
        )
    )
    fig.update_layout(
        title=title,
        annotations=annotations,
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(size=13),
    )
    return fig


def make_winner_bar(winner_counts: dict) -> go.Figure:
    """Gráfica de barras con distribución de ganadores del Proceso de Moran."""
    if not winner_counts:
        return go.Figure()

    labels = []
    values = []
    for name, count in sorted(winner_counts.items(), key=lambda x: -x[1]):
        label = ATTITUDE_LABELS.get(name, name)
        labels.append(label)
        values.append(count)

    total = sum(values)
    fig = px.bar(
        x=labels,
        y=values,
        color=labels,
        color_discrete_map={
            ATTITUDE_LABELS.get(k, k): v for k, v in ATTITUDE_COLORS.items()
        },
        text=[f"{v} ({100 * v / total:.1f}%)" if total else f"{v} (0.0%)" for v in values],
        labels={"x": "Actitud ganadora", "y": "Número de veces ganada"},
        title="Distribución de ganadores",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False,
        height=350,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def list_available_experiments() -> list[str]:
    """Lista los módulos para los que existe un archivo _matrices.txt en results/."""
    if not RESULTS_DIR.exists():
        return []
    return sorted(
        f.stem.replace("_matrices", "") for f in RESULTS_DIR.glob("*_matrices.txt")
    )


def list_moran_experiments() -> list[str]:
    """Lista los módulos para los que existe un archivo _moran.csv en results/."""
    if not RESULTS_DIR.exists():
        return []
    return sorted(
        f.stem.replace("_moran", "") for f in RESULTS_DIR.glob("*_moran.csv")
    )


def load_moran_latest(algo: str) -> dict:
    """Carga el último resultado Moran guardado para un módulo concreto."""
    csv_path = RESULTS_DIR / f"{algo}_moran.csv"
    if not csv_path.exists():
        return {}
    try:
        df = pd.read_csv(csv_path, encoding="utf8")
        return {row["Actitud"]: int(row["Victorias"]) for _, row in df.iterrows()}
    except Exception:
        return {}


def load_moran_history() -> pd.DataFrame:
    """Carga el historial completo de simulaciones Moran guardadas en disco."""
    history_path = RESULTS_DIR / "moran_history.csv"
    if not history_path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(history_path, encoding="utf8")
    except Exception:
        return pd.DataFrame()


def module_display_name(module: str) -> str:
    return MODULE_LABELS.get(module, module)


def _suggested_filename(model_key: str, prompt_type: str, noise: bool) -> str:
    prefix = MODEL_FILE_PREFIXES.get(model_key, model_key.replace("-", "_"))
    suffix = "_noise" if noise else ""
    return f"{prefix}_{prompt_type}{suffix}"


# ---------------------------------------------------------------------------
# Vista Paper — réplica de tablas y figuras del artículo (datos n=500)
# ---------------------------------------------------------------------------

# Colores idénticos a los del paper (make_figures.py)
PAPER_C_AGG = "#d62728"   # rojo
PAPER_C_COO = "#1f77b4"   # azul
PAPER_C_NEU = "#7f7f7f"   # gris

# Orden de las 12 combinaciones modelo–prompt (igual que la Tabla 5)
PAPER_ALGOS = [
    ("anthropic_sonnet46_default_75", "Claude 4.6",       "Default"),
    ("anthropic_sonnet46_prose_75",   "Claude 4.6",       "Prose"),
    ("anthropic_sonnet46_refine_75",  "Claude 4.6",       "Refine"),
    ("gemini_25_flash_default_75",    "Gemini 2.5 Flash", "Default"),
    ("gemini_25_flash_prose_75",      "Gemini 2.5 Flash", "Prose"),
    ("gemini_25_flash_refine_75",     "Gemini 2.5 Flash", "Refine"),
    ("gemini_31_pro_default_75",      "Gemini 3.1 Pro",   "Default"),
    ("gemini_31_pro_prose_75",        "Gemini 3.1 Pro",   "Prose"),
    ("gemini_31_pro_refine_75",       "Gemini 3.1 Pro",   "Refine"),
    ("openai_gpt54mini_default_75",   "GPT-5.4 Mini",     "Default"),
    ("openai_gpt54mini_prose_75",     "GPT-5.4 Mini",     "Prose"),
    ("openai_gpt54mini_refine_75",    "GPT-5.4 Mini",     "Refine"),
]

# Valores de referencia Willis et al. (Tabla 6 del paper original) — A/C/N
# por las 4 condiciones: 4:4:4 clean | 4:4:4 noise | 8:2:2 clean | 8:2:2 noise
PAPER_WILLIS_REF = {
    ("ChatGPT-4o", "Default"): ["14/53/33", "16/42/42", "66/19/17", "59/20/21"],
    ("ChatGPT-4o", "Prose"):   ["13/38/49", "23/41/36", "35/27/38", "60/18/22"],
    ("ChatGPT-4o", "Refine"):  ["19/48/33", "28/38/34", "49/30/21", "63/19/18"],
    ("Claude 3.5 Sonnet", "Default"): ["4/49/47",  "15/37/48", "36/24/40", "41/20/39"],
    ("Claude 3.5 Sonnet", "Prose"):   ["14/42/44", "17/33/50", "41/30/29", "61/26/13"],
    ("Claude 3.5 Sonnet", "Refine"):  ["16/51/33", "37/34/29", "50/22/28", "60/18/22"],
}
# Δnoise promedio de referencia (Tabla 8 del paper original)
PAPER_WILLIS_DNOISE = {
    "Claude 3.5 Sonnet": [12, 9, 17, 13],   # Default, Prose, Refine, Avg
    "ChatGPT-4o":        [11, -3, 10, 6],
}


@st.cache_data(show_spinner=False)
def load_n500_results() -> dict:
    """Carga el JSON autoritativo n=500 (modal_waves_final_*.json).

    Devuelve dict indexado por (algo, 'AAACCCNNN') -> registro.
    """
    import json
    files = sorted(RESULTS_DIR.glob("modal_waves_final_*.json"))
    if not files:
        return {}
    try:
        with open(files[-1], encoding="utf8") as fh:
            rows = json.load(fh)
    except Exception:
        return {}
    out = {}
    for r in rows:
        pop = f"{r['pop_agresivos']}{r['pop_cooperativos']}{r['pop_neutrales']}"
        out[(r["algo"], pop)] = r
    out["__file__"] = files[-1].name
    return out


def _fmt_acn(rec: dict) -> str:
    """'A/C/N' redondeado a enteros desde un registro n=500."""
    if not rec:
        return "—"
    return (f"{round(rec['pct_Aggressive'])}/"
            f"{round(rec['pct_Cooperative'])}/"
            f"{round(rec['pct_Neutral'])}")


def _z_test_prop(x1: int, x2: int, n1: int = 500, n2: int = 500):
    """z-test de dos proporciones (pooled)."""
    import math
    p1, p2 = x1 / n1, x2 / n2
    pp = (x1 + x2) / (n1 + n2)
    if pp in (0.0, 1.0):
        return 0.0, 1.0
    se = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se
    # p-valor dos colas vía aprox. normal (sin scipy para no añadir dependencia)
    p = math.erfc(abs(z) / math.sqrt(2))
    return z, p


# ---------------------------------------------------------------------------
# Encabezado principal
# ---------------------------------------------------------------------------
st.title("🧬 EvoLLM — Simulador del Dilema del Prisionero")
st.caption(
    "Herramienta de investigación: simulación evolutiva de estrategias generadas por LLMs "
    "en juegos de dilema social (Proceso de Moran)."
)

tab_gen, tab_moran, tab_torneo, tab_dashboard, tab_paper, tab_export = st.tabs([
    "🤖  Generar Estrategias",
    "🔁  Simulación Moran",
    "⚔️  Torneo",
    "📊  Dashboard Comparativo",
    "📄  Vista Paper",
    "⬇️  Exportar",
])


# ===========================================================================
# PESTAÑA 1: GENERACIÓN DE ESTRATEGIAS
# ===========================================================================
with tab_gen:
    st.header("Generación de Estrategias con LLMs")
    st.markdown(
        """
        Genera un nuevo conjunto de estrategias llamando a la API del modelo seleccionado.
        Cada generación produce **3 × n estrategias** (una por actitud: Agresiva, Cooperativa, Neutral).

        Las claves de API se leen del archivo **`.env`** en la raíz del proyecto
        (copia `.env.example` y rellena tus claves).
        """
    )

    model_options = list(llm_clients.MODEL_REGISTRY.keys())
    model_display = {k: llm_clients.MODEL_DISPLAY_NAMES.get(k, k) for k in model_options}

    col_g1, col_g2 = st.columns([1, 1])

    with col_g1:
        st.subheader("Configuración del modelo")
        selected_model = st.selectbox(
            "Modelo",
            model_options,
            format_func=lambda k: model_display[k],
            help="Selecciona el modelo LLM que generará las estrategias.",
        )

        prompt_type = st.selectbox(
            "Tipo de prompt",
            ["default", "prose", "refine"],
            format_func={
                "default": "Directo (standard IPD)",
                "prose": "Prosa (escenario real → IPD)",
                "refine": "Refinado (el LLM critica y mejora)",
            }.get,
            help=(
                "**Directo**: el LLM recibe directamente el dilema. "
                "**Prosa**: un escenario real (ciencia, comercio, etc.) se convierte a IPD. "
                "**Refinado**: se pide al LLM que critique y reescriba su estrategia."
            ),
        )

        n_per_attitude = st.number_input(
            "Estrategias por actitud (n)",
            min_value=1,
            max_value=25,
            value=5,
            help="Total generado = 3 × n (una por cada actitud).",
        )

        temperature = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Mayor temperatura = mayor variedad pero menor coherencia.",
        )

    with col_g2:
        st.subheader("Opciones adicionales")

        add_noise = st.checkbox(
            "Añadir ruido (10%)",
            value=False,
            help="Añade una probabilidad del 10% de que cada acción sea intercambiada.",
        )

        suggested_name = _suggested_filename(selected_model, prompt_type, add_noise)
        algo_name = st.text_input(
            "Nombre del archivo de salida (en strategies/)",
            value=suggested_name,
            help="El archivo se guardará como strategies/{nombre}.py",
        )

        st.markdown("---")
        st.subheader("Resumen")
        provider, model_id = llm_clients.MODEL_REGISTRY[selected_model]
        st.markdown(f"- **Proveedor**: `{provider}`")
        st.markdown(f"- **Modelo API**: `{model_id}`")
        st.markdown(f"- **Total a generar**: `{3 * n_per_attitude}` estrategias")
        st.markdown(f"- **Archivo de salida**: `strategies/{algo_name}.py`")

        output_path = STRATEGIES_DIR / f"{algo_name}.py"
        if output_path.exists():
            st.warning(
                f"⚠️ `strategies/{algo_name}.py` ya existe. "
                "Cambia el nombre o el archivo será sobreescrito."
            )

    st.markdown("---")

    gen_btn = st.button(
        f"▶  Generar {3 * n_per_attitude} estrategias con {model_display[selected_model]}",
        use_container_width=True,
        type="primary",
    )

    if gen_btn:
        if not algo_name.strip():
            st.error("⚠️ El nombre del archivo no puede estar vacío.")
        elif output_path.exists():
            st.error(
                f"⚠️ El archivo `strategies/{algo_name}.py` ya existe. "
                "Elimínalo o cambia el nombre antes de continuar."
            )
        else:
            cmd_gen = [
                sys.executable, str(SRC_CREATE),
                "--strategy_llm", provider,
                "--model", selected_model,
                "--n", str(n_per_attitude),
                "--temp", str(temperature),
                "--algo", str(STRATEGIES_DIR / algo_name),
            ]
            if prompt_type == "prose":
                cmd_gen.append("--prose")
            elif prompt_type == "refine":
                cmd_gen.append("--refine")
            if add_noise:
                cmd_gen += ["--noise", "0.1"]

            st.markdown("**Registro de generación:**")
            log_ph_gen = st.empty()
            rc_gen = 0

            with st.spinner(
                f"Generando estrategias con {model_display[selected_model]}... "
                "(puede tardar varios minutos)"
            ):
                log_gen = ""
                for line in run_subprocess_streaming(cmd_gen):
                    if line.startswith("__returncode__:"):
                        rc_gen = int(line.split(":")[1])
                    else:
                        log_gen += line + "\n"
                        log_ph_gen.markdown(
                            f'<div class="log-box">{log_gen[-4000:]}</div>',
                            unsafe_allow_html=True,
                        )

            if rc_gen != 0:
                st.error(
                    f"La generación terminó con error (código {rc_gen}). "
                    "Revisa el log y verifica que las API keys estén configuradas en `.env`."
                )
            else:
                st.success(
                    f"✅ Estrategias generadas en `strategies/{algo_name}.py`. "
                    "Ahora puedes ejecutar el Torneo o la Simulación Moran."
                )
                # Actualizar la lista de módulos en sesión
                st.session_state["new_module_generated"] = algo_name


# ===========================================================================
# PESTAÑA 2: SIMULACIÓN MORAN
# ===========================================================================
with tab_moran:
    st.header("Proceso de Moran — Simulación Evolutiva")
    st.markdown(
        """
        El **Proceso de Moran** simula cómo una población de jugadores evoluciona a lo largo
        del tiempo. En cada paso, el jugador con mayor puntaje se "reproduce" y otro muere,
        hasta que una sola estrategia domina la población (**fijación**).

        Puedes correr cientos de iteraciones para estimar qué actitud (Agresiva, Cooperativa o
        Neutral) tiende a ganar con más frecuencia.
        """
    )

    # Recargar lista de módulos (puede haber cambiado tras generar)
    current_modules = sorted([p.stem for p in STRATEGIES_DIR.glob("*.py")])

    with st.form("moran_form"):
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.subheader("Estrategias y simulación")
            algo_sel = st.selectbox(
                "Módulo de estrategias",
                current_modules,
                format_func=module_display_name,
                help="Elige el conjunto de estrategias LLM a usar en la simulación.",
            )

            iteraciones = st.slider(
                "Número de iteraciones",
                min_value=10,
                max_value=500,
                value=100,
                step=10,
                help="Cuántas veces se repite la simulación completa.",
            )

            procesos = st.slider(
                "Procesos paralelos",
                min_value=1,
                max_value=8,
                value=1,
                help="En Windows se recomienda 1 para evitar errores de multiprocessing.",
            )

            modo_trayectoria = st.checkbox(
                "Mostrar trayectoria individual (una sola ejecución con gráfico)",
                value=False,
            )

        with col_right:
            st.subheader("Población inicial")
            st.caption("Define cuántos jugadores de cada actitud inician la simulación.")

            n_agresivos = st.number_input(
                "Jugadores Agresivos", min_value=1, max_value=20, value=4
            )
            n_cooperativos = st.number_input(
                "Jugadores Cooperativos", min_value=1, max_value=20, value=4
            )
            n_neutrales = st.number_input(
                "Jugadores Neutrales", min_value=1, max_value=20, value=4
            )

            st.markdown("---")
            st.subheader("Filtro de estrategias")

            keep_top = st.slider(
                "keep_top (0 = las mejores, 0.5 = top 50%)",
                min_value=0.0,
                max_value=0.9,
                value=0.0,
                step=0.05,
            )
            keep_bottom = st.slider(
                "keep_bottom (1 = todas, 0.5 = bottom 50%)",
                min_value=0.1,
                max_value=1.0,
                value=1.0,
                step=0.05,
            )

        ejecutar_moran = st.form_submit_button(
            "▶  Ejecutar simulación", use_container_width=True
        )

    if ejecutar_moran:
        if keep_top >= keep_bottom:
            st.error("⚠️ keep_top debe ser menor que keep_bottom.")
        else:
            algo_path = str(STRATEGIES_DIR / algo_sel)
            cmd = [
                sys.executable,
                str(SRC_MORAN),
                "--algo",
                algo_path,
                "--initial_pop",
                str(n_agresivos),
                str(n_cooperativos),
                str(n_neutrales),
                "--keep_top",
                str(keep_top),
                "--keep_bottom",
                str(keep_bottom),
            ]
            if modo_trayectoria:
                cmd.append("--plot")
            else:
                cmd += [
                    "--iterations",
                    str(iteraciones),
                    "--processes",
                    str(procesos),
                ]

            st.markdown("**Registro de ejecución:**")
            log_placeholder = st.empty()
            output_lines = []
            returncode = 0

            with st.spinner("Simulando..."):
                log_text = ""
                for line in run_subprocess_streaming(cmd):
                    if line.startswith("__returncode__:"):
                        returncode = int(line.split(":")[1])
                    else:
                        output_lines.append(line)
                        log_text += line + "\n"
                        log_placeholder.markdown(
                            f'<div class="log-box">{log_text[-3000:]}</div>',
                            unsafe_allow_html=True,
                        )

            if returncode != 0:
                st.error(
                    f"La simulación terminó con error (código {returncode}). Revisa el log."
                )
            else:
                st.success("✅ Simulación completada.")

                if modo_trayectoria:
                    moran_img = RESULTS_DIR / "example_moran.png"
                    if moran_img.exists():
                        st.subheader("Trayectoria de población")
                        st.image(str(moran_img), use_container_width=False, width=600)
                else:
                    winner_counts = parse_winner_counts(output_lines)
                    if winner_counts:
                        st.session_state["moran_winner_counts"] = winner_counts
                        st.session_state["moran_last_algo"] = algo_sel

                        st.subheader("Resultados — Distribución de ganadores")
                        total = sum(winner_counts.values())
                        cols_met = st.columns(len(winner_counts))
                        for i, (name, count) in enumerate(
                            sorted(winner_counts.items(), key=lambda x: -x[1])
                        ):
                            label = ATTITUDE_LABELS.get(name, name)
                            with cols_met[i]:
                                st.metric(
                                    label=label,
                                    value=f"{count} veces",
                                    delta=f"{100 * count / total:.1f}%",
                                )

                        st.plotly_chart(
                            make_winner_bar(winner_counts),
                            use_container_width=True,
                            key="moran_winner_bar",
                        )
                    else:
                        st.warning(
                            "No se pudo extraer el conteo de ganadores del log."
                        )


# ===========================================================================
# PESTAÑA 3: TORNEO
# ===========================================================================
with tab_torneo:
    st.header("Análisis de Torneo")
    st.markdown(
        """
        Compara estrategias LLM mediante torneos:

        - **Beaufils**: Las estrategias LLM se enfrentan a 11 estrategias clásicas
          (Cooperador, Traidor, TitForTat, Rencoroso, etc.).

        - **Head-to-head**: Las estrategias LLM se enfrentan entre sí.
          Genera matrices de cooperación y pagos por actitud.
        """
    )

    torneo_modules = sorted([p.stem for p in STRATEGIES_DIR.glob("*.py")])

    with st.form("torneo_form"):
        col_t1, col_t2 = st.columns([1, 1])

        with col_t1:
            algo_t = st.selectbox(
                "Módulo de estrategias",
                torneo_modules,
                format_func=module_display_name,
            )
            modo_torneo = st.radio(
                "Tipo de torneo",
                [
                    "Beaufils (LLM vs estrategias clásicas)",
                    "Head-to-head (LLM vs LLM)",
                ],
            )

        with col_t2:
            st.subheader("Filtro de estrategias")
            keep_top_t = st.slider(
                "keep_top",
                min_value=0.0,
                max_value=0.9,
                value=0.0,
                step=0.05,
                key="t_kt",
            )
            keep_bottom_t = st.slider(
                "keep_bottom",
                min_value=0.1,
                max_value=1.0,
                value=1.0,
                step=0.05,
                key="t_kb",
            )

        ejecutar_torneo = st.form_submit_button(
            "▶  Ejecutar torneo", use_container_width=True
        )

    if ejecutar_torneo:
        if keep_top_t >= keep_bottom_t:
            st.error("⚠️ keep_top debe ser menor que keep_bottom.")
        else:
            algo_t_path = str(STRATEGIES_DIR / algo_t)
            cmd_t = [
                sys.executable,
                str(SRC_H2H),
                "--algo",
                algo_t_path,
                "--keep_top",
                str(keep_top_t),
                "--keep_bottom",
                str(keep_bottom_t),
            ]
            if "Head-to-head" in modo_torneo:
                cmd_t.append("--h2h")

            st.markdown("**Registro de ejecución:**")
            log_ph_t = st.empty()
            out_lines_t = []
            rc_t = 0

            with st.spinner("Ejecutando torneo (puede tardar varios minutos)..."):
                log_t = ""
                for line in run_subprocess_streaming(cmd_t):
                    if line.startswith("__returncode__:"):
                        rc_t = int(line.split(":")[1])
                    else:
                        out_lines_t.append(line)
                        log_t += line + "\n"
                        log_ph_t.markdown(
                            f'<div class="log-box">{log_t[-3000:]}</div>',
                            unsafe_allow_html=True,
                        )

            if rc_t != 0:
                st.error(f"El torneo terminó con error (código {rc_t}).")
            else:
                st.success("✅ Torneo completado.")
                st.session_state["torneo_last_algo"] = algo_t
                st.session_state["torneo_last_mode"] = modo_torneo

                if "Beaufils" in modo_torneo:
                    beaufils_svg = RESULTS_DIR / "beaufils.svg"
                    if beaufils_svg.exists():
                        st.subheader("Resultados Beaufils")
                        st.image(str(beaufils_svg), use_container_width=True)
                    else:
                        st.warning(
                            "No se encontró el archivo beaufils.svg en results/."
                        )
                else:
                    matrices_file = RESULTS_DIR / f"{algo_t}_matrices.txt"
                    if matrices_file.exists():
                        coop_df, pay_df, sum_df = parse_matrices_txt(matrices_file)

                        st.subheader("Matrices de interacción")
                        col_h1, col_h2 = st.columns(2)
                        with col_h1:
                            st.plotly_chart(
                                make_heatmap(
                                    coop_df,
                                    "Tasa de Cooperación (0=traición, 1=cooperación total)",
                                    "RdYlGn",
                                    ".3f",
                                ),
                                use_container_width=True,
                                key="torneo_h2h_coop",
                            )
                        with col_h2:
                            st.plotly_chart(
                                make_heatmap(
                                    pay_df, "Pagos medios por actitud", "Blues", ".2f"
                                ),
                                use_container_width=True,
                                key="torneo_h2h_pay",
                            )

                        if not sum_df.empty:
                            st.subheader("Tabla de clasificación")
                            st.dataframe(sum_df, use_container_width=True, height=400)
                    else:
                        st.warning(
                            f"No se encontró {matrices_file.name} en results/."
                        )


# ===========================================================================
# PESTAÑA 4: DASHBOARD COMPARATIVO
# ===========================================================================
with tab_dashboard:
    st.header("Dashboard Comparativo")
    st.markdown(
        "Explora y compara los resultados de múltiples experimentos. "
        "Ideal para contrastar los modelos originales del paper contra los nuevos modelos."
    )

    available = list_available_experiments()

    if not available:
        st.info(
            "No hay resultados disponibles aún. "
            "Ejecuta un torneo Head-to-head en la pestaña ⚔️ Torneo para generar datos."
        )
    else:
        # --- Selector de experimento individual ---
        exp_sel = st.selectbox(
            "Experimento a explorar",
            available,
            format_func=module_display_name,
        )

        matrices_path = RESULTS_DIR / f"{exp_sel}_matrices.txt"
        coop_df, pay_df, sum_df = parse_matrices_txt(matrices_path)

        # Métricas rápidas
        if not sum_df.empty:
            name_col = "Name" if "Name" in sum_df.columns else sum_df.columns[0]
            score_col = "Median_score" if "Median_score" in sum_df.columns else None
            coop_col = (
                "Cooperation_rating" if "Cooperation_rating" in sum_df.columns else None
            )

            st.subheader("Métricas generales")
            mc1, mc2, mc3, mc4 = st.columns(4)
            with mc1:
                st.metric("Total de estrategias", len(sum_df))
            if score_col:
                with mc2:
                    best_row = sum_df.loc[sum_df[score_col].idxmax()]
                    best_name = best_row.get(name_col, "?")
                    st.metric(
                        "Mejor puntaje",
                        f"{sum_df[score_col].max():.3f}",
                        delta=str(best_name),
                    )
                with mc3:
                    st.metric("Puntaje promedio", f"{sum_df[score_col].mean():.3f}")
            if coop_col:
                with mc4:
                    st.metric("Cooperación media", f"{sum_df[coop_col].mean():.3f}")

        st.markdown("---")

        # Heatmaps
        st.subheader("Matrices de interacción entre actitudes")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.plotly_chart(
                make_heatmap(coop_df, "Tasa de Cooperación normalizada", "RdYlGn", ".3f"),
                use_container_width=True,
                key="dash_coop",
            )
        with col_d2:
            st.plotly_chart(
                make_heatmap(pay_df, "Pagos medios por actitud", "Blues", ".2f"),
                use_container_width=True,
                key="dash_pay",
            )

        # Radar de actitudes
        if not coop_df.empty:
            st.subheader("Perfil de cooperación por actitud (radar)")
            attitudes_orig = list(coop_df.index)
            categories = [ATTITUDE_LABELS.get(a, a) for a in coop_df.columns]

            fig_radar = go.Figure()
            colors_radar = ["#EF553B", "#00CC96", "#636EFA"]
            for i, att in enumerate(attitudes_orig):
                vals = coop_df.loc[att].tolist()
                vals_closed = vals + [vals[0]]
                cats_closed = categories + [categories[0]]
                fig_radar.add_trace(
                    go.Scatterpolar(
                        r=vals_closed,
                        theta=cats_closed,
                        fill="toself",
                        name=ATTITUDE_LABELS.get(att, att),
                        line_color=colors_radar[i % len(colors_radar)],
                        opacity=0.7,
                    )
                )
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(range=[0, 1], tickfont_size=10)),
                height=350,
                margin=dict(l=40, r=40, t=40, b=40),
                legend=dict(orientation="h", y=-0.1),
            )
            st.plotly_chart(fig_radar, use_container_width=False, key="dash_radar")

        # Ganadores Moran — selector independiente (no ligado al exp. de torneo)
        st.markdown("---")
        st.subheader("Simulación Moran — Distribución de ganadores")

        moran_exps_dash = list_moran_experiments()
        moran_counts_session = st.session_state.get("moran_winner_counts", {})
        last_algo_session = st.session_state.get("moran_last_algo", "")

        if moran_exps_dash:
            moran_sel_dash = st.selectbox(
                "Módulo Moran a visualizar",
                moran_exps_dash,
                format_func=module_display_name,
                key="dash_moran_sel",
            )
            moran_counts_disk = load_moran_latest(moran_sel_dash)

            if sum(moran_counts_disk.values()) > 0:
                st.caption(f"Fuente: archivo guardado · Módulo: **{module_display_name(moran_sel_dash)}**")
                st.plotly_chart(
                    make_winner_bar(moran_counts_disk),
                    use_container_width=True,
                    key="dash_winner_bar_disk",
                )
            else:
                st.warning(
                    "El archivo guardado tiene todas las victorias en 0 — "
                    "probablemente esa ejecución falló por el bug de `None` (ya corregido). "
                    "Vuelve a ejecutar la simulación en la pestaña 🔁 Simulación Moran."
                )
        elif moran_counts_session and sum(moran_counts_session.values()) > 0:
            st.caption(f"Fuente: sesión actual · Módulo: **{module_display_name(last_algo_session)}**")
            st.plotly_chart(
                make_winner_bar(moran_counts_session),
                use_container_width=True,
                key="dash_winner_bar_session",
            )
        else:
            st.info(
                "No hay resultados Moran guardados aún. "
                "Ejecuta una simulación en la pestaña 🔁 Simulación Moran."
            )

        # Historial completo de simulaciones Moran
        moran_hist = load_moran_history()
        if not moran_hist.empty:
            st.markdown("---")
            st.subheader("Historial de todas las simulaciones Moran")
            filas_invalidas = int((moran_hist["Aggressive"] + moran_hist["Cooperative"] + moran_hist["Neutral"] == 0).sum())
            caption_txt = "Cada fila es una ejecución guardada. Se acumula automáticamente."
            if filas_invalidas:
                caption_txt += f" ⚠️ {filas_invalidas} ejecución(es) con victorias en 0 (bug corregido — re-ejecutar)."
            st.caption(caption_txt)

            # Agregar nombre legible
            moran_hist["Modelo"] = moran_hist["algo"].apply(module_display_name)

            # Gráfico comparativo de % de victorias entre modelos
            hist_rows = []
            for _, row in moran_hist.iterrows():
                total_h = row["Aggressive"] + row["Cooperative"] + row["Neutral"]
                if total_h == 0:
                    continue
                label = f"{module_display_name(row['algo'])} ({row['fecha'][:10]})"
                for att in ["Aggressive", "Cooperative", "Neutral"]:
                    hist_rows.append({
                        "Ejecución": label,
                        "Actitud": ATTITUDE_LABELS.get(att, att),
                        "% victorias": round(100 * row[att] / total_h, 1),
                    })

            if hist_rows:
                hist_df_plot = pd.DataFrame(hist_rows)
                fig_hist = px.bar(
                    hist_df_plot,
                    x="Ejecución",
                    y="% victorias",
                    color="Actitud",
                    barmode="group",
                    color_discrete_map={
                        "Agresivo": "#EF553B",
                        "Cooperativo": "#00CC96",
                        "Neutral": "#636EFA",
                    },
                    title="% de victorias por actitud en cada simulación",
                )
                fig_hist.update_layout(
                    height=420,
                    xaxis_tickangle=-30,
                    margin=dict(l=10, r=10, t=50, b=120),
                )
                st.plotly_chart(fig_hist, use_container_width=True, key="dash_moran_hist")

            # Tabla del historial
            display_cols = [
                "fecha", "Modelo", "iteraciones",
                "pop_agresivos", "pop_cooperativos", "pop_neutrales",
                "pct_Aggressive", "pct_Cooperative", "pct_Neutral",
            ]
            cols_present = [c for c in display_cols if c in moran_hist.columns]
            st.dataframe(moran_hist[cols_present].rename(columns={
                "fecha": "Fecha",
                "iteraciones": "Iteraciones",
                "pop_agresivos": "Ini. Agresivos",
                "pop_cooperativos": "Ini. Cooperativos",
                "pop_neutrales": "Ini. Neutrales",
                "pct_Aggressive": "% Agresivo gana",
                "pct_Cooperative": "% Cooperativo gana",
                "pct_Neutral": "% Neutral gana",
            }), use_container_width=True)

        # Imagen trayectoria Moran si existe
        moran_img_path = RESULTS_DIR / "example_moran.png"
        exp_img_path = RESULTS_DIR / f"{exp_sel}.png"
        img_to_show = (
            exp_img_path
            if exp_img_path.exists()
            else (moran_img_path if moran_img_path.exists() else None)
        )
        if img_to_show:
            st.markdown("---")
            st.subheader("Trayectoria de población (Proceso de Moran)")
            st.image(str(img_to_show), width=600)

        # Tabla de clasificación con filtros
        if not sum_df.empty:
            st.markdown("---")
            st.subheader("Tabla de clasificación completa")

            name_col = "Name" if "Name" in sum_df.columns else sum_df.columns[0]
            score_col = "Median_score" if "Median_score" in sum_df.columns else None

            fc1, fc2 = st.columns([1, 2])
            with fc1:
                att_filter = st.multiselect(
                    "Filtrar por actitud",
                    ["Aggressive", "Cooperative", "Neutral"],
                    default=["Aggressive", "Cooperative", "Neutral"],
                    format_func=lambda x: ATTITUDE_LABELS.get(x, x),
                )
            with fc2:
                if score_col and score_col in sum_df.columns:
                    min_score = float(sum_df[score_col].min())
                    max_score = float(sum_df[score_col].max())
                    if min_score < max_score:
                        score_range = st.slider(
                            "Rango de puntaje",
                            min_value=min_score,
                            max_value=max_score,
                            value=(min_score, max_score),
                            step=0.01,
                            key="dash_score_range",
                        )
                    else:
                        score_range = (min_score, max_score)

            filtered_df = sum_df.copy()
            if name_col in filtered_df.columns and att_filter:
                mask = filtered_df[name_col].str.contains(
                    "|".join(att_filter), na=False
                )
                filtered_df = filtered_df[mask]
            if score_col and score_col in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df[score_col] >= score_range[0])
                    & (filtered_df[score_col] <= score_range[1])
                ]

            st.dataframe(filtered_df, use_container_width=True, height=450)

        # --- Comparación entre experimentos ---
        st.markdown("---")
        st.subheader("Comparación entre modelos")
        st.caption(
            "Selecciona 2 o más experimentos para comparar el puntaje mediano por actitud. "
            "Útil para ver si los modelos nuevos cooperan más o menos que los originales del paper."
        )

        compare_sel = st.multiselect(
            "Experimentos a comparar",
            available,
            default=available[:2] if len(available) >= 2 else available,
            format_func=module_display_name,
            key="dash_compare_sel",
        )

        if len(compare_sel) >= 2:
            compare_rows = []
            for exp in compare_sel:
                mpath = RESULTS_DIR / f"{exp}_matrices.txt"
                _, _, sdf = parse_matrices_txt(mpath)
                if sdf.empty:
                    continue
                name_c = "Name" if "Name" in sdf.columns else sdf.columns[0]
                score_c = "Median_score" if "Median_score" in sdf.columns else None
                if not score_c:
                    continue
                for att in ["Aggressive", "Cooperative", "Neutral"]:
                    subset = sdf[sdf[name_c].str.startswith(att)]
                    if not subset.empty:
                        compare_rows.append(
                            {
                                "Experimento": module_display_name(exp),
                                "Actitud": ATTITUDE_LABELS.get(att, att),
                                "Puntaje mediano": subset[score_c].median(),
                            }
                        )

            if compare_rows:
                compare_df = pd.DataFrame(compare_rows)
                fig_cmp = px.bar(
                    compare_df,
                    x="Experimento",
                    y="Puntaje mediano",
                    color="Actitud",
                    barmode="group",
                    color_discrete_map={
                        "Agresivo": "#EF553B",
                        "Cooperativo": "#00CC96",
                        "Neutral": "#636EFA",
                    },
                    title="Puntaje mediano por actitud y modelo",
                )
                fig_cmp.update_layout(
                    height=450,
                    xaxis_tickangle=-25,
                    margin=dict(l=10, r=10, t=50, b=100),
                )
                st.plotly_chart(
                    fig_cmp, use_container_width=True, key="dash_compare"
                )
            else:
                st.info(
                    "No hay datos suficientes para comparar los experimentos seleccionados."
                )
        elif len(compare_sel) == 1:
            st.info("Selecciona al menos 2 experimentos para comparar.")


# ===========================================================================
# PESTAÑA 5: VISTA PAPER — réplica de tablas y figuras del artículo
# ===========================================================================
with tab_paper:
    st.header("📄 Vista Paper — Resultados como en el artículo")
    st.markdown(
        "Réplica transparente de las **tablas y figuras del paper** a partir de "
        "los resultados autoritativos **n=500** "
        "(`modal_waves_final_*.json`). Cada número aquí es el mismo que aparece "
        "en el manuscrito."
    )

    n500 = load_n500_results()

    if not n500:
        st.warning(
            "No se encontró el archivo `results/modal_waves_final_*.json` "
            "(resultados n=500). Ejecuta el run wave-based "
            "(`modal run modal_moran_waves.py`) o copia el JSON a `results/`."
        )
    else:
        st.caption(f"Fuente: `{n500.get('__file__', '?')}` · n=500 iteraciones por condición")

        POPS = [("444", "4:4:4 clean", False), ("444", "4:4:4 noise", True),
                ("822", "8:2:2 clean", False), ("822", "8:2:2 noise", True)]

        def _rec(algo, pop, noise):
            return n500.get((algo + ("_noise" if noise else ""), pop), {})

        # ---- TABLA 5 — Equilibrios Moran -----------------------------------
        st.subheader("Tabla 5 — Proporciones de equilibrio Moran (%A / %C / %N)")
        st.caption(
            "Proporción de 500 corridas que convergen a cada actitud. "
            "Filas inferiores: valores de referencia de Willis et al. (paper original)."
        )
        t5_rows = []
        for algo, model, prompt in PAPER_ALGOS:
            t5_rows.append({
                "Modelo": model, "Prompt": prompt,
                "4:4:4 clean": _fmt_acn(_rec(algo, "444", False)),
                "4:4:4 noise": _fmt_acn(_rec(algo, "444", True)),
                "8:2:2 clean": _fmt_acn(_rec(algo, "822", False)),
                "8:2:2 noise": _fmt_acn(_rec(algo, "822", True)),
            })
        for (model, prompt), vals in PAPER_WILLIS_REF.items():
            t5_rows.append({
                "Modelo": f"{model} †", "Prompt": prompt,
                "4:4:4 clean": vals[0], "4:4:4 noise": vals[1],
                "8:2:2 clean": vals[2], "8:2:2 noise": vals[3],
            })
        t5_df = pd.DataFrame(t5_rows)
        st.dataframe(t5_df, use_container_width=True, hide_index=True,
                     height=560)
        st.caption("† Willis et al. \\cite{Willis2025_llm_ipd}, Tabla 6 (referencia).")
        st.download_button(
            "⬇️ Descargar Tabla 5 (CSV)",
            t5_df.to_csv(index=False).encode("utf8"),
            "tabla5_moran_equilibria_n500.csv", "text/csv",
            key="dl_t5",
        )

        # ---- FIGURA 2 — Distribución de equilibrios (4 paneles) ------------
        st.markdown("---")
        st.subheader("Figura 2 — Distribución de equilibrios (48 condiciones)")
        st.caption(
            "Barras apiladas: proporción de 500 corridas → Agresivo (rojo), "
            "Cooperativo (azul), Neutral (gris). Línea discontinua: prior teórico."
        )
        from plotly.subplots import make_subplots

        short_labels = [f"{m.split()[0][:3]}.{p[:3]}"
                        for _, m, p in PAPER_ALGOS]
        fig2 = make_subplots(rows=2, cols=2,
                             subplot_titles=[pl[1] for pl in POPS],
                             vertical_spacing=0.16, horizontal_spacing=0.08)
        for idx, (popk, label, noise) in enumerate(POPS):
            r, c = idx // 2 + 1, idx % 2 + 1
            A, C, N = [], [], []
            for algo, _, _ in PAPER_ALGOS:
                rec = _rec(algo, popk, noise)
                A.append(round(rec.get("pct_Aggressive", 0)))
                C.append(round(rec.get("pct_Cooperative", 0)))
                N.append(round(rec.get("pct_Neutral", 0)))
            show_leg = (idx == 0)
            fig2.add_trace(go.Bar(x=short_labels, y=A, name="Agresivo",
                                  marker_color=PAPER_C_AGG, legendgroup="A",
                                  showlegend=show_leg), row=r, col=c)
            fig2.add_trace(go.Bar(x=short_labels, y=C, name="Cooperativo",
                                  marker_color=PAPER_C_COO, legendgroup="C",
                                  showlegend=show_leg), row=r, col=c)
            fig2.add_trace(go.Bar(x=short_labels, y=N, name="Neutral",
                                  marker_color=PAPER_C_NEU, legendgroup="N",
                                  showlegend=show_leg), row=r, col=c)
            prior = 33 if popk == "444" else 67
            fig2.add_hline(y=prior, line_dash="dash", line_color="black",
                           opacity=0.5, row=r, col=c)
        fig2.update_layout(barmode="stack", height=620,
                           legend=dict(orientation="h", y=1.08, x=0.5,
                                       xanchor="center"),
                           margin=dict(l=40, r=20, t=70, b=80))
        fig2.update_xaxes(tickangle=-60, tickfont_size=8)
        fig2.update_yaxes(range=[0, 100], title_text="Freq. equilibrio (%)",
                          title_font_size=10)
        st.plotly_chart(fig2, use_container_width=True, key="paper_fig2")

        # ---- TABLA 6 — z-tests cross-provider -----------------------------
        st.markdown("---")
        st.subheader("Tabla 6 — z-tests pareados de $p_A$ (4:4:4 clean, Default)")
        st.caption(
            "Dos proporciones, corrección Holm-Bonferroni (6 comparaciones). "
            "*** = significativo tras corrección."
        )
        zt_models = {
            "Claude 4.6":   _rec("anthropic_sonnet46_default_75", "444", False),
            "G2.5 Flash":   _rec("gemini_25_flash_default_75",    "444", False),
            "G3.1 Pro":     _rec("gemini_31_pro_default_75",      "444", False),
            "GPT-5.4 Mini": _rec("openai_gpt54mini_default_75",   "444", False),
        }
        zt_names = list(zt_models)
        zt_x = {k: int(v.get("Aggressive", 0)) for k, v in zt_models.items()}
        zt_pairs = []
        for i in range(len(zt_names)):
            for j in range(i + 1, len(zt_names)):
                a, b = zt_names[i], zt_names[j]
                z, p = _z_test_prop(zt_x[a], zt_x[b])
                zt_pairs.append([a, b, zt_x[a], zt_x[b], z, p])
        zt_pairs.sort(key=lambda r: r[5])
        k_tests = len(zt_pairs)
        t6_rows = []
        for rank, (a, b, xa, xb, z, p) in enumerate(zt_pairs):
            thr = 0.05 / (k_tests - rank)
            t6_rows.append({
                "Modelo A": f"{a} ({round(100*xa/500)}%)",
                "Modelo B": f"{b} ({round(100*xb/500)}%)",
                "z": f"{z:+.2f}",
                "p": f"{p:.2e}",
                "HB α": f"{thr:.4f}",
                "Sig.": "***" if p < thr else "ns",
            })
        t6_df = pd.DataFrame(t6_rows)
        st.dataframe(t6_df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Descargar Tabla 6 (CSV)",
            t6_df.to_csv(index=False).encode("utf8"),
            "tabla6_ztests_n500.csv", "text/csv", key="dl_t6",
        )

        # ---- TABLA 8 — Sensibilidad al ruido Δnoise -----------------------
        st.markdown("---")
        st.subheader("Tabla 8 — Sensibilidad al ruido $\\Delta_{noise}$ (4:4:4)")
        st.caption(
            "Δnoise = %C(clean) − %C(noise). Positivo = degradación del "
            "equilibrio cooperativo bajo ruido. Filas † = referencia Willis et al."
        )
        import numpy as _np
        t8_rows = []
        for model in ["Claude 4.6", "Gemini 2.5 Flash",
                      "Gemini 3.1 Pro", "GPT-5.4 Mini"]:
            ds = []
            for algo, m, prompt in PAPER_ALGOS:
                if m != model:
                    continue
                cl = _rec(algo, "444", False).get("pct_Cooperative", 0)
                no = _rec(algo, "444", True).get("pct_Cooperative", 0)
                ds.append(cl - no)
            t8_rows.append({
                "Modelo": model,
                "Default": round(ds[0]), "Prose": round(ds[1]),
                "Refine": round(ds[2]), "Avg.": round(float(_np.mean(ds))),
            })
        for model, vals in PAPER_WILLIS_DNOISE.items():
            t8_rows.append({
                "Modelo": f"{model} †",
                "Default": vals[0], "Prose": vals[1],
                "Refine": vals[2], "Avg.": vals[3],
            })
        t8_df = pd.DataFrame(t8_rows)
        st.dataframe(t8_df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Descargar Tabla 8 (CSV)",
            t8_df.to_csv(index=False).encode("utf8"),
            "tabla8_noise_sensitivity_n500.csv", "text/csv", key="dl_t8",
        )

        st.markdown("---")
        st.info(
            "💡 Estos paneles se regeneran automáticamente del JSON n=500. "
            "Para reproducir los números exactos del paper: "
            "`cd paper && python analysis_h3_h4_entropy.py`."
        )


# ===========================================================================
# PESTAÑA 6: EXPORTAR RESULTADOS
# ===========================================================================
with tab_export:
    st.header("Exportar Resultados")
    st.markdown(
        "Descarga los resultados de los experimentos en formato CSV para análisis externo."
    )

    export_available = list_available_experiments()

    if not export_available and not st.session_state.get("moran_winner_counts"):
        st.info(
            "No hay datos para exportar. "
            "Ejecuta un torneo o una simulación Moran primero."
        )
    else:
        col_e1, col_e2 = st.columns(2)

        # --- Exportar resultados de torneo (matrices) ---
        with col_e1:
            st.subheader("Resultados de Torneo (Head-to-head)")
            if not export_available:
                st.info("No hay archivos de resultados de torneo.")
            else:
                exp_export = st.selectbox(
                    "Experimento a exportar",
                    export_available,
                    format_func=module_display_name,
                    key="export_exp_sel",
                )
                exp_path = RESULTS_DIR / f"{exp_export}_matrices.txt"
                coop_ex, pay_ex, sum_ex = parse_matrices_txt(exp_path)

                if not sum_ex.empty:
                    csv_summary = sum_ex.to_csv(index=True).encode("utf-8")
                    st.download_button(
                        label="⬇ Tabla de clasificación (CSV)",
                        data=csv_summary,
                        file_name=f"{exp_export}_clasificacion.csv",
                        mime="text/csv",
                        key="dl_summary",
                    )

                if not coop_ex.empty:
                    csv_coop = coop_ex.to_csv(index=True).encode("utf-8")
                    st.download_button(
                        label="⬇ Matriz de cooperación (CSV)",
                        data=csv_coop,
                        file_name=f"{exp_export}_cooperacion.csv",
                        mime="text/csv",
                        key="dl_coop",
                    )

                if not pay_ex.empty:
                    csv_pay = pay_ex.to_csv(index=True).encode("utf-8")
                    st.download_button(
                        label="⬇ Matriz de pagos (CSV)",
                        data=csv_pay,
                        file_name=f"{exp_export}_pagos.csv",
                        mime="text/csv",
                        key="dl_pay",
                    )

                # Exportar comparación entre todos los experimentos disponibles
                if len(export_available) >= 2:
                    st.markdown("---")
                    st.subheader("Comparación global entre modelos")
                    all_rows = []
                    for exp in export_available:
                        mpath = RESULTS_DIR / f"{exp}_matrices.txt"
                        _, _, sdf = parse_matrices_txt(mpath)
                        if sdf.empty:
                            continue
                        name_c = "Name" if "Name" in sdf.columns else sdf.columns[0]
                        score_c = (
                            "Median_score" if "Median_score" in sdf.columns else None
                        )
                        coop_c = (
                            "Cooperation_rating"
                            if "Cooperation_rating" in sdf.columns
                            else None
                        )
                        if not score_c:
                            continue
                        for att in ["Aggressive", "Cooperative", "Neutral"]:
                            subset = sdf[sdf[name_c].str.startswith(att)]
                            if not subset.empty:
                                row = {
                                    "Experimento": exp,
                                    "Modelo": module_display_name(exp),
                                    "Actitud": att,
                                    "Puntaje_mediano": subset[score_c].median(),
                                    "Puntaje_media": subset[score_c].mean(),
                                }
                                if coop_c:
                                    row["Cooperacion_media"] = subset[coop_c].mean()
                                all_rows.append(row)

                    if all_rows:
                        all_df = pd.DataFrame(all_rows)
                        csv_all = all_df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            label="⬇ Comparación de todos los modelos (CSV)",
                            data=csv_all,
                            file_name="evollm_comparacion_modelos.csv",
                            mime="text/csv",
                            key="dl_all",
                        )
                        st.dataframe(all_df, use_container_width=True)

        # --- Exportar resultados de Moran ---
        with col_e2:
            st.subheader("Resultados de Simulación Moran")

            moran_exps = list_moran_experiments()
            moran_hist_exp = load_moran_history()

            if not moran_exps and not moran_hist_exp.empty is False:
                st.info(
                    "No hay resultados de simulación Moran guardados. "
                    "Ejecuta una simulación en la pestaña 🔁 Simulación Moran."
                )
            else:
                # Exportar resultado individual de un módulo
                if moran_exps:
                    exp_moran_sel = st.selectbox(
                        "Módulo a exportar",
                        moran_exps,
                        format_func=module_display_name,
                        key="export_moran_sel",
                    )
                    moran_counts_file = load_moran_latest(exp_moran_sel)
                    if moran_counts_file:
                        total_m = sum(moran_counts_file.values())
                        moran_rows = [
                            {
                                "Actitud": name,
                                "Actitud_es": ATTITUDE_LABELS.get(name, name),
                                "Victorias": count,
                                "Porcentaje": round(100 * count / total_m, 2) if total_m else 0,
                            }
                            for name, count in sorted(
                                moran_counts_file.items(), key=lambda x: -x[1]
                            )
                        ]
                        moran_df = pd.DataFrame(moran_rows)
                        st.dataframe(moran_df, use_container_width=True)

                        st.download_button(
                            label="⬇ Último resultado Moran (CSV)",
                            data=moran_df.to_csv(index=False).encode("utf-8"),
                            file_name=f"{exp_moran_sel}_moran.csv",
                            mime="text/csv",
                            key="dl_moran_latest",
                        )
                        st.plotly_chart(
                            make_winner_bar(moran_counts_file),
                            use_container_width=True,
                            key="export_moran_bar",
                        )

                # Exportar historial completo
                if not moran_hist_exp.empty:
                    st.markdown("---")
                    st.caption(f"Historial acumulado: **{len(moran_hist_exp)} ejecuciones** guardadas.")
                    st.download_button(
                        label="⬇ Historial completo de simulaciones Moran (CSV)",
                        data=moran_hist_exp.to_csv(index=False).encode("utf-8"),
                        file_name="moran_history.csv",
                        mime="text/csv",
                        key="dl_moran_history",
                    )
                    st.dataframe(moran_hist_exp, use_container_width=True, height=300)
