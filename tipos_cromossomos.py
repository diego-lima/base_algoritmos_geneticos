from bitstring import Bits
from classes_ga import *
from random import randrange as numero_aleatorio, random, choice


class CromossomoQuadratico(Cromossomo):
    """
    Essa classe vai tratar do problema de encontrar o mínimo da função y = x^2
    Os cromossomos são uma sequência de 7 bits, onde o primeiro bit é o bit de sinal
    ou seja, os cromossomos representarão números inteiros entre -64 e +63
    observação: o método gerar() só gera números a partir de 0
    """

    @staticmethod
    def gerar():
        """Geramos sequência de bits correspondentes a um número aleatório entre zero e numero_maximo"""
        numero_maximo = 63

        numero = numero_aleatorio(0, numero_maximo+1, 1)
        tam = len(bin(numero_maximo)) - 1
        return CromossomoQuadratico(Bits(int=numero, length=tam).bin)

    @staticmethod
    def avaliar(cromossomo):
        """Avalia a aptidão do cromossomo."""
        x = Bits(bin=cromossomo.genes).int
        return x**2

    @staticmethod
    def mutacionar(cromossomo: 'CromossomoQuadratico', chance_mutacao: float = 0.03):
        """Modifica aleatoriamente um gene do cromossomo. Essa mutação tem uma chance chance_mutacao de acontecer."""

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

        return [CromossomoQuadratico(filho_1), CromossomoQuadratico(filho_2)]


class CromossomoQuadraticoDecimal(Cromossomo):
    """
    Essa classe vai tratar do problema de encontrar o mínimo da função y = x^2
    Dessa vez, os cromossomos serão valores numéricos na representação decimal mesmo.
    """

    @staticmethod
    def gerar():
        """Geramos um número aleatório entre -numero_maximo e +numero_maximo"""
        numero_maximo = 63

        sinal = choice([1, -1])

        numero_gerado = sinal * numero_maximo * random()

        return CromossomoQuadraticoDecimal(numero_gerado)

    @staticmethod
    def avaliar(cromossomo):
        """Avalia a aptidão do cromossomo."""

        return cromossomo.genes ** 2

    @staticmethod
    def mutacionar(cromossomo: 'CromossomoQuadraticoDecimal', chance_mutacao: float = 0.03):
        """Modifica aleatoriamente o gene do cromossomo. Essa mutação tem uma chance chance_mutacao de acontecer.
        A mutação é assim: quando ela acontece, damos uma variação aleatória entre 0 e 10% do valor numérico do gene."""

        if random() > chance_mutacao:
            # Não modificar
            return cromossomo

        sinal = choice([1, -1])

        variacao = 0.1 * random()

        novo_gene = cromossomo.genes + cromossomo.genes * variacao * sinal

        return CromossomoQuadraticoDecimal(novo_gene)

    @staticmethod
    def reproduzir(pai: 'CromossomoQuadraticoDecimal', mae: 'CromossomoQuadraticoDecimal'):
        """A reprodução está sendo assim: eu calculo a "margem" entre os genes do pai e da mãe, que é como se fosse
        o desvio padrão entre eles dois, só que menor (porque eu divido por três).
        Dai, eu aplico essa margem aleatoriamente pra cima ou pra baixo no pai, gerando um filho,
        e pra cima ou pra baixo na mãe, gerando outro filho.
        """

        margem = abs(pai.genes - mae.genes) / 3

        sinal = [1, -1]

        filho_1 = pai.genes + margem * choice(sinal)
        filho_2 = mae.genes + margem * choice(sinal)

        return [CromossomoQuadraticoDecimal(filho_1), CromossomoQuadraticoDecimal(filho_2)]


class CromossomoCilindroParabolico(Cromossomo):
    """
    Essa classe vai tratar do problema de encontrar o mínimo da função z = x^2 - 2 x y + 6 x + y^2 - 6 y
    Dessa vez, os cromossomos serão valores numéricos na representação decimal mesmo.
    """

    @staticmethod
    def gerar():
        """Geramos dois números aleatórios entre -numero_maximo e +numero_maximo"""
        numero_maximo = 63

        numero1 = choice([1, -1]) * numero_maximo * random()
        numero2 = choice([1, -1]) * numero_maximo * random()

        return CromossomoCilindroParabolico([numero1, numero2])

    @staticmethod
    def avaliar(cromossomo):
        """Avalia a aptidão do cromossomo."""

        def funcao(x,y):
            return x**2 - 2*x*y + 6*x + y**2 - 6*y

        return funcao(*cromossomo.genes)

    @staticmethod
    def mutacionar(cromossomo: 'CromossomoCilindroParabolico', chance_mutacao: float = 0.03):
        """Modifica aleatoriamente o gene do cromossomo. Essa mutação tem uma chance chance_mutacao de acontecer.
        A mutação é assim: quando ela acontece, damos uma variação aleatória entre 0 e 10% do valor numérico do gene."""

        if random() > chance_mutacao:
            # Não modificar
            return cromossomo

        variacao1 = 0.1 * random() * choice([1, -1])
        variacao2 = 0.1 * random() * choice([1, -1])

        novos_genes = [
            cromossomo.genes[0] + cromossomo.genes[0] * variacao1,
            cromossomo.genes[1] + cromossomo.genes[1] * variacao2
        ]

        return CromossomoCilindroParabolico(novos_genes)

    @staticmethod
    def reproduzir(pai: 'CromossomoCilindroParabolico', mae: 'CromossomoCilindroParabolico'):
        """A reprodução está sendo assim: eu calculo a "margem" entre os genes do pai e da mãe, que é como se fosse
        o desvio padrão entre eles dois, só que menor (porque eu divido por três).
        Dai, eu aplico essa margem aleatoriamente pra cima ou pra baixo no pai, gerando um filho,
        e pra cima ou pra baixo na mãe, gerando outro filho.
        """

        margem1 = abs(pai.genes[0] - mae.genes[0]) / 3
        margem2 = abs(pai.genes[1] - mae.genes[1]) / 3

        sinal = [1, -1]

        genes_filho_1 = [
            pai.genes[0] + margem1 * choice(sinal),
            pai.genes[1] + margem2 * choice(sinal),

        ]
        genes_filho_2 = [
            mae.genes[0] + margem1 * choice(sinal),
            mae.genes[1] + margem2 * choice(sinal),

        ]

        return [CromossomoCilindroParabolico(genes_filho_1), CromossomoCilindroParabolico(genes_filho_2)]
