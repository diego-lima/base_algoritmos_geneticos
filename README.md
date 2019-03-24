# base_algoritmos_geneticos
Implementação base de algoritmos genéticos

No arquivo [classes_ga.py](https://github.com/diego-lima/base_algoritmos_geneticos/blob/master/classes_ga.py), a classe Cromossomo define os métodos básicos que devem ser implementados no geral. 

Para um problema específico, é preciso herdar dessa classe, definindo os métodos estáticos `gerar`, `avaliar` `mutacionar` e `reproduzir`. 
Definidos esses métodos, o código em [main.py](https://github.com/diego-lima/base_algoritmos_geneticos/blob/master/main.py) irá cuidar do processo de gerar população inicial, selecionar, reproduzir, mutacionar.  

Nesse mesmo arquivo, também estão algumas funções auxiliares, como roleta e torneio.

No arquivo [tipos_cromossomos.py](https://github.com/diego-lima/base_algoritmos_geneticos/blob/master/tipos_cromossomos.py), estão as classes que herdam de Cromossomo e definem o comportamento específico para cada problema.

O ponto de partida é o arquivo [main.py](https://github.com/diego-lima/base_algoritmos_geneticos/blob/master/main.py)
