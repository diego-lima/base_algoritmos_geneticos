from enum import Enum
from random import random, choices
from typing import Union, List


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
    def avaliar(cromossomo: 'Cromossomo') -> Union[int, float]:
        """Avalia a aptidão do cromossomo.
        Essa função deve ser sobrescrita em cada problema específico."""
        raise NotImplementedError("Essa função deve ser implementada especificamete para seu problema")

    @staticmethod
    def mutacionar(cromossomo: 'Cromossomo', chance_mutacao: float) -> 'Cromossomo':
        """Modifica aleatoriamente um gene"""
        raise NotImplementedError("Esse método deve ser definido pela classe herdeira")

    @staticmethod
    def reproduzir(pai: 'Cromossomo', mae: 'Cromossomo') -> List['Cromossomo']:
        """Combina os genes dos dois cromossoos para gerar um novo.

        Se houverem vários métodos de reprodução implementados, Cromossomo.reproduzir deve redirecionar
        para o método default de reprodução."""
        raise NotImplementedError("Esse método deve ser definido pela classe herdeira")

    def __repr__(self):
        return "%s (%.0f)" % (self.genes, self.__class__.avaliar(self))


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
    TORNEIO = 2


class Objetivos(Enum):
    MINIMIZAR = 1
    MAXIMIZAR = 2


"""FUNÇÕES"""


def sortear_roleta(cromossomos: list, avaliadora, qtd: int, objetivo: Objetivos = Objetivos.MINIMIZAR,
                   substituicao: bool = False):
    """
    Recebe uma lista de cromossomos. Recebe a função avaliadora, que retorna a aptidão de um cromossomo.
    Recebe também a quantidade de cromossomos a serem selecionados.
    O parâmetro substituicao decide se um mesmo cromossomo pode ser selecionado mais de uma vez (há substituição).

    Retorna uma lista com os cromossomos relecionados.

    A chance de um cromossomo ser sorteado é proporcional ao seu score dentre todos os outros scores.

    Se o objetivo for MINIMIZAR, as menores aptidões terão mais chances. Se não, as maiores que terão.

    OBSERVAÇÃO: a soma das chances só é 100% se o objetivo for MAXIMIZAR. Se for minimizar, passa de 100%,
    ou seja, o menor score pode ter uma chance de 75%, o segundo de 50%, o terceiro de 30%...
    """
    # Vamos copiar a lista de cromossomos, pra não mexer na lista original, que foi passada
    lista_de_cromossomos = list()
    lista_de_cromossomos.extend(cromossomos)

    lista_de_fitness_scores = [avaliadora(x) for x in lista_de_cromossomos]

    """Definir a forma de comparação, dependendo do objetivo"""
    if objetivo == Objetivos.MINIMIZAR:
        comparar = lambda sorteado, score: sorteado >= score
    else:
        comparar = lambda sorteado, score: sorteado <= score

    """Gerar as faixas de cada cromossomo"""
    acumulador_faixa = 0
    lista_de_faixas = []

    for cromossomo in lista_de_cromossomos:
        acumulador_faixa += avaliadora(cromossomo)
        lista_de_faixas.append(acumulador_faixa)

    total = lista_de_faixas[-1]

    if objetivo == Objetivos.MINIMIZAR:
        # A linha abaixo é só pra prevenir que o último cromossomo tenha 0% de chance, no caso de minimizar objetivo.
        # estamos aumentando a faixa do último
        lista_de_faixas[-1] += avaliadora(lista_de_cromossomos[-1])

    cromossomos_selecionados = []
    indices_cromossomos_escolhidos = set()

    while len(cromossomos_selecionados) < qtd:
        # Gerar um número entre 0 e o total de pontos de score
        numero_sorteado = total * random()

        """Pegar o índice que corresponde à faixa do número sorteado"""
        for indice, aptidao in enumerate(lista_de_faixas):
            if indice in indices_cromossomos_escolhidos and not substituicao:
                # vamos pular esse, que já foi escolhido
                continue

            if comparar(numero_sorteado, aptidao):
                cromossomos_selecionados.append(lista_de_cromossomos[indice])
                indices_cromossomos_escolhidos.add(indice)
                break

    return cromossomos_selecionados


def sortear_torneio(cromossomos: list, avaliadora, qtd: int, objetivo: Objetivos = Objetivos.MINIMIZAR):
    """
    Recebe uma lista de cromossomos. Recebe a função avaliadora, que retorna a aptidão de um cromossomo.
    Recebe também a quantidade de cromossomos a serem selecionados.

    Retorna uma lista com os cromossomos relecionados.

    Implementa o método de seleção Torneio, pegando de 3 em 3 candidatos.
    """

    if objetivo == Objetivos.MINIMIZAR:
        # O torneio pega o primeiro, de menor fitness
        indice_selecao = 0
    else:
        # O torneio pega o último, de maior fitness
        indice_selecao = -1

    cromossomos_selecionados = []
    while len(cromossomos_selecionados) < qtd:

        # Sortear 3 cromossomos aleatoriamente
        cromossomos_sorteados = sorted(choices(cromossomos, k=3), key=avaliadora)

        # Pegar o mais apto dos três
        cromossomos_selecionados.append(cromossomos_sorteados[indice_selecao])

    return cromossomos_selecionados
