# Documento Técnico - Simulador de Máquina de Turing

## 1. Introducción y Objetivos

### 1.1 Propósito del Proyecto

El Simulador de Máquina de Turing es una aplicación web académica desarrollada en Python con el framework Django, diseñada para que estudiantes y profesionales puedan comprender el funcionamiento de las Máquinas de Turing (MT). Una Máquina de Turing es un modelo abstracto de computación fundamental en teoría de la computación que permite analizar la computabilidad y resolver problemas de decisión.

El simulador proporciona una interfaz visual intuitiva que permite:
- Cargar definiciones de máquinas de Turing desde archivos `.mt`
- Validar la sintaxis y semántica de las definiciones
- Ejecutar cadenas de entrada paso a paso
- Visualizar el estado de la cinta, cabezal y transiciones
- Registrar históricos de ejecución para posterior análisis

### 1.2 Objetivos Técnicos

1. **Validación robusta**: Garantizar que las máquinas cargadas sean válidas según la especificación formal
2. **Simulación precisa**: Implementar un motor de ejecución que respete fielmente el comportamiento de Máquinas de Turing deterministas
3. **Interfaz educativa**: Proporcionar visualización clara del estado interno durante la ejecución
4. **Persistencia de datos**: Mantener registro de máquinas cargadas y ejecuciones realizadas
5. **Extensibilidad**: Arquitectura modular que permita futuras mejoras

### 1.3 Tecnología Utilizada

- **Backend**: Python 3.10+ con Django 5.x
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5 semántico con CSS3 responsive
- **Arquitectura**: Patrón MTV (Model-Template-View)

---

## 2. Arquitectura General del Sistema

### 2.1 Estructura de Capas

El proyecto sigue una arquitectura de tres capas:

```
┌─────────────────────────────────────────────────┐
│          Capa de Presentación                   │
│  (Templates HTML + CSS Responsive)              │
├─────────────────────────────────────────────────┤
│          Capa de Lógica de Negocio              │
│  (Views, Forms, Engine, Parser)                 │
├─────────────────────────────────────────────────┤
│          Capa de Persistencia                   │
│  (Modelos Django + Base de Datos)               │
└─────────────────────────────────────────────────┘
```

### 2.2 Componentes Principales

La aplicación `simulator` está compuesta por los siguientes módulos:

| Módulo | Responsabilidad |
|--------|-----------------|
| `parser.py` | Análisis léxico y sintáctico de archivos `.mt` |
| `engine.py` | Motor de simulación y ejecución paso a paso |
| `models.py` | Modelos de datos ORM (TuringMachine, Execution) |
| `views.py` | Lógica de control y enrutamiento HTTP |
| `forms.py` | Formularios para entrada de usuario |
| `templates/` | Templates HTML para renderización |
| `static/css/` | Estilos CSS para interfaz responsiva |

### 2.3 Flujo de Datos

```
Archivo .mt
    ↓
[PARSER] → Validación sintáctica → ParsedMachine
    ↓
[PERSISTENCIA] → Guardar en BD → TuringMachine
    ↓
Usuario elige entrada
    ↓
[ENGINE] → Crear ejecución inicial
    ↓
[ENGINE] → Ejecutar paso a paso → Execution
    ↓
[VISUALIZACIÓN] → Mostrar estado actual
```

---

## 3. Componentes Principales

### 3.1 Parser (parser.py)

#### 3.1.1 Propósito

El parser transforma un archivo de texto en formato `.mt` a una estructura de datos Python que representa una Máquina de Turing válida. Realiza análisis sintáctico, validación semántica y detección de errores.

#### 3.1.2 Formato .mt

El formato `.mt` define una Máquina de Turing mediante:

```
Estados: q0,q1,q2,qf
Alfabeto_entrada: 0,1
Alfabeto_cinta: 0,1,B
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> q1,1,R
q1,1 -> q2,0,L
q2,B -> qf,B,S
```

**Componentes**:
- **Estados**: Conjunto de identificadores de estado (q0, q1, etc.)
- **Alfabeto de entrada**: Símbolos que puede recibir como entrada
- **Alfabeto de cinta**: Símbolos que pueden estar en la cinta (incluye blancos)
- **Estado inicial**: Estado en el que comienza la ejecución
- **Estados finales**: Estados de aceptación
- **Símbolo blanco**: Símbolo que representa celdas vacías
- **Transiciones**: Reglas de movimiento y transformación

#### 3.1.3 Proceso de Parsing

```python
def parse_mt(source, name="", description="") → ParsedMachine:
```

**Pasos**:

1. **Tokenización**: Se divide el archivo en líneas y se elimina:
   - Espacios en blanco
   - Comentarios (líneas que comienzan con `#`)

2. **Extracción de secciones**: Se identifican las 6 secciones obligatorias:
   - Estados, Alfabeto_entrada, Alfabeto_cinta, Inicial, Finales, Blanco

3. **Parsing de transiciones**: Se procesa cada línea de transición:
   - Formato: `q_i,symbol -> q_j,write_symbol,direction`
   - Direction: L (izquierda), R (derecha), S (sin movimiento)

4. **Validación semántica**: Se verifican:
   - Que el estado inicial pertenezca a Estados
   - Que todos los estados finales pertenezcan a Estados
   - Que el símbolo blanco pertenezca al alfabeto de cinta
   - Que alfabeto_entrada ⊆ alfabeto_cinta
   - Que no haya símbolo blanco en alfabeto_entrada
   - Que no haya transiciones duplicadas
   - Que todos los símbolos referenciados sean válidos

#### 3.1.4 Estructura de Datos Retornada

```python
@dataclass(frozen=True)
class ParsedMachine:
    name: str                    # Nombre de la máquina
    description: str             # Descripción opcional
    states: list                 # Lista de estados
    input_alphabet: list         # Alfabeto de entrada
    tape_alphabet: list          # Alfabeto de cinta
    initial_state: str           # Estado inicial
    final_states: list           # Estados finales
    blank_symbol: str            # Símbolo blanco
    transitions: dict            # Dict[state][symbol] = {next_state, write_symbol, direction}
    source: str                  # Código fuente original
```

Las transiciones se almacenan en una estructura anidada para acceso O(1):
```python
transitions = {
    "q0": {
        "0": {"next_state": "q1", "write_symbol": "1", "direction": "R"},
        "1": {"next_state": "q2", "write_symbol": "0", "direction": "L"}
    },
    "q1": {...}
}
```

#### 3.1.5 Manejo de Errores

La clase `MachineParseError` captura todos los errores de parsing:
- Líneas con formato inválido
- Campos obligatorios faltantes
- Símbolos no declarados
- Estados no declarados
- Transiciones duplicadas
- Valores inválidos (direcciones, etc.)

### 3.2 Motor de Simulación (engine.py)

#### 3.2.1 Propósito

El motor de simulación ejecuta una Máquina de Turing step-by-step (paso a paso), manteniendo el estado completo de la ejecución y permitiendo pausas, inspección del estado interno y análisis del histórico.

#### 3.2.2 Tokenización de Entrada

```python
@staticmethod
def _tokenize_input(machine, input_string) → list:
```

Convierte una cadena de entrada en una lista de símbolos. Soporta dos formatos:

**Formato 1: Separado por comas**
```
"0,1,0,1"  →  ["0", "1", "0", "1"]
```

**Formato 2: Compacto (sin separadores)**
```
"0101"     →  ["0", "1", "0", "1"]  (si alfabeto es {0, 1})
"aa0bb"    →  ["aa", "0", "bb"]    (si alfabeto es {aa, 0, bb})
```

El algoritmo para formato compacto:
1. Ordena símbolos del alfabeto por longitud (descendente) para evitar ambigüedades
2. Itera sobre la cadena, intentando hacer match con símbolos válidos
3. Valida que todos los símbolos encontrados pertenezcan al alfabeto

Errores detectados:
- Símbolos no pertenecientes al alfabeto de entrada
- Cadenas con caracteres no reconocibles

#### 3.2.3 Creación de Ejecución

```python
@classmethod
def create_execution(cls, machine, input_string, max_steps=100) → Execution:
```

**Proceso**:

1. Tokeniza la cadena de entrada
2. Crea la cinta inicial: `{0: symbol0, 1: symbol1, ...}`
3. Crea objeto `Execution` en la base de datos con:
   - Posición del cabezal = 0
   - Estado actual = estado_inicial
   - Pasos ejecutados = 0
   - Estado de ejecución = RUNNING

4. **Caso especial**: Si el estado inicial es final, marca como ACCEPTED inmediatamente
   (máquinas que aceptan la cadena vacía sin procesarla)

#### 3.2.4 Ejecución Paso a Paso

```python
def step() → Execution:
```

Ejecuta exactamente un paso de la máquina:

**Algoritmo**:

```
SI ejecución está terminada:
    RETORNAR ejecución

SI pasos >= max_pasos:
    MARCAR como TIMEOUT
    RETORNAR

SI estado_actual ∈ estados_finales:
    MARCAR como ACCEPTED
    RETORNAR

símbolo_leído = LEER(posición_cabezal)
transición = BUSCAR(estado_actual, símbolo_leído)

SI transición NO existe:
    MARCAR como REJECTED
    REGISTRAR en histórico
    RETORNAR

EJECUTAR transición:
    ESCRIBIR(posición_cabezal, símbolo_escrito)
    MOVER cabezal según dirección
    estado_actual = siguiente_estado
    pasos++
    REGISTRAR en histórico

SI estado_actual ∈ estados_finales:
    MARCAR como ACCEPTED
SI pasos >= max_pasos:
    MARCAR como TIMEOUT
```

#### 3.2.5 Representación de la Cinta

La cinta se implementa como diccionario donde las claves son posiciones (números enteros como strings):

```python
tape = {
    "0": "0",    # Posición 0 contiene "0"
    "1": "1",    # Posición 1 contiene "1"
    "2": "B",    # Posición 2 contiene símbolo blanco
    "-1": "0"    # También se puede expandir a la izquierda
}
```

**Ventajas**:
- Cinta potencialmente infinita (pero limitada por memoria)
- Acceso O(1) a cualquier celda
- Optimización: no almacenar símbolos blancos

**Métodos**:
- `_read(position)`: Retorna el símbolo en position (o blank si no existe)
- `_write(position, symbol)`: Escribe symbol en position (o elimina si es blanco)

#### 3.2.6 Visualización de la Cinta

```python
def visible_tape(padding=5) → list[TapeCell]:
```

Retorna solo las celdas relevantes rodeadas de contexto:

1. Calcula rango de celdas usadas (con símbolos no-blancos)
2. Incluye la posición del cabezal
3. Añade padding para contexto visual
4. Retorna objetos `TapeCell` con:
   - Índice
   - Símbolo actual
   - Si es la posición del cabezal

```python
def final_tape() → str:
```

Extrae solo la parte "útil" de la cinta (sin blancos al inicio/final):
- Encuentra min y max de posiciones no-blancas
- Retorna cadena con solo símbolos de ese rango

#### 3.2.7 Histórico de Ejecución

Cada paso registra en `execution.history`:

```python
{
    "step": 3,                    # Número de paso
    "state": "q0",                # Estado antes de transición
    "head": 2,                    # Posición del cabezal
    "read": "1",                  # Símbolo leído
    "transition": {               # Transición ejecutada (o None si rechazado)
        "next_state": "q1",
        "write_symbol": "0",
        "direction": "R"
    }
}
```

Se mantienen los últimos 100 pasos para no agotar memoria.

#### 3.2.8 Estados de Ejecución

Una ejecución puede estar en:

| Estado | Significado |
|--------|------------|
| RUNNING | Aún hay pasos por ejecutar |
| ACCEPTED | Alcanzó estado final |
| REJECTED | No hay transición disponible |
| TIMEOUT | Superó max_steps sin terminar |

### 3.3 Modelos de Datos (models.py)

#### 3.3.1 Modelo TuringMachine

```python
class TuringMachine(models.Model):
    name: CharField                # Nombre único
    description: TextField         # Descripción opcional
    states: JSONField             # Lista de estados
    input_alphabet: JSONField     # Lista de símbolos entrada
    tape_alphabet: JSONField      # Lista de símbolos cinta
    initial_state: CharField      # Estado inicial
    final_states: JSONField       # Lista de estados finales
    blank_symbol: CharField       # Símbolo blanco
    transitions: JSONField        # Dict de transiciones anidado
    source: TextField             # Código .mt original
    created_at: DateTimeField     # Timestamp de creación
```

**Relaciones**:
- Uno a muchos con `Execution`: Una máquina puede tener múltiples ejecuciones

**Métodos**:
- `get_absolute_url()`: URL de vista detallada

#### 3.3.2 Modelo Execution

```python
class Execution(models.Model):
    machine: ForeignKey           # Referencia a máquina
    input_string: CharField       # Cadena de entrada original
    tape: JSONField               # Estado actual de cinta
    head_position: IntegerField   # Posición del cabezal
    current_state: CharField      # Estado actual
    steps: PositiveIntegerField   # Pasos ejecutados
    max_steps: PositiveIntegerField  # Límite de pasos
    status: CharField             # RUNNING|ACCEPTED|REJECTED|TIMEOUT
    history: JSONField            # Histórico de pasos
    created_at: DateTimeField     # Timestamp creación
    updated_at: DateTimeField     # Timestamp última actualización
```

**Propiedad computada**:
- `is_finished`: True si status no es RUNNING

---

## 4. Flujo de Ejecución Completo

### 4.1 Cargar una Máquina

**Entrada**: Archivo `.mt` cargado por formulario

**Proceso en Vista `upload_machine`**:

```
1. Validar form (extensión .mt)
2. Leer archivo y decodificar UTF-8
3. Extraer nombre (del formulario o del nombre de archivo)
4. Parsear con parse_mt()
5. Crear objeto TuringMachine en BD
6. Redirigir a vista detallada
```

**Salida**: Máquina disponible para simulación

### 4.2 Ejecutar una Simulación

**Entrada**: Máquina seleccionada + cadena de entrada

**Proceso**:

```
1. Validar formulario de simulación
2. Tokenizar entrada
3. Crear Execution con TuringMachineSimulator.create_execution()
4. Si necesario, ejecutar pasos con simulator.step()
5. Mostrar estado actual en template
```

**Caso 1: Ver solo estado final**
```
→ simulator.run() ejecuta todos los pasos automáticamente
```

**Caso 2: Ejecución interactiva**
```
→ simulator.step() ejecuta un paso por solicitud HTTP
→ Usuario ve estado y presiona "Siguiente"
```

### 4.3 Visualizar Ejecución

**Datos mostrados**:

1. **Estado de máquina**:
   - Máquina actual
   - Cadena de entrada procesada
   - Estado actual

2. **Visualización de cinta**:
   - Celdas del rango visible
   - Resaltado de cabezal (color diferente)
   - Índices de posición

3. **Información de paso**:
   - Pasos ejecutados / Máximo
   - Símbolo leído
   - Transición ejecutada
   - Resultado (aceptado/rechazado/timeout)

4. **Histórico**:
   - Tabla con todos los pasos previos
   - Símbolos leídos y escritos
   - Estados visitados

---

## 5. Características Técnicas Avanzadas

### 5.1 Detección de Anomalías

Función `machine_diagnostics()` analiza máquinas cargadas para detectar:

**Símbolos inalcanzables**:
- Identifica símbolos en transiciones que no pueden generarse
- Ejemplo: Si entrada es {0,1} pero máquina escribe "X", si X no puede leerse desde entrada/blancos

**Algoritmo de alcanzabilidad**:
```
símbolos_alcanzables = entrada ∪ {blanco}
MIENTRAS cambios HAYAN ocurrido:
    POR CADA transición (q, read) → (q', write, dir):
        SI read ∈ símbolos_alcanzables Y write ∉ símbolos_alcanzables:
            AÑADIR write a símbolos_alcanzables
```

### 5.2 Manejo de Entrada Flexible

El motor soporta:

1. **Cadena vacía**: Representada como "" → máquina comienza con solo símbolo blanco
2. **Separadores de coma**: "0,1,0" → ["0", "1", "0"]
3. **Formato compacto**: "010" → depende del alfabeto
4. **Símbolos multi-carácter**: "aa0bb" → ["aa", "0", "bb"] (si son válidos)

### 5.3 Límite de Pasos

Previene infinitas loops:
- Parámetro configurable (1 a 100,000 pasos)
- Defecto: 100 pasos
- Si se alcanza sin terminar → TIMEOUT

### 5.4 Base de Datos

**SQLite para desarrollo**, pero código es agnóstico:
- Modelos ORM permiten fácil migración a PostgreSQL
- Queries optimizadas con `select_related()` para evitar N+1
- JSONField para estructuras complejas (transiciones, histórico)

### 5.5 Interfaz Responsiva

CSS Grid y Media Queries para:
- Desktop: 2 columnas lado a lado
- Tablet: Columnas apiladas
- Mobile: Cinta de simulación en scroll horizontal

---

## 6. Ejemplos de Máquinas Incluidas

### 6.1 Validación de Palíndromo Binario

Acepta cadenas que leen igual forward y backward: "101", "1001", etc.

**Lógica**:
1. Marca símbolos mientras se mueve derecha
2. Regresa e intenta hacer match
3. Si todo coincide → ACEPTADO

### 6.2 Duplicador de Binarios

Transforma entrada en: entrada#entrada

**Entrada**: "01" **Salida**: "01#01"

**Lógica**:
1. Copia entrada a la izquierda
2. Agrega separador #
3. Copia entrada nuevamente

### 6.3 Suma en Unario

Suma dos números representados en unario (palotes):
- "11#111" → "11111" (2 + 3 = 5)

---

## 7. Flujo de Desarrollo

### 7.1 Requisitos

```bash
pip install -r requirements.txt
```

### 7.2 Setup Inicial

```bash
python manage.py migrate           # Crear tablas
python manage.py load_sample_machines  # Cargar ejemplos
python manage.py runserver         # Servidor desarrollo
```

### 7.3 Testing

```bash
python manage.py test simulator    # Suite de 24 pruebas
```

Cubre:
- Parsing de máquinas válidas e inválidas
- Ejecución de todas las máquinas de ejemplo
- Edge cases: entrada vacía, límites de pasos, símbolos inválidos
- Validación de histórico y estados finales

---

## Conclusión

El Simulador de Máquina de Turing es un sistema robusto y educativo que implementa fielmente la teoría formal de computación. Su arquitectura modular, validación completa y interfaz intuitiva lo hacen ideal tanto para estudiantes como investigadores que necesiten comprender y experimentar con Máquinas de Turing deterministas.
