<<<<<<< HEAD
# Simulador de Máquina de Turing

Aplicación web académica construida con Python y Django para cargar, validar y ejecutar Máquinas de Turing deterministas descritas en archivos `.mt`.

El frontend usa únicamente HTML y CSS con formularios tradicionales. No hay JavaScript.

## Requisitos

- Python 3.10 o superior
- Django 5.x

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución local

```bash
python manage.py migrate
python manage.py load_sample_machines
python manage.py runserver
```

Abrir:

```txt
http://127.0.0.1:8000/
```

## Pruebas

```bash
python manage.py test
```

La suite incluye parser, validación semántica, ejecución paso a paso, cinta infinita, límite de pasos y las máquinas solicitadas en el documento del proyecto.

## Formato `.mt`

```txt
Estados: q0,qf
Alfabeto_entrada: 0,1
Alfabeto_cinta: 0,1,B
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> q0,0,R
q0,B -> qf,B,S
```

Cada transición tiene la forma:

```txt
estado_actual,símbolo_leído -> nuevo_estado,símbolo_escrito,movimiento
```

Los movimientos válidos son `L`, `R` y `S`.

## Máquinas incluidas

La carpeta `machines/` contiene:

- `0n1n.mt`
- `palindromo_binario.mt`
- `duplica_unos.mt`
- `termina_aa.mt`
- `duplica_binaria.mt`
- `suma_unaria.mt`
- `bucle_infinito.mt`
- `pin_4_digitos.mt`

## Estructura

```txt
turing_project/      configuración Django
simulator/           app principal
machines/            máquinas de prueba en formato .mt
docs/                documento técnico y manual de usuario
```

## Flujo de uso

1. Cargar un archivo `.mt` desde la página inicial.
2. Abrir el detalle de la máquina.
3. Ingresar una cadena y un límite de pasos.
4. Ejecutar paso a paso o ejecutar completa.
5. Revisar resultado, cinta, cabezal, estado actual e historial.
=======
# GyLF-Simulador-de-la-Maquina-de-Turing-
Trabajo Final de la materia de GyLF
>>>>>>> b5cd612cf841210911d9ea64a999332f4def684f
