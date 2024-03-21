from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from port import *
import sys

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

players = {'X': None, 'O': None}

def create_board(): #done
    return [[" " for _ in range(9)] for _ in range(9)]

def draw_board(board): #done
    for linha in board:
        print("|" + "|".join(linha) + "|")

    # Imprime a base do board
    print("+--" * 6 + "+")

def set_player_move(board, column, player):
    #Função para registrar o movimento do jogador
    for line in reversed(range(9)):
        if board[line][column] == " ":
            board[line][column] = player
            return True
    return False

def get_player_move(player):
    player_input = int(input(f"Jogador {player}, escolha uma coluna (0-8): "))
    return player_input

def check_victory(board, player): #done
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


def player_validation(player_id, player_symbol):
    global players

     # Verifica se o símbolo é válido
    if player_symbol not in ['X', 'O']:
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
    server.register_function(draw_board, "draw_board", )
    server.register_function(player_validation, "player_validation")
    server.register_function(get_player_move, "get_player_move")
    server.register_function(set_player_move, "set_player_move")
    server.register_function(check_victory, "check_victory")

    print(f'Serving XML-RPC on {HOST} port {PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)


""" def start_game():
    board = create_board()
    player = 'x'

    while True:
        draw_board(board)
        player_input = get_player_move(player)
        if set_player_move(board, player_input, player):
            if check_victory(board, player):
                draw_board(board)
                print(f"Jogador venceu!")
                break
        else:
            print("Coluna cheia, escolja outra.")

        if all(board[line][column] != " " for line in range(9) for column in range(9)):
            print("Empate!")
            break
    return """