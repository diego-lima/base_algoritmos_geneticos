from bitstring import Bits
from classes import *
from random import randrange as numero_aleatorio


class CromossomoQuadratico(Cromossomo):
    """
    Essa classe vai tratar do problema de encontrar o mínimo da função
    y = x^2
    """

    @staticmethod
    def gerar():
        """Geramos sequência de bits correspondentes a um número aleatório entre -63 e 63"""
        numero_maximo = 63

        numero = numero_aleatorio(-numero_maximo, numero_maximo+1, 1)
        tam = len(bin(numero_maximo)) - 1
        return CromossomoQuadratico(Bits(int=numero, length=tam).bin)

    @staticmethod
    def avaliar(cromossomo):
        """Avalia a aptidão do cromossomo."""
        x = Bits(bin=cromossomo.genes).int
        return x**2

    @staticmethod
    def mutacionar(cromossomo):
        """Modifica aleatoriamente um gene do cromossomo"""
        indice_gene = numero_aleatorio(0, len(cromossomo.genes))
        novos_genes = list(cromossomo.genes)
        gene = novos_genes[indice_gene]
        novos_genes[indice_gene] = '0' if gene == '1' else '1'

        return CromossomoQuadratico(''.join(novos_genes))

    @staticmethod
    def reproduzir(pai, mae):
        pass


if __name__ == "__main__":
    """
    CONFIGURAÇÕES
    """
    # Quantos indivíduos vamos gerar
    TAM_POPULACAO = 10
    # Qual classe se responsabilizará pelo manuseio dos cromossomos
    classe_cromossomo = CromossomoQuadratico
    # Quantas gerações queremos ter
    NUM_GERACOES = 150
    # Vamos guardar um histórico de todas gerações
    historico = []

    """
    TRIAGEM
    """
    # Geramos TAM_POPULACAO cromossomos aleatoriamente
    cromossomos = [classe_cromossomo.gerar() for x in range(TAM_POPULACAO)]

    # Vamos fazer NUM_GERACOES iterações
    for _ in range(NUM_GERACOES):
        # TODO historico
        # Guardamos a geração atual no histórico
        # Ordenamos pela aptidão: os de menor (melhor) score são os primeiros
        cromossomos.sort(key=classe_cromossomo.avaliar)

        # Aplicamos uma mutação aleatória em todos cromossomos
        cromossomos = map(CromossomoQuadratico.mutacionar, cromossomos)
