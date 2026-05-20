# Documento técnico

## Marco referencial

Una Máquina de Turing determinista se define como una 7-tupla:

```txt
M = (Q, Σ, Γ, δ, q0, B, F)
```

`Q` es el conjunto de estados, `Σ` el alfabeto de entrada, `Γ` el alfabeto de cinta, `δ` la función de transición, `q0` el estado inicial, `B` el símbolo blanco y `F` el conjunto de estados finales. Este proyecto implementa simulación determinista con aceptación por estado final.

## Arquitectura

El proyecto se divide en tres capas:

- Modelos Django para persistir máquinas y ejecuciones.
- Parser y motor de simulación en Python puro.
- Templates HTML y estilos CSS sin JavaScript.

`TuringMachine` almacena la definición formal de la máquina. `Execution` almacena una ejecución concreta: entrada, cinta, cabezal, estado actual, pasos, estado final e historial.

## Parser `.mt`

El parser lee archivos de texto plano con campos obligatorios:

- `Estados`
- `Alfabeto_entrada`
- `Alfabeto_cinta`
- `Inicial`
- `Finales`
- `Blanco`
- `Transiciones`

La validación comprueba que el blanco pertenezca al alfabeto de cinta, que el alfabeto de entrada esté contenido en el de cinta, que estados y símbolos existan, que las transiciones sean deterministas y que las direcciones sean `L`, `R` o `S`.

## Motor de simulación

La cinta se representa con un diccionario de posiciones enteras serializadas, lo que permite expansión infinita hacia izquierda y derecha sin errores de índice. Las celdas no almacenadas se leen como símbolo blanco.

Cada paso ejecuta:

```txt
δ(estado, símbolo) = (nuevo_estado, símbolo_escrito, movimiento)
```

Si el estado actual pertenece a `F`, la ejecución se acepta. Si no existe transición para el par leído, se rechaza. Si los pasos alcanzan el límite configurado, la ejecución queda como `no_termina`.

## Casos de prueba

La suite valida:

- Parser correcto e inválido.
- Lenguaje `0ⁿ1ⁿ`.
- Palíndromos binarios.
- Duplicación unaria.
- Lenguaje regular “termina en aa”.
- Duplicación binaria con separador `#`.
- Suma unaria.
- Bucle infinito por límite de pasos.
- Expansión de cinta.

## Resultados esperados

Las pruebas automatizadas se ejecutan con:

```bash
python manage.py test
```

El resultado esperado es una suite completa aprobada sin errores del sistema Django.
