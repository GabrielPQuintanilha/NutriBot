import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
#totalkids = None

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

    login_input.send_keys("XXXXXXXXXXXXXXXXXX@gmail.com")
    senha_input.send_keys("XXXXXXXX")
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

    if totalkids =="yes":
        return f"%20Como%20foi%20a%20semana%20d%20{criarNomeSimplificado(nome_paciente_texto)}?"
        
    else:
        return f"%20Como%20foi%20a%20sua%20semana,%20{criarNomeSimplificado(nome_paciente_texto)}?"
        

def printNomeTelefone():
    for i in range(0,50):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"fotoPerfil{i}"))
        )

        totalkids = totalkidsOuNao(i)

        botao_imgPaciente = driver.find_element(By.ID, f"fotoPerfil{i}")
        botao_imgPaciente.click()

        perguntaNovaConsulta()

        driver.implicitly_wait(1)

        modal_content = driver.find_elements(By.ID, "modal-content")
        nome_paciente = driver.find_element(By.ID, "nomeDadosFake")
        telefone_paciente = driver.find_element(By.ID, "telefoneDadosFake")

        nome_paciente_texto = nome_paciente.text
        telefone_paciente_texto = telefone_paciente.text
        telefone_paciente_texto = re.sub(r'\D','', telefone_paciente_texto)

        print(f"Nome: {nome_paciente_texto} | link: https://web.whatsapp.com/send/?phone=55{telefone_paciente_texto}&text={turnoDoDia()}{textoParaWhatsapp(nome_paciente_texto,totalkids)}")
        print("")
        
        close_button = driver.find_element(By.XPATH, "//*[@id='pacientesModal']/div/div/div[1]/button/i")
        close_button.click()





loginNoSite()
verListaPaciente()
printNomeTelefone()

time.sleep(10)

