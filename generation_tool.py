import itertools
import math
import random

from utils import create_csv


class GenerationTool:
    def __init__(self, num_jobs, num_machines, population, job_machine_time, iteration, pop, instance_name):
        self.population = population
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.population_worktime = []
        self.job_machine_time = job_machine_time
        self.ordered_pop = {}
        self.pb = []
        self.best_matrix_len = int((len(
            population) - math.floor(0.7*len(population)))/10)
        self.best_candidates_len = int((len(
            population) - math.floor(0.5*len(population)))/10)
        self.best_candidates_len_c = int((len(
            population) - math.floor(0.5*len(population)))/10)
        print("BEST MATRIX LEN:" + str(self.best_matrix_len))
        print("BEST CANDIDATES LEN:" + str(self.best_candidates_len))
        print("BEST CANDIDATES LEN C:" + str(self.best_candidates_len_c))
        self.new_pop_len = int((len(population)/10 - self.best_candidates_len))
        #print("NEW POP LEN:" + str(self.new_pop_len))
        self.populations = []
        self.populations_makespan = {}
        for i in range(1, iteration+2):
            # add iterations and add makespan for each iteration
            self.populations_makespan[i] = []
        self.iteration = iteration
        self.pop = pop
        self.instance_name = instance_name

    def initialize_matrix(self):
        """Este metodo retorna a matriz de probabilidade preenchida com zeros

        Returns:
            [list of list[int]] -- 
        """
        self.pb = [[0 for col in range(self.num_machines)]
                   for row in range(self.num_jobs)]
        print("num machines {} num jobs {}".format(self.num_machines,self.num_jobs))

    def calculate_individual_worktime(self):
        """esse metodo percorre a populacao e verifica o makespan e worktime para cada maquina em cada individuo
        i = job
        p[i] = maquina
        """
        print("TAMANHO DA 1 POPULACAO: %d" %len(self.population))
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
        #print("tipo:", type(self.best_candidates_len))
        #self.ordered_pop = self.ordered_pop[0:self.best_candidates_len]
        #print("TAMANHO DA POPULACAO APOS RECUPERAR MELHORES VALORES:",
        #      len(self.ordered_pop))
        #print("QUANTIDADE DE INDIVIDUOS QUE SERAO GERADOS:", self.new_pop_len)

    def generate_matrix(self):
        """Este metodo gera a matriz de probabilidades

        """
        for op in self.ordered_pop[:self.best_matrix_len]:
            for i in range(len(op['individual'])):
                self.pb[i][op['individual'][i]] += 1

    def ajust_zero_elements(self):
        for op in self.ordered_pop:
            print("pb line")
            for i in range(len(op['individual'])):
                print(self.pb[i])
                if self.pb[i][op['individual'][i]] == 0:
                    self.pb[i][op['individual'][i]] += 0.1

    def print_matrix(self):
        for i in self.pb:
            print(i)

    def wheel_selection(self, lista):
        """Este metodo usa a selecao por roleta para gerar um novo individuo

        Arguments:
            lista {lista de int} -- lista de quantas vezes aquele processo apareceu naquela maquina

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

    def tournament_selection(self, lista):
        """Este metodo usa a selecao por torneio para gerar um novo individuo

        Arguments:
            lista {lista de int} -- lista de quantas vezes aquele processo apareceu naquela maquina

        Returns:
            [int] -- posicao do individuo selecionado na lista
        """
        k = int(len(lista)/2)

        tournament_list = []
        enum_list = list(enumerate(lista))

        for _ in range(k):
            tournament_list.append(random.choice(enum_list))
        
        tournament_list = sorted(tournament_list, key=lambda x:x[1], reverse=True)
        return tournament_list[0][0]


    def tournament_selection_modified(self, lista):
        """Este metodo usa a selecao por torneio para gerar um novo individuo

        Arguments:
            lista {lista de int} -- lista de quantas vezes aquele processo apareceu naquela maquina

        Returns:
            [int] -- posicao do individuo selecionado na lista
        """
        k = int(len(lista)/4)

        tournament_list = []
        enum_list = sorted(list(enumerate(lista)), key=lambda x:x[1], reverse=True)

        for pos in range(k):
            tournament_list.append(enum_list[pos])
        
        
        return random.choice(tournament_list)[0]


    def update_new_pop(self, new_individual, count):
        """Este metodo insere o novo individuo na populacao

        Arguments:
            new_individual {list of int} 
        """
        machine_job_relationship = {}
        for i in range(self.num_machines):
            machine_job_relationship[i] = []
        for i in range(len(new_individual)):
            machine_job_relationship[new_individual[i]].append(
                self.job_machine_time.get_jm_value(i, new_individual[i]))
        #self.ordered_pop.append(self.get_population_worktime(
        #    machine_job_relationship, new_individual))
        #
        
        #   self.ordered_pop = self.order_population_by_worktime(self.ordered_pop)
        #for i in range(len(self.ordered_pop)-1,0,-1):#pegar algum dos 5% pior na sorte e substituir se for melhor
            #print("i['makespan']:", i['makespan'][0])
            #print("self.get_population_worktime(machine_job_relationship, new_individual):", self.get_population_worktime(machine_job_relationship, new_individual)['makespan'][0])

        if self.ordered_pop[self.best_candidates_len + count]['makespan'][0] > self.get_population_worktime(machine_job_relationship, new_individual)['makespan'][0] and random.random() > 0.5:
            #print("trocou na pos: %d" % (self.best_candidates_len + count))
            #print("len ordered pop: %d" % len(self.ordered_pop))
            self.ordered_pop[self.best_candidates_len + count] = self.get_population_worktime(machine_job_relationship, new_individual)

            


    def suffle_pop(self):
        random.shuffle(self.ordered_pop)

    def first_gen(self):
        self.ordered_pop = self.order_population_by_worktime(
            self.population_worktime)
        print("ORDERED POP LEN: %d" %len(self.ordered_pop))
        #print("1 POPULATION ORDERED BY MAKESPAN")
        for i in self.ordered_pop:
            #print(i['individual'], i['makespan'])
            self.populations_makespan[1].append(i['makespan'])
        self.populations_makespan[1].append(i['makespan'][0])
        self.ordered_pop = self.ordered_pop[0:int(len(self.ordered_pop)/10)]

    def create_new_gen(self, num_gen):
        self.ordered_pop = self.order_population_by_worktime(self.ordered_pop)
        self.update_to_best_population()
        self.initialize_matrix()
        self.generate_matrix()
        #self.ajust_zero_elements()
        #print("PROBABILISTC MATRIX")
        #self.print_matrix()
        #print("GENERATING THE NEW INDIVIDUALS AND ADDING TO THE NEW POPULATION")
        for i in range(self.best_candidates_len_c):
            new_individual = []
            for j in self.pb:
                new_individual.append(self.tournament_selection(j))
            #print("new individual:", new_individual)
            #passar o i e sair verificando se aquele gerado e melhor que o cara da posicao best + i
            self.update_new_pop(new_individual, i)
        self.ordered_pop = self.order_population_by_worktime(self.ordered_pop)
        self.populations_makespan[num_gen +
                                  1].append(self.ordered_pop[-1]['makespan'][0])
        #print(str(num_gen+1)+" POPULATION ORDERED BY MAKESPAN")
        #for i in self.ordered_pop:
        #    print(i['individual'], i['makespan'])
        print("NEW POPULATION SIZE:", len(self.ordered_pop))

    def print_generations(self):
        for i in range(len(self.populations)):
            print("----------------printing the "+str(i+1) +
                  " population-------------------------\n")
            print(self.populations[i][1]['makespan'][0])

    def print_generations_makespan(self):
        #print("POPULATION MAKESPAN\n")
        self.populations_makespan[1] = self.populations_makespan[1][-1]
        #print(self.populations_makespan)
        create_csv(self.num_jobs, self.num_machines, self.pop, self.iteration,
                   self.populations_makespan, self.instance_name)
        # num_jobs, num_machines, iterations, pop, iteration, makespan
