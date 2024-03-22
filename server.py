from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from port import *
import sys

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

players = {'X': None, 'O': None}
""" a = {symbol: None, winner: False} """



def create_board(): #done
    return [[" " for _ in range(9)] for _ in range(9)]

board = create_board()

def draw_board(): #done
    # Cria uma lista para armazenar as linhas do tabuleiro, incluindo os separadores
    board_representation = []

    for linha in board:
        # Constrói a representação da linha atual do board e adiciona à representação
        board_representation.append("|" + "|".join([" " + cell + " " for cell in linha]) + "|")
        
        # Adiciona o separador de linhas após cada linha do board
    
    board_representation.append("+---" * 9 + "+")
    # Retorna a representação do tabuleiro como uma lista de strings
    return board_representation


def set_player_move(column, player):
    #Função para registrar o movimento do jogador
    for line in reversed(range(9)):
        if board[line][column] == " ":
            board[line][column] = player
            return True
    return False


def check_victory(player): #done
    # Verifica linhas, colunas e diagonais para encontrar 4 em linha
    linhas = len(board)
    colunas = len(board[0])
    
    # Verifica linhas
    for linha in range(linhas):
        for coluna in range(colunas - 3):
            if board[linha][coluna] == player and all(board[linha][coluna + i] == player for i in range(4)):
                return True
    
    # Verifica colunas
    for coluna in range(colunas):
        for linha in range(linhas - 3):
            if board[linha][coluna] == player and all(board[linha + i][coluna] == player for i in range(4)):
                return True
    
    # Verifica diagonais (positivas e negativas)
    for linha in range(linhas - 3):
        for coluna in range(colunas - 3):
            if board[linha][coluna] == player and all(board[linha + i][coluna + i] == player for i in range(4)):
                return True
            if board[linha + 3][coluna] == player and all(board[linha + 3 - i][coluna + i] == player for i in range(4)):
                return True
    
    return False


def player_validation(player_id, player_symbol):
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
    else:
        return True  # Jogador validado, mas aguardando o outro jogador


with SimpleXMLRPCServer((HOST,PORT), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    server.register_function(create_board, "create_board")
    server.register_function(draw_board, "draw_board")
    server.register_function(player_validation, "player_validation")
    server.register_function(set_player_move, "set_player_move")
    server.register_function(check_victory, "check_victory")

    print(f'Serving XML-RPC on {HOST} port {PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)

