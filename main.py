from tipos_cromossomos import *


if __name__ == "__main__":
    """
    CONFIGURAÇÕES
    """
    # Quantos indivíduos vamos gerar
    TAM_POPULACAO = 12
    # A geração, quantos cromossomos passam pela seleção
    QTD_SELECIONADOS = 5
    # Quantas gerações queremos ter
    NUM_GERACOES = 25
    # Método de seleção
    SELECAO = Selecoes.ROLETA
    # Método de reprodução
    REPRODUCAO = 0 # 0 significa "default"
    # Chance de mutação
    CHANCE_MUTACAO = 0.03
    # OBJETIVO = Objetivos.MINIMIZAR
    # Qual classe se responsabilizará pelo manuseio dos cromossomos
    classe_cromossomo = CromossomoPotencia

    """
    SETUP DA CLASSE DE CROMOSSOMO
    """
    GRANULARIDADE_PLANTA = 4
    QUANTIDADE_ROTEADORES = 1
    lado_quadrado = 20

    planta = Planta(GRANULARIDADE_PLANTA)
    """Estamos fazendo um quadrado de lado lado_quadrado, que a ponta inferior esquerda tá na origem"""
    planta.adicionar_parede(Ponto(0, lado_quadrado), Ponto(lado_quadrado, lado_quadrado))
    planta.adicionar_parede(Ponto(lado_quadrado, lado_quadrado), Ponto(lado_quadrado, 0))
    planta.adicionar_parede(Ponto(lado_quadrado, 0), Ponto(0, 0))
    planta.adicionar_parede(Ponto(0, 0), Ponto(0, lado_quadrado))

    planta.procurar_pontos_internos()
    print("Temos %d pontos internos." % len(planta.pontos_internos))
    CromossomoPotencia.planta = planta
    CromossomoPotencia.k = QUANTIDADE_ROTEADORES

    """
    TRIAGEM / PROCESSO
    """

    # Geramos TAM_POPULACAO cromossomos aleatoriamente
    cromossomos = [classe_cromossomo.gerar() for x in range(TAM_POPULACAO)]

    for _ in range(NUM_GERACOES):
        print(_)
        """Seleção"""
        if SELECAO == Selecoes.ROLETA:
            cromossomos_selecionados = sortear_roleta(cromossomos, classe_cromossomo.avaliar, QTD_SELECIONADOS)

        elif SELECAO == Selecoes.TORNEIO:
            cromossomos_selecionados = sortear_torneio(cromossomos, classe_cromossomo.avaliar, QTD_SELECIONADOS)

        else:
            # seleção completamente aleatória de QTD_SELECIONADOS entre os cromossomos
            cromossomos_selecionados = choices(cromossomos, k=QTD_SELECIONADOS)

        """Reprodução"""

        if REPRODUCAO == Reproducoes.CROSSOVER_1:
            cromossomos_filhos = []
            while len(cromossomos_filhos) < TAM_POPULACAO:
                # Faço uma roleta pra pegar dois pais aleatórios para gerar os filhos
                pais = sortear_torneio(cromossomos_selecionados, classe_cromossomo.avaliar, 2)
                cromossomos_filhos.extend(classe_cromossomo.reproduzir_crossover_1(*pais))

        else:
            # Chamo o método de reprodução default.
            cromossomos_filhos = []
            while len(cromossomos_filhos) < TAM_POPULACAO:
                # Faço uma roleta pra pegar dois pais aleatórios para gerar os filhos
                pais = sortear_torneio(cromossomos_selecionados, classe_cromossomo.avaliar, 2)
                cromossomos_filhos.extend(classe_cromossomo.reproduzir(*pais))

        """Mutação"""
        # chamamos a função mutacionar em cima de cada cromossomo que chegou até aqui.
        # essa funço já se encarrega em girar o dado pra ver se vai acontecer a mutação
        cromossomos = [classe_cromossomo.mutacionar(filho, CHANCE_MUTACAO) for filho in cromossomos_filhos]

    # fora do laço principal, vou printar todos os cromossomos, mostrando o gene e a aptidão
    for cromossomo in cromossomos:
        print(cromossomo)
