from random import randint


def get_instance(instance):
    """Esse metodo retorna as instancias de processos e maquinas do problema HCSP
    
    Arguments:
        instance {int} -- o argumento e um inteiro entre 0 e 5
    
    Returns:
        tupla de int --       - 1024 , 32
                                2048 , 64
                                ...
    """
    return 1024*pow(2,instance),32*pow(2,instance)
    #return 24,8

def generate_population(num_jobs, num_machines):
    """Esse metodo retorna uma geracao de jobs alocados em maquinas
    
    Arguments:
        num_jobs {int} -- quantidade de jobs da instancia
        num_machines {int} -- quantidade de maquinas da instancia
    """
    gen = [randint(0,num_machines-1) for i in range(num_jobs)]
    return gen
