import xmlrpc.client 
import time
import sys
import os
from port import *

proxy = xmlrpc.client.ServerProxy("http://localhost:8080", allow_none=True)

# Recebe o identificador e simbolo do jogador
player_id = int(input("Você é o jogador 0 ou 1? "))
player_symbol = input("Você quer ser o jogador X ou O? ")

# Valida o jogador no servidor
validated = proxy.player_validation(player_id, player_symbol)
if validated:
    print("Você foi validado com sucesso. Aguardando outro jogador...")
    time.sleep(10)
else:
    print("Não foi possível validar. Talvez o símbolo já tenha sido escolhido ou a entrada seja inválida.")
    sys.exit(0)

while True:
    # Verifica se um jogador já ganhou
    if proxy.get_game_status():
        break

    os.system('clear')

    # Verifica se é o turno do jogador atual
    if proxy.get_turn_check() == player_id:

        # Mostra o tabuleiro
        current_board = proxy.draw_board()
        for linha in current_board:
            print(linha)

        player_input = int(input(f"Jogador, escolha uma coluna (0-8): "))

        # Valida se a jogada foi feita com sucesso
        if proxy.set_player_move(player_input, player_symbol):
            
            # Verifica se o jogador atual ganhou a partida
            if proxy.check_victory(player_symbol):
                proxy.set_game_status()
                break

            # Altera o turno para o próximo jogador
            proxy.set_turn_check()

            # Mostra o tabuleiro
            current_board = proxy.draw_board()
            for linha in current_board:
                print(linha)

        else:
            print("Coluna cheia, escolha outra.")

# Mostra o tabuleiro
current_board = proxy.draw_board()
for linha in current_board:
    print(linha)

# Mostra uma mensagem para ambos os jogadores informando o vencedor
if proxy.get_game_status():
    player_winner = proxy.get_turn_check()
    print(f"Jogador {player_winner} venceu!")



