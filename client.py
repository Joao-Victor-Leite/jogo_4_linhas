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
    time.sleep(10)
else:
    print("Não foi possível validar. Talvez o símbolo já tenha sido escolhido ou a entrada seja inválida.")
    sys.exit(0)
""" 
while TRUE:
jogador 0 input --> server
.......
verifica o turno
se for entra no loop tentando fazer a jogada
jogador 1 input --> server


faco a jogada
entra no loop
so sai quando for a jogada dnv

"""

teste = proxy.draw_board()
for linha in teste:
    print(linha)

while True:
    player_input = int(input(f"Jogador, escolha uma coluna (0-8): "))
    if proxy.set_player_move(player_input, player_symbol):
        teste_2 = proxy.draw_board()
        for linha in teste_2:
            print(linha)

        if proxy.check_victory(player_symbol):
            print("Jogador venceu!")
            break
    else:
        print("Coluna cheia, escolha outra.")

"""     if all(board[line][column] != " " for line in range(9) for column in range(9)):
        print("Empate!")
        break """

