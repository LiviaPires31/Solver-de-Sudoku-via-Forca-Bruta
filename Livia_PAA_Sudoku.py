import os
import sys

# Função para ler o tabuleiro do Sudoku de um arquivo
def ler_tabuleiro(nome_arquivo):
    # Abre o arquivo para leitura
    with open(nome_arquivo, 'r') as arquivo:
        # Lê todas as linhas do arquivo
        linhas_arquivo = arquivo.readlines()
    tabuleiro_sudoku = []
    # Para cada linha no arquivo
    for linha in linhas_arquivo:
        # Ignora linhas em branco
        if linha.strip():
            # Converte a linha em uma lista de inteiros e adiciona ao tabuleiro
            tabuleiro_sudoku.append(list(map(int, linha.strip().split())))
    return tabuleiro_sudoku

# Função para verificar se um número é válido em uma determinada posição do tabuleiro
def numero_valido(tabuleiro, linha, coluna, numero):
    # Verifica se o número já está na mesma linha ou coluna
    for i in range(9):
        if tabuleiro[linha][i] == numero and coluna != i:
            return False
        if tabuleiro[i][coluna] == numero and linha != i:
            return False

    # Verifica se o número já está no quadrado 3x3
    for i in range(linha // 3 * 3, linha // 3 * 3 + 3):
        for j in range(coluna // 3 * 3, coluna // 3 * 3 + 3):
            if tabuleiro[i][j] == numero and (i, j) != (linha, coluna):
                return False

    # Retorna true se válido
    return True

def sudoku_valido(tabuleiro_sudoku):
    # Percorre todas as células do tabuleiro
    for i in range(81):
        # Verifica se a célula não está vazia (diferente de 0)
        if tabuleiro_sudoku[i // 9][i % 9] != 0:
            # Chama a função numero_valido para verificar se o número na célula é válido
            if not numero_valido(tabuleiro_sudoku, i // 9, i % 9, tabuleiro_sudoku[i // 9][i % 9]):
                # Se o número não for válido, o tabuleiro não é válido
                return False
    
    # Retorna true se válido
    return True

# Função para resolver o Sudoku usando backtracking
def resolver_sudoku(tabuleiro, linha=0, coluna=0):
    # Se todas as linhas foram preenchidas, o Sudoku foi resolvido
    if linha == 9:
        return True
    # Se todas as colunas de uma linha foram preenchidas, passa para a próxima linha
    elif coluna == 9:
        return resolver_sudoku(tabuleiro, linha+1, 0)
    # Se a célula atual já está preenchida, passa para a próxima célula
    elif tabuleiro[linha][coluna] != 0:
        return resolver_sudoku(tabuleiro, linha, coluna+1)
    else:
        # Tenta todos os números de 1 a 9 na célula atual
        for numero in range(1, 10):
            if numero_valido(tabuleiro, linha, coluna, numero):
                tabuleiro[linha][coluna] = numero
                # Se a solução é válida até agora, continua resolvendo o resto do Sudoku
                if resolver_sudoku(tabuleiro, linha, coluna+1):
                    return True
                # Se a solução não é válida, desfaz a última escolha e tenta o próximo número
                tabuleiro[linha][coluna] = 0
        # Se nenhum número é válido na célula atual, retorna False para voltar à última escolha válida (backtracking)
        return False

while True:
    # Solicita o nome do arquivo ao usuário
    nome_arquivo = input("\n Qual o nome do arquivo? (-1 para sair) ")

    # Se o usuário digitar -1, encerra o programa
    if nome_arquivo == '-1':
        break

    # Tenta ler o tabuleiro do arquivo especificado pelo usuário
    try:
        tabuleiro_sudoku = ler_tabuleiro(nome_arquivo)
    except FileNotFoundError:
        print(f'O arquivo {nome_arquivo} não foi encontrado.')
        continue

    if not sudoku_valido:
        print(f'O arquivo {nome_arquivo} não representa um Sudoku válido.')
        continue

    # Chama a função resolver_sudoku para resolver o Sudoku
    resolver_sudoku(tabuleiro_sudoku)

    # Imprime o nome do arquivo e o tabuleiro resolvido no terminal
    print(f'\n Solução para {nome_arquivo}: \n')
    for linha in tabuleiro_sudoku:
        print(' '.join(str(x) for x in linha))
