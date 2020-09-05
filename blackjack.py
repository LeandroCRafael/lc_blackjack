import random


def cria_baralho(num_baralhos=1):
    '''
    Cria baralho

    :param num_baralhos: número de baralhos para construir (opcional,
        padrão 1)
    '''
    naipe = ['A', 'J', 'Q', 'K'] + list(range(2, 11))
    baralho = 4 * naipe
    return num_baralhos * baralho


def jogada(id_jogador, lista_ativos, lista_pontuacoes, baralho):
    '''
    Processa jogadas.

    :param id_jogador: identificador do jogador
    :param lista_ativos: lista para controlar situação dos jogadores
        (True para ativo, False para inativo)
    :param lista_pontuacoes: lista para controlar pontuações dos 
        jogadores
    :param baralho: lista para representar o baralho
    '''
    msg = 'Deseja comprar jogador {} (s/n)? '.format(id_jogador + 1)

    if input(msg).lower() != 's':
        lista_ativos[id_jogador] = False
    else:
        ponto_carta = sorteio_carta(baralho)
        lista_pontuacoes[id_jogador] += ponto_carta
        msg_base = '\tNova pontuação do jogador {}: {}'
        print(msg_base.format(id_jogador + 1, lista_pontuacoes[id_jogador]))
        

def sorteio_carta(baralho):
    '''
    Sorteia cartas e retorna a pontuação.

    :param baralho: lista para representar o baralho
    :return: pontuação da carta sorteada
    '''
    # Sorteando uma posição para recuperar e remover uma carta do baralho
    posicao_sort = random.randint(0, len(baralho) - 1)
    carta = baralho.pop(posicao_sort)
    
    # Tenta converter a carta para inteiro...
    try:
        pontos_carta = int(carta)
    except ValueError:
        # Caso a carta seja figura (A, J, Q, K)...
        if carta == 'A':
            pontos_carta = 1
        else:
            pontos_carta = 10

    return pontos_carta


def validacao(lista_pontuacoes, lista_ativos):
    '''
    Valida pontuação dos jogadores.

    :param lista_pontuacoes: lista para controlar pontuações dos 
        jogadores
    :param lista_ativos: lista para controlar situação dos jogadores
        (True para ativo, False para inativo)
    :return: caso algum ganhador, retorna não vazia
    '''
    lista_ganhadores = []

    for indice_jog, situacao_jog in enumerate(lista_ativos):
        # Se o jogador da iteração está inativo, o ignora.
        if not situacao_jog:
            continue

        # Recupera a pontuação
        pontuacao_jog = lista_pontuacoes[indice_jog]

        # Torna o jogador inativo caso tenha alcançado ou estourado 21
        if pontuacao_jog >= 21:
            lista_ativos[indice_jog] = False

    # Verifique o link abaixo para ver mais sobre precedência de 
    #   operadores!
    # https://docs.python.org/3/reference/expressions.html
    if True not in lista_ativos:
        # Caso não exista jogador ativo, busca a maior pontuação válida
        # e os jogadores correspondentes.
        max_pontuacao = max([pontuacao 
                             for pontuacao in lista_pontuacoes 
                             if pontuacao <= 21])

        for id_jog, pontuacao_jog in enumerate(lista_pontuacoes):
            if pontuacao_jog == max_pontuacao:
                lista_ganhadores.append(id_jog)

    return lista_ganhadores


def blackjack():
    '''Função principal.'''
    num_jogadores = int(input('Informe o número de jogadores: '))
    
    # Valida número de jogadores.
    while num_jogadores < 1:
        print('Precisamos de pelo menos um jogador!')
        num_jogadores = int(input('Informe o número de jogadores: '))    

    lista_nomes = []
    contador = 0
    msg = 'Informe o nome do {}o jogador: '

    while contador < num_jogadores:
        contador += 1
        nome = input(msg.format(contador))
        lista_nomes.append(nome)

    lista_ativos = [True] * num_jogadores
    lista_pontuacoes = [0] * num_jogadores

    num_baralhos = int(input('Informe o número de baralhos: '))
    
    # Valida número de baralhos.
    while num_baralhos < 1:
        print('Precisamos de pelo menos um baralho!')
        num_baralhos = int(input('Informe o número de baralhos: '))    

    baralho = cria_baralho(num_baralhos)
    id_rodada = 1

    while True in lista_ativos:
        print('\t\tRODADA {}\n'.format(id_rodada))

        for id_jog, situacao_jog in enumerate(lista_ativos):
            if situacao_jog:
                jogada(id_jog, lista_ativos, lista_pontuacoes, baralho)

        ganhadores = validacao(lista_pontuacoes, lista_ativos)

        if ganhadores:
            for id_ganhador in ganhadores:
                nome_ganhador = lista_nomes[id_ganhador]
                print('\tParabéns, {}!'.format(nome_ganhador))

            return

        id_rodada += 1

    print('\tNão temos ganhadores! Mais sorte na próxima ;)')


if __name__ == '__main__':
    blackjack()
