# EvoLLM — Informe de Contexto del Proyecto
**Fecha de última actualización:** 2026-04-27  
**Propósito:** Documento de contexto para retomar el trabajo en una nueva conversación con Claude u otra IA.

---

## 1. ¿Qué es este proyecto?

Extensión del experimento publicado en el paper académico:
> *"Will Systems of LLM Agents Lead to Cooperation"* — AAMAS 2025

El experimento estudia si agentes basados en LLMs cooperan o traicionan en el **Dilema del Prisionero Iterado (IPD)**. Se usan tres actitudes: **Agresiva, Cooperativa y Neutral**. Se genera código Python que define estrategias de juego, y luego se simula su evolución con el **Proceso de Moran** y torneos usando la librería `axelrod`.

**Lo que se hizo:** extender el experimento añadiendo modelos LLM más modernos (abril 2026) y construir una interfaz gráfica web (Streamlit) para ejecutar y visualizar los experimentos sin usar la línea de comandos.

---

## 2. Entorno de ejecución

```
Máquina: Windows 11
Python: 3.14 en C:\Users\Francisco\AppData\Local\Python\pythoncore-3.14-64\
        (NO hay conda instalado — usar pip directamente)

Raíz del repositorio: D:\evollm\
Worktree activo:       D:\evollm\.claude\worktrees\stupefied-mclaren\
Rama git:              claude/stupefied-mclaren
```

**Para ejecutar la GUI:**
```bash
cd D:\evollm\.claude\worktrees\stupefied-mclaren
python -m streamlit run gui.py
```

**Para ejecutar scripts CLI** (siempre desde la raíz del worktree):
```bash
cd D:\evollm\.claude\worktrees\stupefied-mclaren
python src/evollm/moran_process.py --algo strategies/anthropic_sonnet46_default_75 --initial_pop 4 4 4 --iterations 100
python src/evollm/head_to_head.py --algo strategies/anthropic_sonnet46_default_75 --h2h
```

**Dependencias instaladas vía pip:**
```
axelrod, anthropic, openai, pandas, numpy, matplotlib,
streamlit, plotly, google-genai>=1.0, python-dotenv
```

---

## 3. Estructura de archivos

```
D:\evollm\.claude\worktrees\stupefied-mclaren\
├── src\evollm\
│   ├── llm_clients.py          <- Capa de abstracción LLM (OpenAI/Anthropic/Google)
│   ├── create_strategies.py    <- Genera estrategias llamando al LLM
│   ├── moran_process.py        <- Simula el Proceso de Moran
│   ├── head_to_head.py         <- Torneos axelrod
│   ├── algorithms.py           <- Carga archivos .py de estrategias
│   ├── common.py               <- Clases base: LLM_Strategy, juegos, update_score
│   └── prompts.py              <- Plantillas de prompts (default/prose/refine)
├── strategies\                 <- Archivos .py con estrategias generadas
├── results\                    <- CSV y TXT con resultados de simulaciones
├── gui.py                      <- Interfaz Streamlit (5 pestañas)
├── .env                        <- API keys (NO en git)
├── .env.example                <- Plantilla de API keys
└── CONTEXTO_PROYECTO.md        <- Este archivo
```

---

## 4. Arquitectura del código

### 4.1 `src/evollm/llm_clients.py`

Modulo central de abstraccion para llamar APIs. Contiene:

- **`MODEL_REGISTRY`**: mapea clave de registro -> `(provider, api_model_id)`

| Clave registro | Proveedor | Modelo API |
|---|---|---|
| `chatgpt-4o-latest` | openai | `chatgpt-4o-latest` |
| `claude-3-5-sonnet` | anthropic | `claude-3-5-sonnet-20240620` |
| `gpt-5.4-mini` | openai | `gpt-5.4-mini` |
| `claude-sonnet-4-6` | anthropic | `claude-sonnet-4-6` |
| `gemini-2.5-flash` | google | `gemini-2.5-flash` |
| `gemini-3.1-pro-preview` | google | `gemini-3.1-pro-preview` |

- **`load_api_keys()`**: llama `load_dotenv(override=True)` para cargar `.env`
- **`make_client(model_key)`**: construye el cliente apropiado segun proveedor
- **`get_response(client, system, messages, temp)`**: dispatcher central
- **Google SDK**: usa `from google import genai` (paquete `google-genai`), **NO** `google.generativeai`

### 4.2 `src/evollm/algorithms.py`

- **`load_algorithms(module_path, keep_top, keep_bottom)`**: carga clases del archivo .py
- **`create_classes(algos)`**: genera tres clases `StrategySampler` (Aggressive, Cooperative, Neutral)
- **`StrategySampler.strategy()`**: llama a la estrategia LLM seleccionada aleatoriamente.
  - **GUARD DOBLE**: envuelve la llamada en `try/except Exception` para capturar cualquier error de la estrategia LLM. Devuelve `axl.Action.D` como fallback.
  - Si la accion retornada no es `C` ni `D`, tambien devuelve `D` con WARNING.
  - El `__repr__` retorna `"LLM: Aggressive (ours)"` — esto es lo que usa `mp.winning_strategy_name`.

### 4.3 `src/evollm/moran_process.py`

- Simula el Proceso de Moran con `axl.MoranProcess`
- Cada iteracion (`run_moran_process`) esta envuelta en `try/except` — si falla, retorna `None` y se omite del conteo (la simulacion no se interrumpe)
- **Normaliza claves**: `mp.winning_strategy_name` retorna `"LLM: Aggressive (ours)"` -> se mapea a `"Aggressive"` usando `if att in name`
- **Guarda doble**:
  - `results/{algo}_moran.csv` — sobrescribe (ultimo resultado)
  - `results/moran_history.csv` — acumula (nunca borrar)

### 4.4 `src/evollm/common.py`

- **`update_score()`**: valida que las acciones sean `axl.Action.C/D` antes de llamar `game.score()`. Si no son validas, logua WARNING y hace `return` (skip seguro). Envuelto en `try/except (IndexError, TypeError, ValueError)`.
- **Juegos disponibles**: `Classic`, `PrisonersDilemma`, `Chicken`, `StagHunt`

### 4.5 `gui.py` — Interfaz Streamlit con 5 pestanas

| Pestana | Funcion |
|---|---|
| Generar Estrategias | Llama a `create_strategies.py` via subprocess. Configura modelo, n, temperatura, tipo de prompt. |
| Simulacion Moran | Ejecuta `moran_process.py`. Guarda CSV automaticamente. Muestra graficas de ganadores. |
| Torneo | Ejecuta `head_to_head.py`. Muestra heatmaps de cooperacion/pagos y ranking. |
| Dashboard Comparativo | Lee archivos de `results/` y compara experimentos. Muestra historial Moran acumulado. |
| Exportar | Descarga resultados en CSV. Incluye historial completo `moran_history.csv`. |

**Importante en gui.py:**
- La pestana Dashboard usa un **selectbox independiente** para experimentos Moran (no usa el mismo que Torneo, porque los nombres de archivo son diferentes)
- `make_winner_bar()` tiene guard contra `total=0` para evitar ZeroDivisionError

---

## 5. Estado actual de los archivos de estrategias

### Modelos nuevos (75 clases = 25 Agresivas + 25 Cooperativas + 25 Neutrales)

| Archivo | Clases | Estado |
|---|---|---|
| `anthropic_sonnet46_default_75.py` | 75 (A=25, C=25, N=25) | Completo |
| `anthropic_sonnet46_prose_75.py` | 75 (A=25, C=25, N=25) | Completo |
| `anthropic_sonnet46_refine_75.py` | 75 (A=25, C=25, N=25) | Completo |
| `gemini_25_flash_default_75.py` | 75 (A=25, C=25, N=25) | Completo |
| `gemini_25_flash_prose_75.py` | 75 (A=25, C=25, N=25) | Completo — bug `history.length` corregido en linea 845 |
| `gemini_25_flash_refine_75.py` | 75 (A=25, C=25, N=25) | Completo — 47 clases anadidas manualmente |
| `gemini_31_pro_default_75.py` | 75 (A=25, C=25, N=25) | Completo |
| `gemini_31_pro_prose_75.py` | 21 (A=7, C=7, N=7) | INCOMPLETO — faltan 54 clases |
| `gemini_31_pro_refine_75.py` | 7 (A=3, C=2, N=2) | INCOMPLETO — faltan 68 clases |
| `openai_gpt54mini_default_75.py` | 75 (A=25, C=25, N=25) | Completo |
| `openai_gpt54mini_prose_75.py` | 75 (A=25, C=25, N=25) | Completo |
| `openai_gpt54mini_refine_75.py` | 75 (A=25, C=25, N=25) | Completo |

### Modelos originales del paper (en `strategies/`)
`anthropic_default`, `anthropic_prose`, `anthropic_refine`, `anthropic_default_noise`, `anthropic_prose_noise`, `anthropic_refine_noise`, `openai_default`, `openai_prose`, `openai_refine`, `openai_default_noise`, `openai_prose_noise`, `openai_refine_noise` — todos completos.

---

## 6. Estado actual de los resultados

### Archivos en `results/`

**Torneos head-to-head** (archivos `_matrices.txt`): Solo existen para los **modelos del paper original**:
- `anthropic_default_matrices.txt`, `anthropic_default_noise_matrices.txt`
- `anthropic_prose_matrices.txt`, `anthropic_prose_noise_matrices.txt`
- `anthropic_refine_matrices.txt`, `anthropic_refine_noise_matrices.txt`
- `openai_default_matrices.txt`, `openai_default_noise_matrices.txt`
- `openai_prose_matrices.txt`, `openai_prose_noise_matrices.txt`
- `openai_refine_matrices.txt`, `openai_refine_noise_matrices.txt`

**Simulaciones Moran** (archivos `_moran.csv`): Existen algunos CSV de pruebas:
- `anthropic_sonnet46_default_75_moran.csv`
- `anthropic_sonnet46_prose_75_moran.csv`
- `anthropic_sonnet46_refine_75_moran.csv`
- `gemini_25_flash_default_75_moran.csv`
- `moran_history.csv` (historial acumulado)

**PENDIENTE**: Correr Moran y torneos para todos los archivos `_75.py` nuevos con resultados validos (las ejecuciones anteriores pueden haber tenido bugs que ya estan corregidos).

---

## 7. Bugs corregidos (ambas sesiones)

### Bug 1 — `None` en acciones (IndexError en axelrod)
**Causa:** Estrategias LLM sin `return` explicito devuelven `None`. `game.score((None, action))` retorna numpy array en lugar de tupla — `IndexError: index 1 is out of bounds`.
**Solucion:**
- `algorithms.py -> StrategySampler.strategy()`: envuelve la llamada en `try/except Exception` + guard `if action not in (C, D)` -> retorna `axl.Action.D`
- `common.py -> update_score()`: valida acciones antes de `game.score()` + `try/except (IndexError, TypeError, ValueError)`

### Bug 2 — Simulacion Moran se detiene sin guardar resultados
**Causa:** Estrategias con bugs (AttributeError, etc.) lanzaban excepcion dentro de `mp.play()` -> crash total -> nunca se llegaba al codigo de guardado CSV.
**Solucion:** `moran_process.py -> run_moran_process()` envuelta en `try/except Exception`. Retorna `None` si falla; el bucle principal filtra los `None` antes de contar ganadores. Imprime cuantas iteraciones fallaron.

### Bug 3 — Moran history mostraba 0% para todas las actitudes
**Causa:** `winner_counts` tenia claves `"LLM: Aggressive (ours)"` pero el codigo de normalizacion buscaba `"Aggressive"` exacto.
**Solucion:** `normalized_counts` usa `if att in name` (substring match) en lugar de comparacion exacta.

### Bug 4 — ZeroDivisionError en `make_winner_bar()` (gui.py)
**Causa:** `total = 0` cuando no hay victorias registradas.
**Solucion:** Condicional en f-string: `f"{v} ({100*v/total:.1f}%)" if total else f"{v} (0.0%)"`

### Bug 5 — Dashboard "No hay resultados Moran" aunque habia historial
**Causa:** El selectbox de experimentos Moran usaba nombres de archivos `_matrices.txt` (torneos), distintos a `_moran.csv`.
**Solucion:** Selectbox independiente en Dashboard que llama a `list_moran_experiments()` (busca `*_moran.csv` en `results/`).

### Bug 6 — `load_dotenv()` no sobreescribia variables vacias
**Causa:** Variables de entorno vacias en la shell bloqueaban la carga desde `.env`.
**Solucion:** `load_dotenv(override=True)` en `llm_clients.py`.

### Bug 7 — Caracteres Unicode de Gemini rompian el AST (Windows CP1252)
**Causa:** Gemini genera `->`, `>=`, `!=` con caracteres Unicode en codigo Python.
**Solucion:** `sanitize_unicode_operators()` en `create_strategies.py` convierte a ASCII antes del AST.

### Bug 8 — `ast.ExceptHandler` y `ast.Raise` rechazados por `is_safe_ast()`
**Causa:** El whitelist de nodos AST no los incluia.
**Solucion:** Anadidos a `allowed_nodes` en `create_strategies.py`.

### Bug 9 — Windows multiprocessing (PicklingError)
**Causa:** `multiprocessing.Pool` no funciona bien en Windows con objetos axelrod.
**Solucion:** Modo secuencial en Moran (`processes=1`); `processes=None` en torneos.

### Bug 10 — `np.iinfo(np.uint32).max` desbordaba int32
**Causa:** Seeds aleatorias usaban `uint32.max` que excede el rango `int32`.
**Solucion:** Cambiado a `np.iinfo(np.int32).max`.

### Bug 11 — `AttributeError: 'History' object has no attribute 'length'`
**Causa:** Gemini genero `self.history.length` que no existe en axelrod. Lo correcto es `len(self.history)`.
**Solucion:** Corregido en `gemini_25_flash_prose_75.py` linea 845.

---

## 8. Convenciones de nomenclatura

### Archivos de estrategias
```
{proveedor}_{modelo}_{tipo_prompt}_{n_estrategias}.py
```
Ejemplos:
- `anthropic_sonnet46_default_75.py` -> Claude Sonnet 4.6, prompt directo, 75 estrategias
- `gemini_25_flash_refine_75.py` -> Gemini 2.5 Flash, prompt refinado, 75 estrategias
- `openai_gpt54mini_prose_75.py` -> GPT-5.4 Mini, prompt prosa, 75 estrategias

### Tipos de prompt
- `default` — el LLM recibe directamente el dilema del prisionero
- `prose` — se narra un escenario real (negocio, ciencia) que el LLM mapea a IPD
- `refine` — el LLM genera, luego critica su propia estrategia y la reescribe

### Clases dentro de cada archivo de estrategia
```python
class Aggressive_1(LLM_Strategy): ...
class Cooperative_1(LLM_Strategy): ...
class Neutral_1(LLM_Strategy): ...
# ... hasta n=25
```

---

## 9. Comandos utiles

### Generar estrategias (CLI)
```bash
cd D:\evollm\.claude\worktrees\stupefied-mclaren
python src/evollm/create_strategies.py \
    --strategy_llm anthropic \
    --model claude-sonnet-4-6 \
    --n 25 \
    --temp 0.7 \
    --algo strategies/anthropic_sonnet46_default_75
```

### Simular Moran (resultado valido con bugs corregidos)
```bash
python src/evollm/moran_process.py \
    --algo strategies/anthropic_sonnet46_default_75 \
    --initial_pop 4 4 4 \
    --iterations 100
```

### Torneo head-to-head entre actitudes LLM
```bash
python src/evollm/head_to_head.py \
    --algo strategies/anthropic_sonnet46_default_75 \
    --h2h
```

### Torneo Beaufils (LLM vs estrategias clasicas)
```bash
python src/evollm/head_to_head.py \
    --algo strategies/anthropic_sonnet46_default_75
```

---

## 10. Tareas pendientes

### Alta prioridad
1. **Completar archivos incompletos:**
   - `gemini_31_pro_prose_75.py` — tiene 21 clases (A=7, C=7, N=7), faltan 54. Necesita clases Aggressive_8 a 25, Cooperative_8 a 25, Neutral_8 a 25.
   - `gemini_31_pro_refine_75.py` — tiene 7 clases (A=3, C=2, N=2), faltan 68. Necesita Aggressive_4 a 25, Cooperative_3 a 25, Neutral_3 a 25.

2. **Re-ejecutar Moran para todos los archivos completos (con bugs ya corregidos):**
   Los CSVs existentes pueden tener resultados invalidos de ejecuciones anteriores con bugs.
   Archivos a simular:
   ```
   anthropic_sonnet46_default_75, anthropic_sonnet46_prose_75, anthropic_sonnet46_refine_75
   gemini_25_flash_default_75, gemini_25_flash_prose_75, gemini_25_flash_refine_75
   gemini_31_pro_default_75
   openai_gpt54mini_default_75, openai_gpt54mini_prose_75, openai_gpt54mini_refine_75
   ```

3. **Ejecutar torneos para todos los archivos `_75.py`:**
   No existe ningun `_matrices.txt` para los modelos nuevos.

### Baja prioridad
4. **Comparativa final:** Con Moran y torneos completos, el Dashboard puede comparar si los modelos nuevos (abril 2026) cooperan mas o menos que los del paper (2024).

---

## 11. Variables de entorno requeridas (`.env`)

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
```

El archivo `.env` esta en la raiz del worktree y no esta en git (`.gitignore`).

---

## 12. Notas criticas para el siguiente desarrollador

1. **NO hay conda** en esta maquina. Usar `python` (Python 3.14) directamente con pip. Activar entorno no es necesario.

2. **Windows**: Usar siempre `encoding='utf8'` al abrir archivos. Evitar `multiprocessing.Pool` — usar modo secuencial (`--processes 1` o sin flag).

3. **Google SDK**: Usar `from google import genai` (paquete `google-genai`), **NO** `import google.generativeai`. La API es completamente diferente.

4. **Gemini genera Unicode**: Las estrategias de Gemini pueden incluir caracteres Unicode en operadores. La funcion `sanitize_unicode_operators()` en `create_strategies.py` los convierte a ASCII antes del AST.

5. **Estrategias con bugs**: Algunas retornan `None` o lanzan excepciones. El guard en `algorithms.py -> StrategySampler.strategy()` las intercepta con `try/except` y devuelve `axl.Action.D`. Si ves warnings como `"raised AttributeError"` en el log, indica que esa estrategia tiene un bug en el codigo generado. La simulacion **NO se detiene** por esto.

6. **`mp.winning_strategy_name`** retorna `"LLM: Aggressive (ours)"` (el `__repr__` de `StrategySampler`), NO `"Aggressive"` suelto. El mapeo `if att in name` en `moran_process.py` maneja esta conversion.

7. **Moran guarda doble**: Cada simulacion actualiza `results/{algo}_moran.csv` (sobrescribe) Y anade una fila a `results/moran_history.csv` (acumula). **Nunca borrar `moran_history.csv` manualmente.**

8. **axelrod History**: El atributo correcto es `len(self.history)`. No existen `.length`, `.size`. Si existen `.defections` y `.cooperations` como propiedades.

9. **`create_strategies.py` tiene logging dual**: archivo `create_strategies.log` (INFO+) + consola (WARNING+). Los errores de estrategias individuales no cortan la generacion.

10. **Iteraciones Moran fallidas**: Si una iteracion falla (muy improbable con los bugs corregidos), `run_moran_process` retorna `None` y se filtra antes del conteo. Se imprime cuantas fallaron. El CSV se guarda igual con las iteraciones exitosas.
