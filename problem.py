import os

from generation_tool import GenerationTool
from job import JobMachine
from utils import generate_population, get_files, get_instance

from multiprocessing import Pool

iterations = [5000]

pop_size = [1000]

files = sorted(get_files())[1::]

print(files)

def schedule(file_name):

    file = list(open(os.path.join("512_16", file_name)))
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
            for i in range(pop*10):
                population.append(generate_population(num_jobs, num_machines))
            

            g = GenerationTool(num_jobs, num_machines, population,
                               job_machine_time, iteration, pop, file_name)

            g.calculate_individual_worktime()

            #print("Population worktime\n")
            #print(g.population_worktime)
            
            g.first_gen()

            for i in range(1, iteration+1):
                print("Iteration: %d" %i)
                g.create_new_gen(i)

            #g.print_generations()
            
            g.print_generations_makespan()

if __name__ == '__main__':
    with Pool(8) as p:
        print(p.map(schedule, files))