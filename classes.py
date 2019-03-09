from enum import Enum
from random import random


class Cromossomo:
    """
    Serve para definir o modelo geral de um cromossomo.
    Os métodos dessa classe devem ser implementados em uma subclasse, que
    tratará dos detalhes específicos de cada problema
    """
    # Informação genética
    genes = None

    def __init__(self, genes=None):
        self.genes = genes

    @staticmethod
    def gerar() -> 'Cromossomo':
        """Gera um cromossomo aleatoriamente"""
        raise NotImplementedError("Esse método deve ser definido pela classe herdeira")

    @staticmethod
    def avaliar(cromossomo: 'Cromossomo'):
        """Avalia a aptidão do cromossomo.
        Essa função deve ser sobrescrita em cada problema específico."""
        raise NotImplementedError("Essa função deve ser implementada especificamete para seu problema")

    @staticmethod
    def mutacionar(cromossomo: 'Cromossomo', chance_mutacao: float) -> 'Cromossomo':
        """Modifica aleatoriamente um gene"""
        raise NotImplementedError("Esse método deve ser definido pela classe herdeira")

    @staticmethod
    def reproduzir(pai: 'Cromossomo', mae: 'Cromossomo'):
        """Combina os genes dos dois cromossoos para gera um novo"""
        raise NotImplementedError("Esse método deve ser definido pela classe herdeira")

    def __repr__(self):
        return self.genes


"""ENUMERAÇÕES"""


class Reproducoes(Enum):
    """
    Tipos de reprodução implementadas
    """
    # Crossover de um ponto)
    CROSSOVER_1 = 2


class Selecoes(Enum):
    """
    Tipos de seleção implementadas
    """
    ROLETA = 1


class Objetivos(Enum):
    MINIMIZAR = 1
    MAXIMIZAR = 2


"""FUNÇÕES"""


def sortear_roleta(cromossomos: list, avaliadora, qtd: int, objetivo: Objetivos = Objetivos.MINIMIZAR):
    """
    Recebe uma lista de cromossomos. Recebe a função avaliadora, que retorna a aptidão de um cromossomo.
    Recebe também a quantidade de cromossomos a serem selecionados.

    Retorna uma lista com os cromossomos relecionados.

    A chance de um cromossomo ser sorteado é proporcional ao seu score dentre todos os outros scores.

    Se o objetivo for MINIMIZAR, as menores aptidões terão mais chances. Se não, as maiores que terão.

    OBSERVAÇÃO: a soma das chances só é 100% se o objetivo for MAXIMIZAR. Se for minimizar, passa de 100%,
    ou seja, o menor score pode ter uma chance de 75%, o segundo de 50%, o terceiro de 30%...
    """

    lista_de_fitness_scores = [avaliadora(x) for x in cromossomos]

    """Definir a forma de comparação, dependendo do objetivo"""
    if objetivo == Objetivos.MINIMIZAR:
        comparar = lambda sorteado, score: sorteado <= score
    else:
        comparar = lambda sorteado, score: sorteado >= score

    """Gerar as faixas de cada cromossomo"""
    acumulador_faixa = 0
    lista_de_faixas = []

    for cromossomo_fitness in lista_de_fitness_scores:
        acumulador_faixa += cromossomo_fitness
        lista_de_faixas.append(acumulador_faixa)

    if objetivo == Objetivos.MINIMIZAR:
        # A linha abaixo é só pra prevenir que o último cromossomo tenha 0% de chance, no caso de minimizar objetivo.
        lista_de_faixas[-1] += lista_de_fitness_scores[-1]

    total = sum(lista_de_fitness_scores)

    cromossomos_selecionados = []
    while len(cromossomos_selecionados) < qtd:
        # Gerar um número entre 0 e o total de pontos de score
        numero_sorteado = total * random()

        """Pegar o índice que corresponde à faixa do número sorteado"""
        for indice, aptidao in enumerate(lista_de_faixas):
            if comparar(numero_sorteado, aptidao):
                cromossomos_selecionados.append(cromossomos[indice])
                break

    return cromossomos_selecionados
