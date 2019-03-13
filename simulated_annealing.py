from math import exp
from random import random, choice
from typing import Union, List


class Solucao:
    """Classe base que abstrai os detalhes de um problema que será resolvido com Simulated Annealing.
    """

    valor = None

    def __init__(self, valor=None):
        self.valor = valor

    @staticmethod
    def gerar() -> 'Solucao':
        raise NotImplementedError

    @property
    def vizinhos(self) -> List['Solucao']:
        raise NotImplementedError

    @property
    def energia(self) -> Union[int, float]:
        raise NotImplementedError

    def __repr__(self):
        return "%s (%.1f)" % (self.valor, self.energia)


class SolucaoQuadratica(Solucao):
    """
    Resolve, por simulated annealing, o problema de minizar a função y = x^2
    """

    @staticmethod
    def gerar():
        """Geramos um número aleatório entre -numero_maximo e +numero_maximo"""
        numero_maximo = 63

        sinal = choice([1, -1])

        numero_gerado = sinal * numero_maximo * random()

        return SolucaoQuadratica(numero_gerado)

    @property
    def vizinhos(self):

        variacao = 0.1 * random()

        novo_valor_1 = self.valor + self.valor * variacao
        novo_valor_2 = self.valor - self.valor * variacao

        return [SolucaoQuadratica(novo_valor_1), SolucaoQuadratica(novo_valor_2)]

    @property
    def energia(self):
        return self.valor ** 2



def probabilidade_exponencial(temperatura, valor):

    return exp(valor / (-1 * temperatura))


if __name__ == "__main__":
    """
    CONFIGURAÇÕES
    """
    DECAIMENTO_TEMPERATURA = 0.99
    TEMPERATURA_INICIAL = 30
    TEMPERATURA_FINAL = 0
    PASSOS_POR_TEMPERATURA = 3
    LIMITE_ITERACOES = 1000

    classe = SolucaoQuadratica

    """
    START
    """

    temperatura = TEMPERATURA_INICIAL

    solucao_atual = classe.gerar()

    contador = 0

    while temperatura > TEMPERATURA_FINAL:

        for _ in range(PASSOS_POR_TEMPERATURA):
            solucao_vizinha = choice(solucao_atual.vizinhos)

            delta_energia = solucao_vizinha.energia - solucao_atual.energia
            print("delta: ", delta_energia)

            if delta_energia < 0:
                solucao_atual = solucao_vizinha

            elif probabilidade_exponencial(temperatura, delta_energia) > random():
                solucao_atual = solucao_vizinha

        temperatura = temperatura * DECAIMENTO_TEMPERATURA

        contador += 1
        if contador >= LIMITE_ITERACOES:
            break

    print("Solução: ", solucao_atual)




