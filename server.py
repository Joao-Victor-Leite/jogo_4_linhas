from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from port import *
import sys

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

players = {'X': None, 
           'O': None}

turn_check = {'player': 0, 
              'winner': False}


def create_board():
    """
    Cria e retorna um novo tabuleiro de jogo.

    Retorna:
        list: Um tabuleiro 9x9 vazio.
    """

    return [[" " for _ in range(9)] for _ in range(9)]

board = create_board()

def draw_board():
    """
    Desenha o tabuleiro de jogo atual.

    Retorna:
        list: Uma lista de strings que representam o tabuleiro atual.
    """

    board_representation = []

    for linha in board:
        board_representation.append("|" + "|".join([" " + cell + " " for cell in linha]) + "|")
    
    board_representation.append("+---" * 9 + "+")
    
    return board_representation

def set_player_move(column, player):
    """
    Registra o movimento de um jogador no tabuleiro.

    Parâmetros:
        column (int): O índice da coluna onde o jogador deseja fazer o movimento.
        player (str): O símbolo do jogador ('X' ou 'O').

    Retorna:
        bool: True se o movimento foi bem-sucedido, False caso contrário.
    """

    for line in reversed(range(9)):
        if board[line][column] == " ":
            board[line][column] = player
            return True
    return False

def get_turn_check():
    """
    Retorna o turno atual do jogo.

    Retorna:
        int: O identificador do jogador que deve realizar o próximo movimento (0 ou 1).
    """
    return turn_check['player']

def set_turn_check():
    """
    Alterna o turno do jogo entre os jogadores.
    """

    if turn_check['player'] == 0:
        turn_check['player'] = 1
    else:
        turn_check['player'] = 0
    return

def check_victory(player): 
    """
    Verifica se um jogador venceu o jogo seja por linha, coluna ou diagonal.

    Parâmetros:
        player (str): O símbolo do jogador ('X' ou 'O').

    Retorna:
        bool: True se o jogador venceu, False caso contrário.
    """

    lines = len(board)
    columns = len(board[0])
    
    # Verifica linhas
    for line in range(lines):
        for column in range(columns - 3):
            if board[line][column] == player and all(board[line][column + i] == player for i in range(4)):
                return True
    
    # Verifica colunas
    for column in range(columns):
        for linha in range(lines - 3):
            if board[line][column] == player and all(board[line + i][column] == player for i in range(4)):
                return True
    
    # Verifica diagonais (positivas e negativas)
    for line in range(lines - 3):
        for column in range(columns - 3):
            if board[line][column] == player and all(board[line + i][column + i] == player for i in range(4)):
                return True
            if board[line + 3][column] == player and all(board[line + 3 - i][column + i] == player for i in range(4)):
                return True
    
    return False

def get_game_status():
    """
    Retorna o status atual do jogo.

    Retorna:
        bool: True se o jogo terminou com um vencedor, False caso contrário.
    """
    return turn_check['winner']

def set_game_status():
    """
    Define o status do jogo como terminado.
    """

    turn_check['winner'] = True
    return True

def player_validation(player_id, player_symbol):
    """
    Valida a conexão de um jogador, verificando o símbolo escolhido e se o jogador já está conectado.

    Parâmetros:
        player_id (str): O identificador do jogador.
        player_symbol (str): O símbolo escolhido pelo jogador ('X' ou 'O').

    Retorna:
        bool: True se o jogador for validado com sucesso, False caso contrário.
    """
    global players

    # Verifica se o símbolo é válido
    if player_symbol.upper() not in ['X', 'O']:
        return False

    # Verifica se o jogador já está conectado
    if players[player_symbol] is not None:
        return False  # Já existe um jogador com este símbolo

    # Atribui o jogador ao símbolo
    players[player_symbol] = player_id

    # Verifica se ambos os jogadores estão conectados
    if all(players.values()):
        return True  # Ambos os jogadores estão prontos
    
    return True
    

with SimpleXMLRPCServer((HOST, PORT), requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()

    server.register_function(create_board, "create_board")
    server.register_function(draw_board, "draw_board")
    server.register_function(set_player_move, "set_player_move")
    server.register_function(get_turn_check, "get_turn_check")
    server.register_function(set_turn_check, "set_turn_check")
    server.register_function(check_victory, "check_victory")
    server.register_function(get_game_status, "get_game_status")
    server.register_function(set_game_status, "set_game_status")
    server.register_function(player_validation, "player_validation")

    print(f'Serving XML-RPC on {HOST} port {PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)

