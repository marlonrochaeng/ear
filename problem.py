from job import Job
from machine import Machine
from utils import get_instance, generate_population

iterations = 100

pop_size = 200
population = []

num_jobs, num_machines = get_instance(0)

jobs = [Job() for i in range(num_jobs)]

for i in range(pop_size):
    population.append(generate_population(num_jobs, num_machines))

#calcular makespan dos 200 individuos
#ordenar por makespan
#pegar os melhores 70%
#montar matriz
#fazer roleta
#gerar os proximos 30%
#fazer isso para as proximas iteracoes
#ver resultado