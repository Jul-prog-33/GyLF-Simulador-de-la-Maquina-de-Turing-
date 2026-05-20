# Manual de usuario

## Instalación

Crear entorno virtual e instalar dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Aplicar migraciones:

```bash
python manage.py migrate
```

Opcionalmente cargar las máquinas de ejemplo:

```bash
python manage.py load_sample_machines
```

Iniciar servidor:

```bash
python manage.py runserver
```

Entrar a:

```txt
http://127.0.0.1:8000/
```

## Cargar una Máquina de Turing

En la página inicial, usar el formulario “Cargar máquina”. Seleccionar un archivo `.mt`, escribir un nombre opcional y presionar “Cargar archivo .mt”.

Si el archivo tiene errores formales, la interfaz muestra el mensaje correspondiente.

## Simular una cadena

Abrir una máquina cargada desde el listado. En el formulario “Ejecutar cadena”, escribir la entrada y el límite de pasos. Presionar “Iniciar simulación”.

La pantalla de ejecución muestra:

- Estado actual.
- Resultado.
- Número de pasos.
- Cinta visible.
- Posición del cabezal.
- Historial reciente.

## Modos de ejecución

- “Paso a paso”: ejecuta una única transición.
- “Ejecutar completa”: avanza hasta aceptar, rechazar o llegar al límite de pasos.
- “Reiniciar”: crea una nueva ejecución con la misma entrada y límite.

## Máquinas de ejemplo

La carpeta `machines/` incluye archivos listos para cargar:

- `0n1n.mt`
- `palindromo_binario.mt`
- `duplica_unos.mt`
- `termina_aa.mt`
- `duplica_binaria.mt`
- `suma_unaria.mt`
- `bucle_infinito.mt`
- `pin_4_digitos.mt`

## Recomendaciones

Usar símbolos separados por comas en alfabetos y transiciones. El símbolo blanco debe estar en el alfabeto de cinta y no debe estar en el alfabeto de entrada.
