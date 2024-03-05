import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la simulación
RANDOM_SEED = 42
MEMORIA_RAM = 100
VELOCIDAD_PROCESADOR = 3
NUM_PROCESOS = [25, 50, 100, 150, 200]
INTERVALOS = [10, 5, 1]

# Clase para la simulación del sistema
class Sistema:
    def __init__(self, env, ram, cpu):
        self.env = env
        self.ram = ram
        self.cpu = cpu

    def proceso(self, nombre, memoria, tiempo_proceso):
        yield self.env.timeout(tiempo_proceso)
        self.ram.put(memoria)

# Función para ejecutar la simulación
def simulacion(num_procesos, intervalo):
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    ram = simpy.Container(env, capacity=MEMORIA_RAM, init=MEMORIA_RAM)
    cpu = simpy.Resource(env, capacity=1)
    sistema = Sistema(env, ram, cpu)

    tiempos_proceso = []

    for i in range(num_procesos):
        memoria = random.randint(1, 10)
        tiempo_llegada = random.expovariate(1.0 / intervalo)
        env.process(sistema.proceso(f'Proceso {i}', memoria, VELOCIDAD_PROCESADOR))
        tiempos_proceso.append(tiempo_llegada)

    env.run()

    tiempo_promedio = np.mean(tiempos_proceso)
    desviacion_estandar = np.std(tiempos_proceso)

    return tiempo_promedio, desviacion_estandar

# Ejecutar la simulación con diferentes cantidades de procesos y intervalos
resultados = { }

for num_procesos in NUM_PROCESOS:
    tiempos_promedio = []
    desviaciones_estandar = []
    for intervalo in INTERVALOS:
        tiempo_promedio, desviacion_estandar = simulacion(num_procesos, intervalo)
        tiempos_promedio.append(tiempo_promedio)
        desviaciones_estandar.append(desviacion_estandar)
    resultados[(num_procesos, 'promedio')] = tiempos_promedio
    resultados[(num_procesos, 'desviacion_estandar')] = desviaciones_estandar

# Imprimir resultados
fig, ax = plt.subplots()

# Desempaquetar las claves
num_procesos_keys, metric_keys = zip(*resultados.keys())

# Representar el tiempo de procesamiento promedio
promedios_values = [val[1] for key, val in resultados.items() if 'promedio' in key]
ax.bar(num_procesos_keys[::2], promedios_values)
ax.set_xlabel('Número de procesos')
ax.set_ylabel('Tiempo promedio')
ax.set_title('Número de Procesos vs Tiempo Promedio')
plt.show()