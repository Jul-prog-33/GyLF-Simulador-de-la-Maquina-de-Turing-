# Simulador de Máquina de Turing

Aplicación web académica para cargar, validar y ejecutar Máquinas de Turing deterministas.
Desarrollada en Python + Django para la materia de **Gramáticas y Lenguajes Formales — UTP**.

---

## Requisitos

- Python 3.10 o superior
- Django 6.0.3
- Las demás dependencias están en `requirements.txt`

---

## Instalación y ejecución

```bash
# 1. Crear y activar entorno virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear la base de datos
python manage.py migrate

# 4. Iniciar el servidor
python manage.py runserver
```

Abrir en el navegador: `http://127.0.0.1:8000/`

---

## Cómo usar el simulador

1. **Cargar máquina** — Sube un archivo `.mt` o usa una de las máquinas de ejemplo ya cargadas.
2. **Abrir máquina** — Haz clic en *Abrir* para ver sus detalles.
3. **Iniciar simulación** — Ingresa una cadena de entrada y el límite máximo de pasos.
4. **Ejecutar** — Avanza paso a paso o ejecuta completa de una sola vez.
5. **Ver resultado** — El simulador muestra el estado final, la cinta con el cabezal y el historial.
6. **Reiniciar** — Resetea la ejecución e intenta con otra cadena sin recargar la máquina.

---

## Formato del archivo `.mt`

```
Estados: q0,q1,qf
Alfabeto_entrada: 0,1
Alfabeto_cinta: 0,1,B
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> q1,X,R
q1,1 -> q0,Y,L
q0,B -> qf,B,S
```

Cada transición sigue el formato:

```
estado_actual,símbolo_leído -> nuevo_estado,símbolo_escrito,movimiento
```

| Campo | Descripción |
|---|---|
| `estado_actual` | Estado desde el que se aplica la regla |
| `símbolo_leído` | Símbolo que el cabezal lee en la cinta |
| `nuevo_estado` | Estado al que transiciona la máquina |
| `símbolo_escrito` | Símbolo que se escribe en la cinta |
| `movimiento` | `L` izquierda · `R` derecha · `S` sin movimiento |

**Condiciones que el archivo debe cumplir:**
- El estado inicial debe estar declarado en `Estados`.
- Los estados finales deben estar declarados en `Estados`.
- El símbolo blanco debe estar en `Alfabeto_cinta` pero no en `Alfabeto_entrada`.
- El alfabeto de entrada debe ser subconjunto del alfabeto de cinta.
- No puede haber dos transiciones para el mismo par (estado, símbolo).

---

## Máquinas de ejemplo incluidas

| Archivo | Qué hace |
|---|---|
| `0n1n.mt` | Reconoce cadenas de la forma 0ⁿ1ⁿ |
| `palindromo_binario.mt` | Reconoce palíndromos binarios |
| `duplica_unos.mt` | Transforma 1ⁿ en 1²ⁿ |
| `duplica_binaria.mt` | Duplica una cadena binaria: w → w#w |
| `suma_unaria.mt` | Suma en unario: 1ⁿ#1ᵐ → 1ⁿ⁺ᵐ |
| `termina_aa.mt` | Reconoce cadenas sobre {a,b} que terminan en aa |
| `pin_4_digitos.mt` | Valida que la cadena tenga exactamente 4 dígitos |
| `bucle_infinito.mt` | Nunca termina — demuestra el problema de la parada |

---

## Ejecutar pruebas

```bash
python manage.py manage.py
```

24 pruebas que cubren parser, validación semántica, ejecución de todas las máquinas, casos borde y operaciones de la interfaz.

---

## Estructura del proyecto

```
Proyecto-Final-MT-GLF/
├── turing_project/       Configuración de Django
├── simulator/            App principal
│   ├── templates/        Plantillas HTML
│   ├── static/           CSS e imágenes
│   ├── parser.py         Lectura y validación de archivos .mt
│   ├── engine.py         Motor de simulación paso a paso
│   ├── models.py         Modelos de base de datos
│   ├── views.py          Vistas HTTP
│   └── tests.py          Suite de pruebas
└── machines/             Archivos .mt de ejemplo
```