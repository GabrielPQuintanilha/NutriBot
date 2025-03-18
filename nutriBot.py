import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.chrome.options import Options
import requests

# --- To do --- #
# Identificar generos
# ---      --- #

chrome_options = Options()

# Adicionar a opção de rodar o Chrome em modo headless
chrome_options.add_argument("--headless")  # Roda o Chrome sem abrir a janela gráfica
chrome_options.add_argument("--disable-gpu")  # Desativa o uso de GPU, útil para o headless
chrome_options.add_argument("--no-sandbox")  # Para evitar problemas com o sandbox em alguns sistemas

# Criar uma instância do WebDriver com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)


def perguntaNovaConsulta():
    # funcao pra clicar no botao de "ver" caso apareca outra popup
    try:
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='swal2-content']/div[7]"))
        )
        botao_swal2 = driver.find_element(By.XPATH, "//*[@id='swal2-content']/div[7]")
        botao_swal2.click()
    except:
        pass

def loginNoSite():
    driver.get("https://pt.webdiet.com.br/painel/v4/pacientes.php")

    login_input = driver.find_element(By.ID, "emailLogin")
    senha_input = driver.find_element(By.ID, "senhaLogin")
    botao_login = driver.find_element(By.CLASS_NAME, "botao")
    ##botao_verPacientes = driver.find_element(By.LINK_TEXT, "Ver todos")

    login_input.send_keys("XXXX")
    senha_input.send_keys("XXXX")
    botao_login.click()

def verListaPaciente():
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Ver todos"))
    )
    botao_verPacientes = driver.find_element(By.LINK_TEXT, "Ver todos")

    botao_verPacientes.click()

def turnoDoDia():
    horario_atual = datetime.datetime.now().time()
    if horario_atual.hour>=12:
        saudacao = "Boa%20tarde!"
        return saudacao
    else:
        saudacao = "Bom%20dia!"
        return saudacao

def criarNomeSimplificado(nome):
    nome_parts = nome.split()
    #-1 representa o ultimo nome
    nome_simplificado = nome_parts[0]# + '%20' + nome_parts[-1]
    return nome_simplificado

def totalkidsOuNao(i):
    try:
        # identificar se o elemento aparece
        element= WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, f"//*[@id='pacientesPage']/div[{6+i}]/div[2]/div[3]//div[@class='tagEtiqueta']"))
        )

        #retira apenas o texto do elemento e tira espacos extra
        element_text = element.text.strip()  

        if element_text == "TotalKids":
            totalkids = "yes"
        else:
            totalkids = "no"
    except:
        totalkids = "no"
    return totalkids
    

def textoParaWhatsapp(nome_paciente_texto, totalkids):

    artigo = generoNome(nome_paciente_texto)

    if totalkids =="yes":
        return f"%20Como%20foi%20a%20semana%20d{artigo}%20{criarNomeSimplificado(nome_paciente_texto)}?"
        
    else:
        return f"%20Como%20foi%20a%20sua%20semana,%20{criarNomeSimplificado(nome_paciente_texto)}?"
        

def printNomeTelefone():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, "output.html")

    print("Diretório atual:", os.getcwd())
    # Abrindo o arquivo no modo 'w' para sobrescrever e começar um novo arquivo HTML
    with open(caminho_arquivo, "w") as file:
        # Começa o arquivo HTML com a estrutura básica
        file.write("<html><body style='text-align: center;'> <p style='font-size: 20px;'>PACIENTES DA ULTIMA SEMANA</p>\n")

        # ultimos 18 pacientes modificados
        for i in range(0, 18):
            # Aguardar o elemento estar clicável
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, f"fotoPerfil{i}"))
            )

            totalkids = totalkidsOuNao(i)

            # Encontrar e clicar no botão de imagem
            botao_imgPaciente = driver.find_element(By.ID, f"fotoPerfil{i}")
            botao_imgPaciente.click()

            # Fazer a consulta nova
            perguntaNovaConsulta()

            # Aguardar o conteúdo carregar
            driver.implicitly_wait(1)

            # Obter dados do modal
            modal_content = driver.find_elements(By.ID, "modal-content")
            nome_paciente = driver.find_element(By.ID, "nomeDadosFake")
            telefone_paciente = driver.find_element(By.ID, "telefoneDadosFake")

            nome_paciente_texto = nome_paciente.text
            telefone_paciente_texto = telefone_paciente.text
            telefone_paciente_texto = re.sub(r'\D', '', telefone_paciente_texto)
            
            # Adiciona as informações no arquivo HTML
            file.write(f"<p><strong>Nome:</strong> {nome_paciente_texto} | <strong>Link:</strong> <a href='https://web.whatsapp.com/send/?phone=55{telefone_paciente_texto}&text={turnoDoDia()}{textoParaWhatsapp(nome_paciente_texto, totalkids)}' target='_blank'>Whatsapp</a></p>\n")

            # Fechar o modal
            close_button = driver.find_element(By.XPATH, "//*[@id='pacientesModal']/div/div/div[1]/button/i")
            close_button.click()

        # Finaliza a estrutura HTML no final do arquivo
        file.write("</body></html>\n")

    print("Arquivo output.html recriado e atualizado com sucesso!")

def generoNome(nome):
    # Realizando a requisição à API do Genderize
    url = f"https://api.genderize.io?name={nome}&country_id=BR"
    response = requests.get(url)
    resultado = response.json()

    # Exibindo o resultado (opcional, pode ser removido)
    #print(resultado)

    # Verificando o gênero retornado
    if 'gender' in resultado:
        if resultado['gender'] == 'male':
            artigo = "o"
        elif resultado['gender'] == 'female':
            artigo = "a"
        else:
            artigo = "X"  # Caso o gênero seja desconhecido ou não identificado
    else:
        artigo = "X"  # Caso a API não retorne um gênero

    return artigo




loginNoSite()
verListaPaciente()
printNomeTelefone()

time.sleep(10)

