import csv
import os
from random import randint
from time import gmtime, strftime


def get_instance(instance):
    """Esse metodo retorna as instancias de processos e maquinas do problema HCSP

    Arguments:
        instance {int} -- o argumento e um inteiro entre 0 e 5

    Returns:
        tupla de int --       - 1024 , 32
                                2048 , 64
                                ...
    """
    return 1024*pow(2, instance), 32*pow(2, instance)
    # return 24,8


def generate_population(num_jobs, num_machines):
    """Esse metodo retorna uma geracao de jobs alocados em maquinas

    Arguments:
        num_jobs {int} -- quantidade de jobs da instancia
        num_machines {int} -- quantidade de maquinas da instancia
    """
    gen = [randint(0, num_machines-1) for i in range(num_jobs)]
    return gen


def create_csv(num_jobs, num_machines, pop, iteration_size, populations_makespan, instance_name):
    filename = 'csv_1024_32//' + str(pop) + '_' + str(iteration_size)+ '_' + strftime("%Y-%m-%d-%H-%M-%S", gmtime()) + \
        '_' + instance_name + '_' + '.csv'
    info_list = []
    csv_columns = ['FILE_NAME', 'NUM_JOBS',
                   'NUM_MACHINES', 'ITERATION_SIZE', 'POPULATION_SIZE', 'ITERATION', 'MAKESPAN']
    for k, v in populations_makespan.items():
        info_list.append({'FILE_NAME': instance_name, 'NUM_JOBS': num_jobs, 'ITERATION_SIZE': iteration_size,
                          'NUM_MACHINES': num_machines, 'POPULATION_SIZE': pop, 'ITERATION': k, 'MAKESPAN': v})
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in info_list:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def get_files():
    path = '1024x32'

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file).split('\\')[1])

    return files
