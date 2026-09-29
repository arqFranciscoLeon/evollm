# Política local de correcciones de implementación v1

Fecha: 2026-09-14. Establecida después de observar errores de validación y antes del torneo; no es una prerregistración pública ni una política anterior a la conversión. El autor indicó continuar tras autorizar la tanda. No se realizan nuevas conversiones API.

La política se aplica por igual a todas las estrategias: un error de código puede corregirse solo cuando una regla operacional explícita de la prosa conservada determina el cambio, existe un contraejemplo reproducible y la corrección no agrega una regla. Una ambigüedad o una regla ausente requiere una decisión metodológica distinta; no se completa mediante este procedimiento.

Se conservan el código original, sus hashes y su validación fallida. La corrección vive en un archivo separado, con hash propio, diferencia exacta, vínculo a la solicitud original y comprobaciones repetidas. No se vuelve a consultar al modelo ni se elige una versión por su puntuación, cooperación, ranking o conveniencia para una hipótesis. Se informa la intervención humana/asistida en cualquier publicación que use estas versiones.

## Aplicaciones actuales

- **Sonnet Neutral_11, original 053:** mover la comprobación de la última defección después del disparador permanente de más del 55%, respetando el orden 1–2–3 de la prosa. No cambiar umbral, acción inicial ni naturaleza del estado.
- **Gemini Pro Aggressive_6, original 156:** sustituir únicamente `len(self.history) >= 995` por `len(self.history) + 1 >= 995`, porque la prosa nombra la ronda actual 995 inclusive.

Las nuevas versiones son candidatas derivadas, no salidas originales del conversor. Se repetirán los 19 escenarios y las 11 partidas de diagnóstico para cada una. El manifiesto derivado referenciará los otros 272 originales sin cambios y mantendrá esta procedencia diferenciada. Hasta completar esos checks no se aprueban las correcciones.
