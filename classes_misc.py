from collections import deque as fila
from shapely.geometry import MultiPoint, Polygon, Point, LineString
from typing import Union, List

import random


def media(*numeros: Union[float, int]):
    """
    Retorna a média dos números passados.
    """

    return sum(numeros)/len(numeros)


def ponto_aleatorio(poly: Polygon):
    """
    Encontra um ponto aleatório que esteja dentro do polígono passado.
    """
    (minx, miny, maxx, maxy) = poly.bounds
    while True:
        p = Ponto(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if poly.contains(p):
            return p


def distancia_entre_pontos(p1: 'Ponto', p2: 'Ponto'):
    """
    Retorna a distância euclidiana entre dois pontos.
    """
    return (abs(p1.x - p2.x)**2 + abs(p1.y - p2.y)**2) ** 0.5


def line_intersection(line1, line2):

    line1 = LineString([(line1[0].x, line1[0].y),(line1[1].x,line1[1].y)])
    line2 = LineString([(line2[0].x, line2[0].y),(line2[1].x,line2[1].y)])
    return line1.intersection(line2)


class Ponto(Point):
    """
    Essa classe encapsula o comportamento de um ponto no plano cartesiano. Herda da classe
    shapely.geometry.Point, acrescentando vizinhos e valor.

    Também acrescenta a possibilidade de o ponto ser usado como chave em um dicionário
    ou item de um set.
    """
    _vizinhos = None
    valor = None

    def __init__(self, *args: Union[float, int]):
        super().__init__(*args)
        self._vizinhos = list()

    @property
    def vizinhos(self):
        """
        Retorna os vizinhos.

        Para poder retornar os vizinhos, você deve ter antes chamado a função calcular_vizinhos, informando
        a granularidade.
        """
        if self._vizinhos is None:
            raise Exception("Antes de tentar saber quais são os vizinhos, chame ponto.calcular_vizinhos\
                informando a granularidade!")

        return self._vizinhos

    def calcular_vizinhos(self, granularidade: float):
        """
        Retorna os quatro pontos vizinhos a self (cima, baixo, direita, esquerda), de acordo
        com a granularidade passada.

        Essa função também seta os vizinhos na propriedade da classe.
        """
        self._vizinhos = [
            Ponto(self.x, self.y + granularidade),
            Ponto(self.x, self.y - granularidade),
            Ponto(self.x + granularidade, self.y),
            Ponto(self.x - granularidade, self.y),
        ]

        return self._vizinhos

    def __str__(self):
        return "(%s)" % ','.join(["%.2f" % x for x in self.coords[0]])

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        """Serve para que o ponto possa ser usado como chave de dicionário ou de conjunto(set)."""
        return hash(self.__str__())


class Planta:
    """
    Essa classe cuida do problema de conhecer todos os pontos dentro de uma determinada
    forma geométrica.
    """
    # Inicializados no init:
    pontos_internos = None
    pontos_paredes = None
    fontes = None
    granularidade = None
    # Setados ao procurar os pontos internos (função procurar_pontos_internos):
    origem = None
    poligono = None

    def __init__(self, granularidade: Union[float, int]):
        self.pontos_internos = set()
        self.pontos_paredes = list()
        self.fontes = list()

        if not isinstance(granularidade, (float, int)):
            raise Exception("Informe a granularidade do tipo float ou int.")
        self.granularidade = granularidade

    def adicionar_parede(self, *pontos: Union[Ponto, List[Union[float, int]]]):
        """
        Adiciona uma lista de pontos (que é uma parede) à lista de paredes.

        A planta lembra de todas paredes que a definem.
        É importante saber quais são as paredes porque é preciso saber se um determinado
        feixe, que surge numa fonte e vai até um ponto, atravessa paredes ou não.
        """

        """
        ABAIXO, UM BUCADO DE CHECAGEM DE TIPOS!
        """
        if len(pontos) < 2:
            raise Exception("Ao adicionar uma parede, informe mais pontos! Lembre que uma parede é uma linha.")

        for ponto in pontos:
            # vamos verificar todos itens
            if isinstance(ponto, Ponto):
                # é ponto, sem problemas
                pass
            elif not isinstance(ponto, list):
                # não é ponto nem lista: problemas!
                ex = """
                Passe pontos separados por vírgula.
                Exemplo: adicionar_parede(Ponto(1,1), Ponto(0,0))
                ou adicionar_parede([1,1], [0,0])"""
                raise Exception(ex)
            elif len(ponto) < 2:
                # não é ponto, mas é lista e não tem pelo menos 2 itens? problemas!
                raise Exception("Ao adicionar uma parede, informe mais pontos! Lembre que uma parede é uma linha.")
            else:
                # não é ponto, é lista, tem pelo menos 2 itens: vamos ver se todos itens são numéricos!
                for x in ponto:
                    if not isinstance(x, (float, int)):
                        raise Exception("as coordenadas dos pontos precisam ser float ou int!")

        self.pontos_paredes.append(pontos)

    def simular_fontes(self, *fontes: List[Ponto]):
        """
        Avalia a intensidade do sinal em todos os pontos internos de acordo com as fontes informadas.

        Obs: cada ponto irá guardar sua nova intensidade.
        """

        # Se algum dos itens abaixo for none, chamamos a função que os seta
        checks = (self.pontos_internos, self.origem, self.poligono)
        if any([x is None for x in checks]):
            self.procurar_pontos_internos()

        # Setamos as fontes na propriedade da classe. Isso é pra que a função self.avaliar() possa
        # consultar quais são as fontes!
        self.fontes = fontes

        # A função abaixo seta o valor de cada ponto de acordo com as fontes.
        for ponto in self.pontos_internos:
            self.avaliar(ponto)


    def procurar_pontos_internos(self):
        """
        Escolhe um ponto de partida (ou seja, uma origem) e vai pulando de vizinho em vizinho até
        encontrar todos os pontos que estão dentro da planta. Se parece com um Breadth-First-Search.

        - A escolha da origem é assim: primeiro vejo se o ponto exatamente no meio dos limites da planta
        está dentro da planta.

        Se não tiver, eu vou gerar pontos aleatórios dentro dos limites da planta até um cair
        dentro da planta.

        - Esta é a função que gera o polígono da planta. O polígono é construído com base nas pontas
        das paredes. Também, o polígono é o que usamos pra dizer se um ponto está dentro ou fora
        da planta.
        """

        """
        SETANDO POLÍGONO DA PLANTA
        """
        # Pegando todos os pontos de todas paredes
        pontos_paredes = []
        for parede in self.pontos_paredes:
            pontos_paredes.extend(parede)

        # Pegando a casca convexa que é formada por esses pontos, e formando o polígono
        self.poligono = MultiPoint(pontos_paredes).convex_hull

        """
        ACHANDO A ORIGEM
        """
        # Achando o ponto central dentro dos limites da planta
        minx, miny, maxx, maxy = self.poligono.bounds

        origem = [
            media(minx, maxx),
            media(miny, maxy)
        ]
        origem = Ponto(*origem)

        if self.poligono.contains(origem):
            self.origem = origem

        else:
            self.origem = ponto_aleatorio(self.poligono)

        # Eu considero a origem como ponto interno!
        self.pontos_internos.add(self.origem)

        """
        BUSCANDO TODOS PONTOS EM TORNO DA ORIGEM, DENTRO DO POLÍGONO
        """
        self.origem.calcular_vizinhos(self.granularidade)
        fifo = fila(self.origem.vizinhos)

        while fifo:
            novo_ponto = fifo.popleft()

            if not self.poligono.contains(novo_ponto):
                # Se o ponto atual está fora da planta, ignore-o
                continue

            if novo_ponto in self.pontos_internos:
                # Se o ponto atual está dentro da planta e já foi visitado, ignore-o
                continue

            # Adiciono o ponto atual
            self.pontos_internos.add(novo_ponto)

            # Acrescento seus vizinhos na fila para serem verificados
            fifo.extend(novo_ponto.calcular_vizinhos(self.granularidade))

    def encontrar(self, p: Union[Ponto, List[Union[float, int]]]):
        """
        Retorna qual é o ponto correspondente às coordenadas passadas.

        Já que a área dentro da planta foi "discretizada", se você me der um ponto qualquer, eu te digo
        qual é o ponto correspondente na discretização que foi feita a partir da granularidade passada.

        Observação: nem sempre retorna qual o ponto discreto mais próximo, porque sempre arredondo as
        coordenadas pra baixo!
        """

        if isinstance(p, Ponto):
            pass
        elif not isinstance(p, list):
            # não é ponto nem lista: problemas!
            raise Exception("Informe o ponto como um objeto Ponto ou lista de coordenadas")
        elif len(p) < 2:
            # não é ponto, mas é lista e não tem pelo menos 2 itens? problemas!
            raise Exception("Informe o ponto com todas suas coordenadas!")
        else:
            for x in p:
                # não é ponto, é lista, tem pelo menos 2 itens: vamos ver se todos itens são numéricos!
                if not isinstance(x, (float, int)):
                    raise Exception("As coordenadas do ponto precisam ser float ou int!")
            p = Ponto(*p)

        # quantas "granularidades" inteiras temos da origem até o ponto, no eixo x?
        delta_x = int((p.x - self.origem.x) / self.granularidade)
        # quantas "granularidades" inteiras temos da origem até o ponto, no eixo y?
        delta_y = int((p.y - self.origem.y) / self.granularidade)

        estimativa = [
            self.origem.x + delta_x * self.granularidade,
            self.origem.y + delta_y * self.granularidade
        ]

        estimativa = Ponto(*estimativa)

        if self.poligono.contains(estimativa):
            return estimativa
        return None

    def avaliar(self, p: Ponto):
        """
        Essa função só serve para chamar para a função que vai realizar o cálculo.

        Isso serve para podermos ter várias funções de cálculo,e poder trocar entre elas facilmente.
        O resto do código chama essa função (avaliar). Então basta mudar aqui e já era.

        Toda função de cálculo só pode receber um parâmetro: um ponto.
        """

        if not isinstance(p, Ponto):
            raise Exception("A função de avaliar deve receber um objeto Ponto como parâmetro.")

        return self.avaliar_perda_paredes(p)

    def avaliar_aleatoriamente(self, p: Ponto):
        """
        Retorna simplesmente um número aleatório, só pra brincar
        """
        return random.random()

    def avaliar_distancia_simples(self, p: Ponto):
        """
        Retorna a distância entre o ponto e a origem. Só pra brincar
        """

        return distancia_entre_pontos(p, self.origem)

    def avaliar_perda_paredes(self, p: Ponto):
        """
        Retorna a quantidade de paredes que o sinal do roteador intercepta até chegar no ponto p.
        """
        fonte = self.fontes[0]
        intersecoes = []
        for parede in self.pontos_paredes:
            if line_intersection(parede, [fonte, p]):
                intersecoes.append(parede)
        return intersecoes


if __name__ == "__main__":
    print("LEMBRETES:")
    print("o cromossomo precisa conhecer a planta!")
    print("lembre de definir a granularidade como uma variável nas configurações.\n\n")

    planta = Planta(2)
    planta.adicionar_parede(Ponto(0, 10), Ponto(5, 10))
    planta.adicionar_parede(Ponto(5, 10), Ponto(5, 0))
    planta.adicionar_parede(Ponto(5, 0), Ponto(0, 0))
    planta.adicionar_parede(Ponto(0, 0), Ponto(0, 10))
    planta.adicionar_parede(Ponto(0, 10), Ponto(5, 0))

    print("pontos internos (antes de calcular): ", planta.pontos_internos)
    planta.procurar_pontos_internos()
    print("pontos internos: ", planta.pontos_internos)

    planta.simular_fontes(Ponto(2,8))

    print("resultado de avaliar() passando a origem:", planta.avaliar(planta.origem))


"""
PSEUDOCÓDIGO DE INSPIRAÇÃO
p = Planta()

p.adicionarParede(p1, p2)
p.adicionarParede(p1, p2)
p.adicionarParede(p1, p2)
p.adicionarParede(p1, p2)

Cromossomo.setPlanta(p)


''' gerar
return choices(planta.pontos_internos, k=k)

''' avaliar
planta.definirFontes(*self.genes) # self.genes = [p1, p2]
return min([x.valor for x in planta.pontos_internos])

''' mutacionar
novas_fontes = []
for fonte in cromossomo.genes:
    vizinho_aleatorio = choice(fonte.vizinhos)
    novas_fontes.append(fonte.vizinhos[vizinho_aleatorio])

return novas_fontes

''' reproduzir
novas_fontes = []
for par_fontes in zip(pai.genes, mae.genes):
    margem1 = ...
    margem2 = ...

    sinal = ...

    nova_fonte1 = ...
    nova_fonte2 = ...

    novas_fontes.append((self.encontrar(nova_fonte1),self.encontrar(nova_fonte1)))

return novas_fontes
"""
