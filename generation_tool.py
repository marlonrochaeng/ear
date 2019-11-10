import itertools
import math
import random


class GenerationTool:
    def __init__(self, num_machines, population, jobs):
        self.population = population
        self.num_machines = num_machines
        self.population_worktime = []
        self.jobs = jobs
        self.ordered_pop = {}
        self.pb = [[0 for col in range(num_machines)]
                   for row in range(len(jobs))]
        self.best_candidates_len = len(
            population) - math.floor(0.7*len(population))
        self.new_pop_len = len(population) - self.best_candidates_len

    def calculate_individual_worktime(self):
        """esse metodo percorre a populacao e verifica o makespan e worktime para cada maquina em cada individuo
        """
        for p in self.population:
            machine_job_relationship = {}
            for i in range(self.num_machines):
                machine_job_relationship[i] = []
            for i in range(len(p)):
                machine_job_relationship[p[i]].append(self.jobs[i])
            self.population_worktime.append(
                self.get_population_worktime(machine_job_relationship, p))
        # print(len(self.population_worktime))
        # print(self.population_worktime[0])

    def get_population_worktime(self, machine_job_relationship, individual):
        worktime = {}

        for m in range(self.num_machines):
            soma = 0
            for i in machine_job_relationship[m]:
                soma += i.work_time
            worktime[m] = soma
            worktime[m]
        worktime['makespan'] = max([(value, key)
                                    for key, value in worktime.items()])
        worktime['individual'] = individual
        return worktime

    def order_population_by_worktime(self):
        return sorted(self.population_worktime, key=lambda i: i['makespan'])

    def update_to_best_population(self):
        self.ordered_pop = self.ordered_pop[0:self.best_candidates_len]

    def generate_matrix(self):
        for op in self.ordered_pop[0:self.best_candidates_len]:
            for i in range(len(op['individual'])):
                self.pb[i][op['individual'][i]] += 1

    def print_matrix(self):
        for i in self.pb:
            print(i)

    def wheel_selection(self, lista):
        max = sum(l for l in lista)
        pick = random.uniform(0, max)
        current = 0
        for v in range(len(lista)):
            current += lista[v]
            if current > pick:
                return v

    def update_new_pop(self, new_individual):
        machine_job_relationship = {}
        for i in range(self.num_machines):
            machine_job_relationship[i] = []
        for i in range(len(new_individual)):
            machine_job_relationship[new_individual[i]].append(self.jobs[i])
        self.ordered_pop.append(self.get_population_worktime(
            machine_job_relationship, new_individual))

    def suffle_pop(self):
        random.shuffle(self.ordered_pop)

    def call_functions(self):
        self.ordered_pop = self.order_population_by_worktime()
        self.update_to_best_population()
        print("POPULATION ORDERED BY MAKESPAN")
        print(self.ordered_pop[0:5])
        self.generate_matrix()
        print("PROBABILISTC MATRIX")
        self.print_matrix()
        print("GENERATING THE NEW INDIVIDUALS AND ADDING TO THE NEW POPULATION")
        for i in range(self.new_pop_len):
            new_individual = []
            for i in self.pb:
                new_individual.append(self.wheel_selection(i))
            self.update_new_pop(new_individual)
        print("SHUFFLE THE POPULATION")
        self.suffle_pop()
        print(self.ordered_pop[0:5])
