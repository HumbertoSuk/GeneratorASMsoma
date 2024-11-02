# Generador de Árbol de Expresión

Este proyecto es una herramienta para visualizar y analizar expresiones matemáticas mediante árboles de expresión. La interfaz gráfica permite ingresar una expresión aritmética, calcular sus recorridos (notación polaca, inorden y posorden), visualizar el árbol de expresión y generar código ensamblador basado en la expresión ingresada.

## Características

- **Cálculo de recorridos**: Genera los recorridos en notación polaca, inorden y posorden de la expresión.
- **Visualización del árbol de expresión**: Muestra gráficamente el árbol de la expresión ingresada.
- **Generación de código ensamblador**: Convierte la expresión en código ensamblador básico que se guarda en un archivo `.asm`.

## Requisitos

Antes de ejecutar el programa, asegúrate de instalar las dependencias necesarias.

### Dependencias

- `networkx` - Para construir y manipular grafos (usado en la visualización del árbol).
- `matplotlib` - Para dibujar y mostrar el grafo del árbol de expresión.

Para instalar las dependencias, utiliza el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Para ejecuto el programa:

```bash
python main.py
```

El archivo ensamblador se guardará en la ruta especificada (C:/MASM/MASM611/BIN/example/NEWCODE.asm por defecto).

## Ejemplos de Expresiones

Aquí tienes algunos ejemplos de expresiones que puedes usar en el programa. Todos los ejemplos son sencillos y no incluyen operaciones de potencia.

### Operaciones Básicas:

- 3 + 5 \* 2
- 8 / 4 + 2
- 7 - 3 \* 2

### Uso de Paréntesis:

- (3 + 5) \* 2
- 4 \* (2 + 3) - 1
- (6 + 2) \* (5 - 3)

### Combinación de Operadores:

- 3 + 5 \* 2 - 4 / 2
- 2 + 3 \* 4 - 1
- (2 + 3) \* (4 - 1) + 6

## Como ejecutar el DosBox

- iniciamos DosBox y nos metemos a la siguiente direccion con el comando ml
- ml example\newcode.asm
- newcode.exe

Ejecutando este comando en terminar saldra el resultado de la expresion.
