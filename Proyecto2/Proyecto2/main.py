from itertools import product


def fuerza_bruta(clausulas):
    # Conjunto para almacenar las variables booleanas de la formula booleana
    variables = set()
    
    # Se itera por cada clausula para obtener las variables unicas
    for clausula in clausulas:
        for caracter in clausula:
            # Se elimina la negacion '-' si existe y se agrega la variable booleana
            variables.add(caracter.replace('-', ''))
    
    # Se generan todas las posibles asignaciones de verdad 
    for asignacion in product([True, False], repeat=len(variables)):
        # Se crea un diccionario para almacenar la asignacion actual
        asignacion_actual = {var: val for var, val in zip(variables, asignacion)}
        
        # Bandera que verifica si la formula es satisfacible con la asignacion actual
        satisfacible = True
        
        # Se itera por cada clausula para verifcar la satisfacibilidad
        for clausula in clausulas:
            # Bandera para verificar si la clausala actual es satisfacible
            clausula_satisfacible = False
            
            # Se itera por cada literal en la clausula
            for caracter in clausula:
                # Se obtiene el valor de verdad de la variable actual
                valor = asignacion_actual[caracter.replace('-', '')]
                
                # Si hay negacion de variable se invierte el valor de verdad
                if '-' in caracter:
                    valor = not valor
                
                # Se usa un or para verificar la satisfacibilidad
                clausula_satisfacible |= valor
            
            # Si no lo es, se acaba el ciclo y se asigna falso a la bandera
            if not clausula_satisfacible:
                satisfacible = False
                break
        
        # Si si lo es, se asigna verdadero a la bandera y se retorna la asignacion satisfactoria
        if satisfacible:
            return True, asignacion_actual
    
    # Solo pasa si no es satisfacible
    return False, {}



def DPLL(B, I):
    # Caso base: Si B esta vacio, la formula es satisfacible
    if not B:
        return True, I
    
    # Caso base: Si hay una disyuncion vacia en B, la formula es insatisfacible
    if any(len(clausula) == 0 for clausula in B):
        return False, {}

    # Seleccionar un literal L no asignado de B
    L = next(iter(B[0]))

    # Para literales negativos, se extrea el nombre de la variable sin el signo '-'
    variable = L[1:] if L.startswith('-') else L
    
    # Constuir B' eliminando clausulas que contienen L de las clausulas restantes
    B_pos = [clausula - {L} for clausula in B if L not in clausula]
    I_pos = I.copy()
    I_pos[variable] = not L.startswith('-')
    
    # Llamada recursiva con B' y asignacion actualizada I
    resultado, I1 = DPLL(B_pos, I_pos)
    if resultado:
        return True, I1
    
    # Construir B' eliminando clausulas que contienen -L de las clausulas restantes
    L_neg = '-' + variable if not L.startswith('-') else variable
    B_neg = [clausula - {L_neg} for clausula in B if L_neg not in clausula]
    I_neg = I.copy()
    I_neg[variable] = L.startswith('-')
    
    # Llamada recursiva con B' y asignacion actualizada I
    resultado, I2 = DPLL(B_neg, I_neg)
    if resultado:
        return True, I2
    
    # Si ambas llamadas recursivas devuelven Falso, la formula es insatisfacible
    return False, {}


clausula = [{'p'}, {'-q'}]


resultado, asignacion = fuerza_bruta(clausula)
print("Algoritmo de fuerza Bruta")
print(f"Clausula: {clausula}")
print(f"Resultado: {resultado}")
print(f"Asignacion: {asignacion}")

B = clausula
I = {'p':False, 'q':True}

resultado, asignacion = DPLL(B,I)
print(f"\nAlgoritmo DPLL")
print(f"Clausula: {clausula}")
print(f"Resultado: {resultado}")
print(f"Asignacion: {asignacion}")