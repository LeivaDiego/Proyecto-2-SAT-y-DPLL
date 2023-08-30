from itertools import product

# Funcion que convierte la representacion clausal de la formula en lista de sublistas
# a una lista de conjuntos de tuplas
def convert_to_tuples(formula_list):
    converted_list = []

    # Itera por cada sublista de la formula en formato de lista de sublistas
    for sublist in formula_list:
        converted_set = set()
        # Por cada item de la sublista verifica si esta negado o no
        for item in sublist:
            # Si esta negado se remueve el '-' y se asigna False
            if item.startswith('-'):
                variable = item[1:]
                bool_value = False
            # De lo contrario se asigna True
            else:
                variable = item
                bool_value = True

            # Se agrega la tupla al conjunto
            converted_set.add((variable, bool_value))

        # Se agrega el conjunto al listado
        converted_list.append(converted_set)

    return converted_list


# Funcion que implementa un algoritmo de fuerza bruta
# evalua todas las posibles asignaciones de valores de verdad
# para la cnf y prueba si cada conjunto de asignaciones
# satisface o no la formula
def brute_force(cnf):
    literals = set()

    # Se genera el listado de variables
    for conj in cnf:
        for disj in conj:
            literals.add(disj[0])

    literals = list(literals)
    n = len(literals)

    # Se verifica cada posible asignacion de valores de verdad
    for seq in product([True,False], repeat=n):
        a = set(zip(literals, seq))
        # Si con esa asignacion es satisfactible, se regresa True y la asignacion
        if all([bool(disj.intersection(a)) for disj in cnf]):
            return True, a

    # De lo contrario se regresa False y vacio
    return False, None


# Funcion que implementa el algoritmo DPLL
# algoritmo recursivo de backtracking utilizado para decidir la satisfacibilidad
# de formulas booleanas en la forma normal conjuntiva (CNF)
def dpll(B, I={}):
    # Primer caso base
    # Si B es vacia, entonces regresar True e I
    if len(B) == 0:
        return True, I

    # Si hay alguna disyuncion vacia en B,
    # entonces regresar False y asignacion vacia
    if any([len(c)==0 for c in B]):
        return False, None

    # L ← seleccionar literal(B) para poner en forma positiva
    for c in B:
        for literal in c:
            l = literal[0]

    # Elimine todas las clausulas que contiene la literal L en B y elimine
    # las ocurrencias en las clausulas de la literal complementaria de L en B,
    # construyendo B'
    new_B = [c for c in B if (l, True) not in c]
    new_B = [c.difference({(l, False)}) for c in new_B]

    # I' = I ∪ {valor de L es verdadero}
    # resultado e I1 ← DPLL(B', I')
    sat, vals = dpll(new_B, {**I, **{l: True}})
    # if resultado es verdadera, entonces regresar True e I1
    if sat:
        return sat, vals

    # Elimine todas las clausulas que contiene la literal complementaria L en B y elimine
    # las ocurrencias en las clausulas de la literal L en B, construyendo B'
    new_B = [c for c in B if (l, False) not in c]
    new_B = [c.difference({(l, True)}) for c in new_B]
    # I' = I ∪ {valor de L es falso}
    # resultado e I2 ← DPLL(B',I')
    sat, vals = dpll(new_B, {**I, **{l: False}})
    # if resultado es verdadero, entonces regresar True e I2
    if sat:
        return sat, vals

    # Regresar False y la asignacion vacia
    return False, None

# Reemplazo de {} por []
# pues los sets en python no tiene un orden predecible
formula = [['p'], ['-q']]
formula_str = str(formula).replace('[', '{').replace(']', '}')
tuple_formula = convert_to_tuples(formula)

# Algoritmo de fuerza bruta
resultado, asignacion = brute_force(tuple_formula)
print(f"Algoritmo de fuerza bruta")
print(f"Formula booleana: {formula_str}")
print(f"Resultado: {resultado}")
print(f"Asignacion: {asignacion}\n")

# Algoritmo DPLL
asignment = {'p': True} #Asignaciones parciales
resultado, asignacion = dpll(tuple_formula, asignment)
print(f"Algoritmo DPLL")
print(f"Formula booleana: {formula_str}")
print(f"Resultado: {resultado}")
print(f"Asignacion: {asignacion}")