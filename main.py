from tipos_cromossomos import *


if __name__ == "__main__":
    """
    CONFIGURAÇÕES
    """
    # Quantos indivíduos vamos gerar
    TAM_POPULACAO = 60
    # A geração, quantos cromossomos passam pela seleção
    QTD_SELECIONADOS = 12
    # Quantas gerações queremos ter
    NUM_GERACOES = 150
    # Método de seleção
    SELECAO = Selecoes.TORNEIO
    # Método de reprodução
    REPRODUCAO = 0 # 0 significa "default"
    # Chance de mutação
    CHANCE_MUTACAO = 0.03
    OBJETIVO = Objetivos.MINIMIZAR
    # Qual classe se responsabilizará pelo manuseio dos cromossomos
    classe_cromossomo = CromossomoQuadraticoDecimal
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

        cromossomos = [classe_cromossomo.mutacionar(filho, CHANCE_MUTACAO) for filho in cromossomos_filhos]

    for cromossomo in cromossomos:
        print(cromossomo)
