import PySimpleGUI as sg
import sqlite3


# Conectando no Banco de Dados
conn = sqlite3.connect('vales.db')
cursor = conn.cursor()

conn = sqlite3.connect('vales.db')
cursor = conn.cursor()
cursor.execute('SELECT NOME FROM VALES')
items = cursor.fetchall()
conn.close()

# Busca o codigo digitado no banco de dados
def buscar_codigo_sql(codigo_digitado):
    conn = sqlite3.connect('vales.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VALES WHERE CHAVE = ?", (codigo_digitado,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def atualizar_status_sql(codigo_digitado):
    conn = sqlite3.connect('vales.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE VALES SET status = 'inativo' WHERE chave = ?", (codigo_digitado,))
    conn.commit()
    conn.close()

# Retorna o nome do vale referente ao codigo digitado
def buscar_nome_sql(codigo_digitado):
    conn = sqlite3.connect('vales.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM VALES WHERE chave = ?", (codigo_digitado,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]  # Retorna o nome
    else:
        return None  # Retorna none se não encontrar nada

# Retorna o status do vale referente ao codigo digitado
def buscar_status_sql(codigo_digitado):
    conn = sqlite3.connect('vales.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM VALES WHERE chave = ?", (codigo_digitado,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]  # Retorna o valor do status
    else:
        return None  # Retorna none se não encontrar nada

# Janela do menu principal
def janela_menu():
    janela_menu_texto = [
        [sg.Text(f'Mozinho lindo', font=('Helvetica', 16, 'bold'))],
    ]
    janela_menu = [
        [sg.Canvas(size=(104, 104), key='canvas', background_color='red'), sg.Column(janela_menu_texto)],
        [sg.Text()],
        [sg.Button('Resgatar vales', key='botao_resgatar_vales', size=(15, 2)), sg.Button('Visualizar vales resgatados', size=(15, 2), key='botao_visualizar_resgatados'), sg.Button('Fechar', size=(15, 2), key='botao_fechar')],
    ]
    menu = sg.Window('menu', layout=janela_menu, size=(427, 210))
    return menu

# Janela do listbox de resgatados
def janela_resgatados():
    layout = [
        [sg.Listbox(values=[item[0] for item in items], size=(40, 14), key='listbox', font=('Helvetica', 16))],
        [sg.Push(), sg.Button('Voltar', key='botao_voltar_resgatados')]
    ]
    window = sg.Window('items', layout, size=(400, 400))
    return window

# Janela para resgatar os codigos
def janela_resgatar():
    layout = [
        [sg.Text("Vales")],
        [sg.InputText(key="input")],
        [sg.Button("Resgatar"), sg.Button("Sair"), sg.Button("Limpar"), sg.Button("Voltar")]
    ]
    # Criação da janela
    window = sg.Window("Vales", layout)
    return window

# Loop do código principal
while True:
    janela = janela_menu()
    event, value = janela.read()

    if event == sg.WINDOW_CLOSED or event == "botao_fechar":
        break

    elif event == "botao_resgatar_vales":
        janela.close()
        janela = janela_resgatar()

        while True:
            event, value = janela.read()

            if event == sg.WINDOW_CLOSED or event == "Sair":
                janela.close()
                janela = janela_menu()
                break

            elif event == "Resgatar":
                codigo_digitado = value["input"]

                if buscar_codigo_sql(codigo_digitado):
                    status_vale = buscar_status_sql(codigo_digitado)
                    if status_vale == "ativo":
                        nomeVale = buscar_nome_sql(codigo_digitado)
                        if nomeVale:
                            sg.popup(f"Nome: {nomeVale}")
                            atualizar_status_sql(codigo_digitado)  # Chamada da função para atualizar o status
                            janela.close()

                        else:
                            sg.popup("Erro ao buscar nome!")
                            janela["input"].update('')
                    else:
                        sg.popup("Vale inativo!")

                else:
                    sg.popup("Código incorreto!")

            elif event == "Limpar":
                janela["input"].update('')

            elif event == "Voltar":
                janela.close()
                break

    elif event == "botao_visualizar_resgatados":
        janela.close()
        janela = janela_resgatados()
        event, value = janela.read()

        if event == sg.WINDOW_CLOSED:
            break

        elif event == "botao_voltar_resgatados":
            janela.close()


# Fechamento da janela
janela.close()

# Comando para compilar o arquivo .py para .exe:
# pyinstaller --onefile -w vales.py
# pyinstaller -> nome da ferramenta
# --onefile -> agrupa tudo em um unico .exe
# -w -> caso tenha alguma interface gráfica
# vales.py -> nome do arquivo .py que será compilado