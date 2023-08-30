from itertools import product

# Funcion que convierte la representacion clausal de la formula en lista a conjuntos de tuplas
def convert_to_tuples(formula_list):
    converted_list = []

    # Por cada sublista de la formula
    for sublist in formula_list:
        converted_set = set()
        # Por cada item de cada sublista
        for item in sublist:
            # Si esta negado, se extrae el signo '-' y su valor de verdad es falso
            if item.startswith('-'):
                variable = item[1:]  
                bool_value = False  
            # Si no, su valor de verdad es verdadero
            else:
                variable = item
                bool_value = True
            
            # Al conjunto de tuplas se le agrega la nueva tupla
            converted_set.add((variable, bool_value))

        # A la lista de conjuntos se le agrega el nuevo conjunto de tuplas
        converted_list.append(converted_set)

    # Se retorna el listado final de conjuntos de tuplas
    return converted_list


def brute_force(cnf):
    literals = set()
    for conj in cnf:
        for disj in conj:
            literals.add(disj[0])
 
    literals = list(literals)
    n = len(literals)
    for seq in product([True,False], repeat=n):
        a = set(zip(literals, seq))
        if all([bool(disj.intersection(a)) for disj in cnf]):
            return True, a
 
    return False, None

def dpll(cnf, assignments={}):
 
    if len(cnf) == 0:
        return True, assignments
 
    if any([len(c)==0 for c in cnf]):
        return False, None
 
    for c in cnf:
        for literal in c:
            l =literal[0]

 
    new_cnf = [c for c in cnf if (l, True) not in c]
    new_cnf = [c.difference({(l, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals
 
    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals
 
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
I = {'p': True} #Asignaciones parciales
resultado, asignacion = dpll(tuple_formula, I)
print(f"Algoritmo DPLL")
print(f"Formula booleana: {formula_str}")
print(f"Resultado: {resultado}")
print(f"Asignacion: {asignacion}")