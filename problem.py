import os

from generation_tool import GenerationTool
from job import JobMachine
from utils import generate_population, get_instance

iterations = 10

pop_size = 5
population = []

file = list(open(os.path.join("1024x32", "A.u_c_hihi")))

num_jobs, num_machines = int(file[0].split(' ')[0]), int(
    file[0].split(' ')[1])  # get_instance(0)

wt = [float(i) for i in file[1::]]

job_machine_time = JobMachine(num_jobs)
jm_count = 0
for n in range(num_jobs):
    for p in range(num_machines):
        job_machine_time.set_wt(p, n, wt[jm_count])
        jm_count += 1


for i in range(pop_size):
    population.append(generate_population(num_jobs, num_machines))

g = GenerationTool(num_jobs, num_machines, population, job_machine_time)

g.calculate_individual_worktime()

print(g.population_worktime)

g.first_gen()

for i in range(iterations):
    g.create_new_gen(i)

g.print_generations()
