import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# === Módulo de Nodos y Árbol de Expresiones ===


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def get_precedence(op):
    precedences = {'-': 1, '+': 1, '/': 2, '*': 2, '^': 3}
    return precedences.get(op)


def is_variable_or_number(char):
    return char.isdigit() or char.isalpha()


def construct_expression_tree(expression):
    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        node = Node(operator)
        node.left = left
        node.right = right
        values.append(node)

    operators, values = [], []
    i = 0
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        if expression[i] == '(':
            operators.append(expression[i])
        elif is_variable_or_number(expression[i]):
            token = []
            while i < len(expression) and is_variable_or_number(expression[i]):
                token.append(expression[i])
                i += 1
            values.append(Node(''.join(token)))
            continue
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()
        else:
            while (operators and operators[-1] != '(' and get_precedence(operators[-1]) >= get_precedence(expression[i])):
                apply_operator(operators, values)
            operators.append(expression[i])
        i += 1
    while operators:
        apply_operator(operators, values)
    return values[0]

# === Módulo de Recorridos en el Árbol ===


def notacion_polaca(nodo):
    if nodo is None:
        return ""
    return str(nodo.value) + (f" {notacion_polaca(nodo.left)}" if nodo.left else "") + (f" {notacion_polaca(nodo.right)}" if nodo.right else "")


def inorder(nodo):
    if nodo is None:
        return ""
    return (f"{inorder(nodo.left)} " if nodo.left else "") + str(nodo.value) + (f" {inorder(nodo.right)}" if nodo.right else "")


def posorder(nodo):
    if nodo is None:
        return ""
    return (f"{posorder(nodo.left)} " if nodo.left else "") + (f"{posorder(nodo.right)} " if nodo.right else "") + str(nodo.value)

# === Módulo de Grafo y Visualización ===


def build_graph(graph, node, node_id_map):
    if node:
        node_id = id(node)
        node_id_map[node_id] = node.value
        if node.left:
            left_id = id(node.left)
            graph.add_edge(node_id, left_id)
            build_graph(graph, node.left, node_id_map)
        if node.right:
            right_id = id(node.right)
            graph.add_edge(node_id, right_id)
            build_graph(graph, node.right, node_id_map)


def hierarchy_pos(graph, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=None):
    if pos is None:
        pos = {}
    if parsed is None:
        parsed = set()

    if root not in parsed:
        parsed.add(root)
        neighbors = list(graph.neighbors(root))
        if parent:
            neighbors.remove(parent)
        if neighbors:
            dx = width / 2
            nextx = xcenter - width / 2 - dx / 2
            for neighbor in neighbors:
                nextx += dx
                pos = hierarchy_pos(graph, neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc -
                                    vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
        pos[root] = (xcenter, vert_loc)
    return pos


def display_expression_tree(root):
    G = nx.Graph()
    node_id_map = {}
    build_graph(G, root, node_id_map)
    pos = hierarchy_pos(G, id(root))
    labels = {node_id: node_value for node_id,
              node_value in node_id_map.items()}
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000,
            node_color="#DDA0DD", font_size=10, font_weight="bold", edge_color="purple")
    plt.show()

# === Módulo de Validación y Generación de Código ===


def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_values(expression):
    for element in expression:
        if element not in ['-', '+', '/', '*', '^'] and not is_number(element):
            messagebox.showwarning(
                'Error', f'La expresión {expression} incluye variables, por lo que no se puede generar código ensamblador a partir de ella')
            return
    return generate_code(expression)


def generate_code(expression):
    stack, code = [], []
    temp_var_counter = 0

    code.extend([".model small", ".stack 100h", ".data"])

    def new_temp_var():
        nonlocal temp_var_counter
        var_name = f"TEMP{temp_var_counter} DW ?"
        temp_var_counter += 1
        return var_name

    for _ in expression:
        code.append(new_temp_var())

    code.append(".code")
    code.append("main proc")

    temp_var_counter = 0
    for token in expression:
        if token.isdigit():
            temp_var = f"TEMP{temp_var_counter}"
            code.append(f'MOV {temp_var}, {token}')
            stack.append(temp_var)
            temp_var_counter += 1
        else:
            if len(stack) >= 2:
                reg2 = stack.pop()
                reg1 = stack.pop()
                temp_var = f"TEMP{temp_var_counter}"
                temp_var_counter += 1

                if token == '+':
                    code.extend(
                        [f'MOV AX, {reg1}', f'ADD AX, {reg2}', f'MOV {temp_var}, AX'])
                elif token == '-':
                    code.extend(
                        [f'MOV AX, {reg1}', f'SUB AX, {reg2}', f'MOV {temp_var}, AX'])
                elif token == '*':
                    code.extend(
                        [f'MOV AX, {reg1}', f'IMUL {reg2}', f'MOV {temp_var}, AX'])
                elif token == '/':
                    code.extend(
                        [f'MOV AX, {reg1}', f'IDIV {reg2}', f'MOV {temp_var}, AX'])
                stack.append(temp_var)

    code.append('''MOV BX, 10
XOR CX, CX
CONVERT:
    XOR DX, DX
    DIV BX
    ADD DL, '0'
    PUSH DX
    INC CX
    TEST AX, AX
    JNZ CONVERT

PRINT_DIGITS:
    POP DX
    MOV AH, 02h
    INT 21h
    LOOP PRINT_DIGITS

    MOV AH, 4Ch
    INT 21h''')

    code.extend(["main endp", "end main"])
    return code


def save_code(code):
    with open('C:/MASM/MASM611/BIN/example/NEWCODE.asm', 'w') as f:
        f.write('\n'.join(code))
    messagebox.showinfo(
        'Código Generado', 'El código ha sido generado y guardado en C:/MASM/MASM611/BIN/example/NEWCODE.asm')

# === Módulo de Interfaz de Usuario ===


def main():
    root = tk.Tk()
    root.title("Generador de Árbol de Expresión")
    root.geometry("600x500")
    root.config(bg="#333333")

    # Estilos
    label_style = {"font": ("Arial", 12, "bold"),
                   "bg": "#333333", "fg": "#FFFFFF"}
    entry_style = {"font": ("Arial", 14), "bg": "#FFFFFF",
                   "fg": "#000000", "justify": "center"}
    button_style = {"font": ("Arial", 12, "bold"), "bg": "#5A5A5A", "fg": "#FFFFFF",
                    "activebackground": "#666666", "width": 20, "height": 2}

    # Entrada de expresión y botón de cálculo alineados
    input_frame = tk.Frame(root, bg="#333333")
    input_frame.pack(pady=10)

    expression_entry = tk.Entry(input_frame, width=30, **entry_style)
    expression_entry.grid(row=0, column=0, padx=(0, 10))

    calculate_button = tk.Button(input_frame, text="Calcular Recorridos",
                                 command=lambda: calculate_traversals(expression_entry.get()), **button_style)
    calculate_button.grid(row=0, column=1)

    # Campo de texto para mostrar resultados de recorridos
    traversal_frame = tk.Frame(root, bg="#333333")
    traversal_frame.pack(pady=10)

    # Notación Polaca (No editable)
    tk.Label(traversal_frame, text="Notación Polaca:", **
             label_style).grid(row=0, column=0, sticky="e")
    polaca_entry = tk.Entry(traversal_frame, width=40,
                            **entry_style, state="readonly")
    polaca_entry.grid(row=0, column=1, pady=5)

    # Inorden (No editable)
    tk.Label(traversal_frame, text="Recorrido Inorden:", **
             label_style).grid(row=1, column=0, sticky="e")
    inorden_entry = tk.Entry(traversal_frame, width=40,
                             **entry_style, state="readonly")
    inorden_entry.grid(row=1, column=1, pady=5)

    # Posorden (No editable)
    tk.Label(traversal_frame, text="Recorrido Posorden:", **
             label_style).grid(row=2, column=0, sticky="e")
    posorden_entry = tk.Entry(
        traversal_frame, width=40, **entry_style, state="readonly")
    posorden_entry.grid(row=2, column=1, pady=5)

    # Función para calcular y mostrar los recorridos
    def calculate_traversals(expression):
        expression = expression.strip()
        if expression:
            tree_root = construct_expression_tree(expression)
            polaca_entry.config(state="normal")
            polaca_entry.delete(0, tk.END)
            polaca_entry.insert(0, notacion_polaca(tree_root))
            polaca_entry.config(state="readonly")

            inorden_entry.config(state="normal")
            inorden_entry.delete(0, tk.END)
            inorden_entry.insert(0, inorder(tree_root))
            inorden_entry.config(state="readonly")

            posorden_entry.config(state="normal")
            posorden_entry.delete(0, tk.END)
            posorden_entry.insert(0, posorder(tree_root))
            posorden_entry.config(state="readonly")
        else:
            messagebox.showinfo(
                "Error", "No se ha proporcionado una expresión")

    # Botón para generar el árbol
    tree_button = tk.Button(root, text="Generar Árbol", command=lambda: generate_tree(
        expression_entry.get()), **button_style)
    tree_button.pack(pady=10)

    # Botón para generar el código ensamblador
    code_button = tk.Button(root, text="Generar Código ASM", command=lambda: generate_asm_code(
        expression_entry.get()), **button_style)
    code_button.pack(pady=10)

    root.mainloop()

# Funciones de generación de árbol y código ensamblador


def generate_tree(expression):
    if expression:
        tree_root = construct_expression_tree(expression.strip())
        display_expression_tree(tree_root)
    else:
        messagebox.showinfo("Error", "No se ha proporcionado una expresión")


def generate_asm_code(expression):
    if expression:
        code = validate_values(
            posorder(construct_expression_tree(expression.strip())).split())
        if code:
            save_code(code)
    else:
        messagebox.showinfo("Error", "No se ha proporcionado una expresión")


if __name__ == "__main__":
    main()
