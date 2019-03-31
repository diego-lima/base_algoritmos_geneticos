from bitstring import Bits
from classes_ga import *
from classes_misc import *
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

        def funcao(x, y):
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


class CromossomoPotencia(Cromossomo):

    planta = None
    k = 1

    @staticmethod
    def gerar():
        if not CromossomoPotencia.planta.pontos_internos:
            raise Exception("falta calcular pontos internos antes de gerar")
        genes = choices(list(CromossomoPotencia.planta.pontos_internos), k=CromossomoPotencia.k)
        return CromossomoPotencia(genes)

    @staticmethod
    def avaliar(cromossomo: 'Cromossomo'):
        CromossomoPotencia.planta.simular_fontes(*cromossomo.genes)
        return max([ponto.valor for ponto in CromossomoPotencia.planta.pontos_internos])

    @staticmethod
    def reproduzir(pai: 'Cromossomo', mae: 'Cromossomo'):
        """A reprodução está sendo assim: eu calculo a "margem" entre os genes do pai e da mãe, que é como se fosse
        o desvio padrão de cada coordenada entre eles dois.

        Dai, eu aplico essa margem aleatoriamente pra cima ou pra baixo no pai, gerando um filho,
        e pra cima ou pra baixo na mãe, gerando outro filho.

        Como cada cromossomo pode guardar a posição de várias fon tes nos seus genes, eu faço assim:

        pego a margem entre o primeiro roteador do pai e o primeiro roteador da mãe, e dou o primeiro roteador filho
        e repito para os roteadores seguintes
        """

        genes_filho_1 = []
        genes_filho_2 = []

        sinal = [1, -1]

        for genes in zip(pai.genes, mae.genes):
            achou = False
            while not achou:
                # Para cada gene do pai e da mãe, vamos gerar dois filhos. Enquanto tiver algum filho caindo
                # fora da planta, vamos ficar reproduzindo.

                """Margem entre o roteador do pai e roteador da mãe"""
                margem_x = abs(genes[0].x - genes[1].x) / 2
                margem_y = abs(genes[0].y - genes[1].y) / 2

                """Gerando um filho no entorno do pai"""
                novo_gene_1 = Ponto(
                    genes[0].x + margem_x * choice(sinal),
                    genes[0].y + margem_y * choice(sinal)
                )
                novo_gene_1 = CromossomoPotencia.planta.encontrar(novo_gene_1)

                """Gerando um filho no entorno da mãe"""
                novo_gene_2 = Ponto(
                    genes[1].x + margem_x * choice(sinal),
                    genes[1].y + margem_y * choice(sinal)
                )
                novo_gene_2 = CromossomoPotencia.planta.encontrar(novo_gene_2)

                if all((novo_gene_1, novo_gene_2)):
                    achou = True
                    genes_filho_1.append(novo_gene_1)
                    genes_filho_2.append(novo_gene_2)

        return [CromossomoPotencia(genes_filho_1), CromossomoPotencia(genes_filho_2)]

    @staticmethod
    def mutacionar(cromossomo: 'Cromossomo', chance_mutacao: float):
        """A mutação é simples: pega um dos vizinhos de cada fonte no gene.

        Se eu não conseguir encontrar um vizinho que esteja DENTRO da planta com até 8 tentativas,
        eu não mudo aquela fonte."""

        if random() > chance_mutacao:
            # Não modificar
            return cromossomo

        novo_cromossomo = []

        for gene in cromossomo.genes: # vamos tentar achar um vizinho pra cada fonte dentro dos genes...
            vizinho = choice(gene.vizinhos)
            achou = False
            for _ in range(8):
                # Um ponto pode ter um vizinho fora da planta. Vamos tentar achar um vizinho dentro da planta até 8
                # vezes.
                if CromossomoPotencia.planta.encontrar(vizinho):
                    achou = True
                    break
                vizinho = choice(gene.vizinhos)

            if not achou:
                # infelizmente não achei um vizinho. aquela parte do gene vai permanecer como está
                vizinho = gene

            novo_cromossomo.append(vizinho)

        return CromossomoPotencia(novo_cromossomo)


if __name__ == "__main__":
    planta = Planta(4)
    lado_quadrado = 20
    """Estamos fazendo um quadrado de lado lado_quadrado, que a ponta inferior esquerda tá na origem"""
    planta.adicionar_parede(Ponto(0, lado_quadrado), Ponto(lado_quadrado, lado_quadrado))
    planta.adicionar_parede(Ponto(lado_quadrado, lado_quadrado), Ponto(lado_quadrado, 0))
    planta.adicionar_parede(Ponto(lado_quadrado, 0), Ponto(0, 0))
    planta.adicionar_parede(Ponto(0, 0), Ponto(0, lado_quadrado))

    planta.procurar_pontos_internos()

    CromossomoPotencia.planta = planta
    CromossomoPotencia.k = 2

    cromossomos = [CromossomoPotencia.gerar(), CromossomoPotencia.gerar()]

    print()
