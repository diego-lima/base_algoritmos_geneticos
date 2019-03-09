

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
    def gerar():
        """Gera um cromossomo aleatoriamente"""
        raise NotImplementedError("Esse método deve ser definido pela classe herdeira")

    @staticmethod
    def avaliar(cromossomo):
        """Avalia a aptidão do cromossomo.
        Essa função deve ser sobrescrita em cada problema específico."""
        cromossomo.gerar()
        raise NotImplementedError("Essa função deve ser implementada especificamete para seu problema")

    @staticmethod
    def mutacionar(cromossomo):
        """Modifica aleatoriamente um gene"""
        raise NotImplementedError("Esse método deve ser definido pela classe herdeira")

    @staticmethod
    def reproduzir(pai, mae):
        """Combina os genes dos dois cromossoos para gera um novo"""
        raise NotImplementedError("Esse método deve ser definido pela classe herdeira")

    def __repr__(self):
        return self.genes
