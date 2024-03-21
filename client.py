import xmlrpc.client 
import time
import sys
from port import *

proxy = xmlrpc.client.ServerProxy("http://localhost:8080")


player_id = int(input("Você é o jogador 0 ou 1? "))
player_symbol = input("Você quer ser o jogador X ou O? ")

validado = proxy.player_validation(player_id, player_symbol)
if validado:
    print("Você foi validado com sucesso. Aguardando outro jogador...")
else:
    print("Não foi possível validar. Talvez o símbolo já tenha sido escolhido ou a entrada seja inválida.")
    sys.exit(0)


board = proxy.create_board()

while True:
    proxy.draw_board(board)
    player_input = proxy.get_player_move(player_symbol)
    if proxy.set_player_move(board, player_input, player_symbol):
        if proxy.check_victory(board, player_symbol):
            proxy.draw_board(board)
            print(f"Jogador venceu!")
            break
    else:
        print("Coluna cheia, escolha outra.")

    if all(board[line][column] != " " for line in range(9) for column in range(9)):
        print("Empate!")
        break



""" while True:
    estado = proxy.obter_estado_jogo()
    
    # Verifica se o jogo terminou
    if estado["vencedor"] is not None:
        print("Jogo terminou!")
        break
    
    # Verifica de quem é a vez
    if estado["turno"] == id_jogador:
        coluna = int(input("Sua vez. Escolha uma coluna: "))
        proxy.registrar_jogada(coluna, id_jogador)
    else:
        print("Aguardando a jogada do outro jogador...")
        time.sleep(1)  # Aguarda um pouco antes de verificar novamente """