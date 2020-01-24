import os

from generation_tool import GenerationTool
from job import JobMachine
from utils import generate_population, get_files, get_instance

"""
change this file and get_files to 512, 2048, etc
"""

iterations = [10,  50, 100, 200, 300, 400, 500, 1000]

pop_size = [5, 10, 50, 100, 250, 500, 600, 750, 1000]

files = get_files()

for file_name in files:

    file = list(open(os.path.join("1024x32", file_name)))
    num_jobs, num_machines = int(file[0].split(' ')[0]), int(
        file[0].split(' ')[1])

    wt = [float(i) for i in file[1::]]

    job_machine_time = JobMachine(num_jobs)
    jm_count = 0
    for n in range(num_jobs):
        for p in range(num_machines):
            job_machine_time.set_wt(p, n, wt[jm_count])
            jm_count += 1

    for iteration in iterations:
        for pop in pop_size:
            population = []
            for i in range(pop):
                population.append(generate_population(num_jobs, num_machines))
            print("Population\n", population)
            

            g = GenerationTool(num_jobs, num_machines, population,
                               job_machine_time, iteration, pop, file_name)

            g.calculate_individual_worktime()

            print("Population worktime\n")
            print(g.population_worktime)
            
            g.first_gen()

            for i in range(1, iteration+1):
                g.create_new_gen(i)

            g.print_generations()
            
            g.print_generations_makespan()
