from bitstring import Bits
from classes import *
from random import randrange as numero_aleatorio


class CromossomoQuadratico(Cromossomo):
    """
    Essa classe vai tratar do problema de encontrar o mínimo da função y = x^2
    Os cromossomos são uma sequência de 7 bits, onde o primeiro bit é o bit de sinal
    ou seja, os cromossomos representarão números inteiros entre -63 e +63
    """

    @staticmethod
    def gerar():
        """Geramos sequência de bits correspondentes a um número aleatório entre -numero_maximo e +numero_maximo"""
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
    def mutacionar(cromossomo: 'CromossomoQuadratico', chance_mutacao: float = 0.03):
        """Modifica aleatoriamente um gene do cromossomo. Essa mutação tem uma chance chance_mutacao de acontecer"""
        if random() > chance_mutacao:
            # Não modificar
            return cromossomo

        indice_gene = numero_aleatorio(0, len(cromossomo.genes))
        novos_genes = list(cromossomo.genes)
        gene = novos_genes[indice_gene]
        novos_genes[indice_gene] = '0' if gene == '1' else '1'

        return CromossomoQuadratico(''.join(novos_genes))

    @staticmethod
    def reproduzir(pai: 'CromossomoQuadratico', mae: 'CromossomoQuadratico'):
        """Podem existir vários métodos de reprodução.
        Cada método deve estar implementado em uma função.
        Essa função "reproduzir" vai chamar o método "default".
        """

        return CromossomoQuadratico.reproduzir_crossover_1(pai, mae)

    @staticmethod
    def reproduzir_crossover_1(pai: 'CromossomoQuadratico', mae: 'CromossomoQuadratico'):
        """Essa reprodução será crossover de um ponto, onde o ponto é aleatório.
        Eu gero um cromossomo, só pra pegar o seu tamanho.
        Depois, eu escolho um ponto aleatório no meio do cromossomo (ou seja, sem pegar o primeiro e último gene)
        e faço o crossover, gerando dois filhos.
        """
        # Tamanho do cromossomo. Esses -2 e +1 abaixo são pra
        # eu pegar entre o primeiro e último gene, sem incluí-los.
        num_genes = len(CromossomoQuadratico.gerar().genes) - 2
        cut_point = int(num_genes * random()) + 1

        filho_1 = pai.genes[:cut_point] + mae.genes[cut_point:]
        filho_2 = mae.genes[:cut_point] + pai.genes[cut_point:]

        return [filho_1, filho_2]


if __name__ == "__main__":
    """
    CONFIGURAÇÕES
    """
    # Quantos indivíduos vamos gerar
    TAM_POPULACAO = 12
    # Quantas gerações queremos ter
    NUM_GERACOES = 150
    # Método de seleção
    SELECAO = Selecoes.ROLETA
    # A geração, quantos cromossomos passam pela seleção
    QTD_SELECIONADOS = 6
    # Método de reprodução
    REPRODUCAO = Reproducoes.CROSSOVER_1
    # Chance de mutação
    CHANCE_MUTACAO = 0.03
    OBJETIVO = Objetivos.MINIMIZAR
    # Qual classe se responsabilizará pelo manuseio dos cromossomos
    classe_cromossomo = CromossomoQuadratico
    # Vamos guardar um histórico de todas gerações
    historico = []

    """
    TRIAGEM / PROCESSO
    """

    """População inicial"""

    # Geramos TAM_POPULACAO cromossomos aleatoriamente
    cromossomos = [classe_cromossomo.gerar() for x in range(TAM_POPULACAO)]

    for _ in range(NUM_GERACOES):
        # TODO historico

        """Seleção"""

        if SELECAO == Selecoes.ROLETA:
            cromossomos_selecionados = sortear_roleta(cromossomos, classe_cromossomo.avaliar, QTD_SELECIONADOS)

        else:
            cromossomos_selecionados = []

        """Reprodução"""

        if REPRODUCAO == Reproducoes.CROSSOVER_1:
            cromossomos_filhos = []
            while len(cromossomos_filhos) < TAM_POPULACAO:
                # Faço uma roleta pra pegar dois pais aleatórios para gerar os filhos
                pais = sortear_roleta(cromossomos_selecionados, classe_cromossomo.avaliar, 2)
                cromossomos_filhos.extend(classe_cromossomo.reproduzir_crossover_1(*pais))

        else:
            cromossomos_filhos = []

        """Mutação"""

        cromossomos = [classe_cromossomo.mutacionar(filho, CHANCE_MUTACAO) for filho in cromossomos_filhos]

    for cromossomo in cromossomos:
        print(cromossomo, " (%d)" % classe_cromossomo.avaliar(cromossomo))
