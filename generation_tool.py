import itertools
import math
import random


class GenerationTool:
    def __init__(self, num_jobs, num_machines, population, job_machine_time):
        self.population = population
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.population_worktime = []
        self.job_machine_time = job_machine_time
        self.ordered_pop = {}
        self.pb = []
        self.best_candidates_len = int(len(
            population) - math.floor(0.3*len(population)))
        self.new_pop_len = int(len(population) - self.best_candidates_len)
        self.populations = []

    def initialize_matrix(self):
        """Este metodo retorna a matriz de probabilidade preenchida com zeros

        Returns:
            [list of list[int]] -- 
        """
        self.pb = [[0 for col in range(self.num_machines)]
                   for row in range(self.num_jobs)]

    def calculate_individual_worktime(self):
        """esse metodo percorre a populacao e verifica o makespan e worktime para cada maquina em cada individuo
        i = job
        p[i] = maquina
        """
        for p in self.population:
            machine_job_relationship = {}
            for i in range(self.num_machines):
                machine_job_relationship[i] = []
            for i in range(len(p)):
                machine_job_relationship[p[i]].append(
                    self.job_machine_time.get_jm_value(i, p[i]))
            self.population_worktime.append(
                self.get_population_worktime(machine_job_relationship, p))

    def get_population_worktime(self, machine_job_relationship, individual):
        """este metodo cria o objeto que contem o individuo, carga de cada maquina e makespan

        Arguments:
            machine_job_relationship {dict} -- soma de cada job em cada maquina
            individual {list of int} -- individuo da populacao

        Returns:
            [dict] -- ex: {0: 96, 1: 109, 2: 94, 3: 305, 4: 39, 5: 229, 6: 330, 7: 126, 'makespan': (330, 6), 'individual': [5, 1, 1, 3, 2, 1, 5, 3, 6, 3, 0, 3, 2, 1, 6, 6, 6, 2, 4, 7, 5, 7, 6, 5]}
        """
        worktime = {}
        for m in range(self.num_machines):
            soma = 0
            for i in machine_job_relationship[m]:
                soma += i
            worktime[m] = soma
            worktime[m]
        worktime['makespan'] = max([(value, key)
                                    for key, value in worktime.items()])
        worktime['individual'] = individual
        return worktime

    def order_population_by_worktime(self, to_sort):
        """Este metodo retorna a lista de populacao ordenada de forma crescente 
        onde o valor utilizado para comparacao eh o makespan

        Returns:
            [list of object] 
        """
        return sorted(to_sort, key=lambda i: i['makespan'])

    def update_to_best_population(self):
        """Este metodo salva a populacao atual e deleta os 30% menos interessantes 
        """
        self.populations.append(self.ordered_pop[:])
        print("tipo:",type(self.best_candidates_len))
        self.ordered_pop = self.ordered_pop[0:self.best_candidates_len]
        print("TAMANHO DA POPULACAO APOS RECUPERAR MELHORES VALORES:",
              len(self.ordered_pop))
        print("QUANTIDADE DE INDIVIDUOS QUE SERAO GERADOS:", self.new_pop_len)

    def generate_matrix(self):
        """Este metodo gera a matriz de probabilidades

        """
        for op in self.ordered_pop:
            for i in range(len(op['individual'])):
                self.pb[i][op['individual'][i]] += 1

    def print_matrix(self):
        for i in self.pb:
            print(i)

    def wheel_selection(self, lista):
        """Este metodo usa a selecao por roleta para gerar um novo individuo

        Arguments:
            lista {lista de int} -- lista do workload das maquinas

        Returns:
            [int] -- posicao do individuo selecionado na lista
        """
        max = sum(l for l in lista)
        pick = random.uniform(0, max)
        current = 0
        for v in range(len(lista)):
            current += lista[v]
            if current > pick:
                return v

    def update_new_pop(self, new_individual):
        """Este metodo insere o novo individuo na populacao

        Arguments:
            new_individual {list of int} 
        """
        machine_job_relationship = {}
        for i in range(self.num_machines):
            machine_job_relationship[i] = []
        for i in range(len(new_individual)):
            machine_job_relationship[new_individual[i]].append(self.job_machine_time.get_jm_value(i, new_individual[i]))
        self.ordered_pop.append(self.get_population_worktime(
            machine_job_relationship, new_individual))

    def suffle_pop(self):
        random.shuffle(self.ordered_pop)

    def first_gen(self):
        self.ordered_pop = self.order_population_by_worktime(
            self.population_worktime)
        print("1 POPULATION ORDERED BY MAKESPAN")
        for i in self.ordered_pop:
            print(i['individual'], i['makespan'])

    def create_new_gen(self, num_gen):
        self.update_to_best_population()
        self.initialize_matrix()
        self.generate_matrix()
        print("PROBABILISTC MATRIX")
        self.print_matrix()
        print("GENERATING THE NEW INDIVIDUALS AND ADDING TO THE NEW POPULATION")
        for i in range(self.new_pop_len):
            new_individual = []
            for i in self.pb:
                new_individual.append(self.wheel_selection(i))
            print("new individual:", new_individual)
            self.update_new_pop(new_individual)
        self.ordered_pop = self.order_population_by_worktime(self.ordered_pop)
        print(str(num_gen+1)+" POPULATION ORDERED BY MAKESPAN")
        for i in self.ordered_pop:
            print(i['individual'], i['makespan'])
        print("NEW POPULATION SIZE:", len(self.ordered_pop))

    def print_generations(self):
        for i in range(len(self.populations)):
            print("----------------printing the "+str(i+1) +
                  " population-------------------------\n")
            print(self.populations[i][1]['makespan'])
