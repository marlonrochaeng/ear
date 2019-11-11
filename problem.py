from generation_tool import GenerationTool
from job import Job
from utils import generate_population, get_instance

iterations = 10

pop_size = 10
population = []

num_jobs, num_machines = get_instance(0)

jobs = [Job() for i in range(num_jobs)]

for i in range(pop_size):
    population.append(generate_population(num_jobs, num_machines))

g = GenerationTool(num_machines, population, jobs)
g.calculate_individual_worktime()

g.first_gen()

for i in range(iterations):
    g.create_new_gen(i)

#g.print_generations()
g.get_makespan_generations()
