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



clausula = [{'p'}, {'-p'}]
resultado, asignacion = fuerza_bruta(clausula)
print(f"Clausula: {clausula}")
print("Resultado:", resultado)
print("Asignacion:", asignacion)