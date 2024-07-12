import random
import string
import sqlite3
import PySimpleGUI as sg

# Conexão ao banco de dados
conn = sqlite3.connect('vales.db')
cursor = conn.cursor()

# Variaveis
nome = ""
status = "OFF"
chave2 = "teste de chave"

# Função para gerar chave aleatória
def generate_key():
    key = '-'.join(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5)) for _ in range(4))
    return key

# Gera 1 chave aleatória e adiciona ao banco de dados
def salvar_key():
    global chave2
    chave = generate_key()
    chave2 = chave
    cursor.execute("INSERT INTO VALES (NOME, CHAVE, STATUS) VALUES (?,?,?)", (nome, chave, "ativo"))
    print(f"Chave adicionada: {chave}")

layout = [
    [sg.Text("Nome do vale")],
    [sg.InputText(key="nome")],
    [sg.Text('Sua chave aleatória:')],
    [sg.Text(key='key', size=(50, 1))],
    [sg.Button("Gerar"), sg.Button("Sair"), sg.Button("Limpar")]
]
# Criação da janela
window = sg.Window("Vales", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Sair":
        break
    elif event == "Gerar":
        nome = values['nome']
        print(f"Nome salvo: {nome}")
        salvar_key()
        window['key'].update(chave2)  # Atualiza o output do GUI
    elif event == "Limpar":
        window["nome"].update('')

# Commita as alterações
conn.commit()

# Fecha a conexão
conn.close()