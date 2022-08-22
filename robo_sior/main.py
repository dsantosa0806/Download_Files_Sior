from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import json
import sqlite3


def option_navegador():

    options = webdriver.ChromeOptions()
    download_path = r'C:\Users\Usuário\PycharmProjects\robo_sior\autos' + '\\' + str(N_Autos)
    options.add_experimental_option('prefs', {
        "download.default_directory": download_path,  # change default directory for downloads
        "download.prompt_for_download": False,  # to auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # it will not show PDF directly in chrome
    })
    return options


def acessa_sior():
    #Acesso a tela de login
    url_Login = 'http://servicos.dnit.gov.br/sior/Account/Login/?ReturnUrl=%2Fsior%2F'
    navegador.get(url_Login)
    time.sleep(1)


def login():
    userName = ''
    userPass = ''
    CPFpath = '// *[ @ id = "UserName"]'
    senhaPath = '//*[@id="Password"]'
    clickpath = '//*[@id="FormLogin"]/div[4]/div[2]/button'

    err = True
    while err:

        try:
            WebDriverWait(navegador, 120).until(
                EC.presence_of_element_located(
                    (By.XPATH, CPFpath))).send_keys(userName)
            WebDriverWait(navegador, 120).until(
                EC.presence_of_element_located(
                    (By.XPATH, senhaPath))).send_keys(userPass)
            WebDriverWait(navegador, 120).until(
                EC.element_to_be_clickable(
                    (By.XPATH, clickpath))).click()
            

            time.sleep(2)

            err = False
        except TimeoutException:
            print("loading....")


def pesquisa_auto():

    path_Auto = '//*[@id="NumeroAuto"]'
    path_Btn_CloseFilter = '//*[@id="SituacoesInfracaoSelecionadas_taglist"]/li/span[2]'
    path_Btn_Consultar = '//*[@id="placeholder"]/div[1]/div/div[1]/button'
    path_details = '//*[@id="gridInfracao"]/table/tbody/tr/td[1]/a'
    path_Menu_relat = '//*[@id="menu_relatorio"]/li/span'
    path_Menu_relat2 = '//*[@id="menu_relatorio_mn_active"]/span'

    # INPUT AIT
    try:
        WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, path_Auto))).send_keys(N_Autos)
    except TimeoutException:
        print('Travei no primeiro passo, no início da consulta')

    # DESABILITA FILTRO AUTO
    try:
        WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, path_Btn_CloseFilter))).click()
    except TimeoutException:
        print('Travei no segundo passo, tentei fechar o filtro')

    # REALIZA A CONSULTA
    try:
        WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, path_Btn_Consultar))).click()
    except TimeoutException:
        print('Travei no terceiro passo, no botão consultar')

    #detalhes
    try:
        WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, path_details))).click()
    except TimeoutException:
        print('Travei no quarto passo, indo em detalhes')

    # CLIQUE PARA ABRIR MENU
    try:
        WebDriverWait(navegador, 120).until(
            EC.element_to_be_clickable((By.XPATH, path_Menu_relat))).click()
    except ElementClickInterceptedException:
        print('Travei no sexto passo, clique em abrir o menu')


def download_na_np_ait_arna():
    # EXECUTANDO O DOWNLOAD NA, NP, AR
    try:
        # navegador.get(urlBaseSior + urlDownloadAuto) # # DOWNLOAD AUTO
        # time.sleep(1)

        navegador.get(urlBaseSior + urlDownloadNa)  # # DOWNLOAD NA
        time.sleep(2)

        navegador.get(urlBaseSior + urlDownloadNp)  # # # DOWNLOAD NP
        time.sleep(2)

        navegador.get(urlBaseSiorAr + urlDownloadArNa)  # # # DOWNLOAD AR NA
        time.sleep(2)

        # PRINT URL
        link_auto = (urlBaseSior + urlDownloadAuto)
        link_na = (urlBaseSior + urlDownloadNa)
        link_np = (urlBaseSior + urlDownloadNp)
        link_ar_na = (urlBaseSiorAr + urlDownloadArNa)

    except TimeoutException:
        print('Travei Download da NP e NA')


def download_relatorio_resumido():
    path_Id_Relatorio = 'btnExportarRelatorioResumido'
    path_Relatorio = '//*[@id="btnExportarRelatorioResumido"]'
    
    # CLIQUE PARA BAIXAR RELATÓRIO RESUMIDO
    try:
        WebDriverWait(navegador, 120).until(
            EC.element_to_be_clickable(
                (By.ID, path_Id_Relatorio))).click()
        time.sleep(3)  # importante manter um Delay de Time, necessário implementar uma função que verifica se o download foi exec

    except ElementClickInterceptedException:
        print('Travei no 7 passo, clique em Baixar Relatório o menu')


def acessa_tela_incial_auto():
    url_Base = 'https://servicos.dnit.gov.br/sior/Infracao/ConsultaAutoInfracao/?SituacoesInfracaoSelecionadas=1'
    # Acessa a tela da notificação da autuação
    navegador.get(url_Base)
    time.sleep(1)


def acessa_tela_consulta_auto():

    navegador.get(urlBaseSiorDetaisAuto + codInfracaoNa)
    time.sleep(3)


def download_edital_dou_na():
    path_Edital_Na = '//*[@id="center-pane"]/div/div/div/div[5]/div[1]/a'
    path_Dou_Na = '//*[@id="center-pane"]/div/div/div/div[5]/div[2]/a'
    
    # Acessa a tela da notificação da autuação
    navegador.get(urlBaseSiorDetails + urlDownloadArNa)
    time.sleep(3)    
    try:
        WebDriverWait(navegador, 120).until(
            EC.element_to_be_clickable(
                (By.XPATH, path_Edital_Na))).click()
        WebDriverWait(navegador, 120).until(
            EC.element_to_be_clickable(
                (By.XPATH, path_Dou_Na))).click()
        time.sleep(
            3)  # importante manter um Delay de Time, necessário implementar uma função que verifica se o download foi exec

    except ElementClickInterceptedException:
        print('Travei no 8 passo, clique em Baixar Editais NA')


def download_edital_dou_np():
    path_Edital_Np = '//*[@id="center-pane"]/div/div/div/div[5]/div[1]/a'
    path_Dou_Np = '//*[@id="center-pane"]/div/div/div/div[5]/div[2]/a'
    
    # Acessa a tela da notificação de penalidade
    navegador.get(urlBaseSiorDetails + codInfracaoNp)
    time.sleep(3)
    try:
        WebDriverWait(navegador, 120).until(
            EC.element_to_be_clickable(
                (By.XPATH, path_Edital_Np))).click()
        WebDriverWait(navegador, 120).until(
            EC.element_to_be_clickable(
                (By.XPATH, path_Dou_Np))).click()
        time.sleep(
            5)  # importante manter um Delay de Time, necessário implementar uma função que verifica se o download foi exec

    except ElementClickInterceptedException:
        print('Travei no 9 passo, clique em Baixar Editais Np')


def verifica_da_sa_recursos():

    path_da_sa_recursos = '//*[@id="tabInfracao-tab-3"]/span[2]'
    path_da_sa_recursos2 = '//*[@id="tabInfracao-tab-3"]'
    path_id_da = 'tabInfracao-tab-3'


    try:
        WebDriverWait(navegador, 120).until(
            EC.presence_of_element_located(
                (By.XPATH, path_da_sa_recursos))).click()
        print('elemento DA/SA/Rec loc !')

    except ElementClickInterceptedException:
        print('Travei no 10 passo, clique em Elementos Ait')

    urlverificada = navegador.page_source.encode('utf-8')
    soupverificacao = BeautifulSoup(urlverificada, 'html.parser')
    elementosverificacao = str(soupverificacao.find_all("div", attrs={"class": 'lt-row'}))  # Class padrão DA SA e recursos

    print(soupverificacao.prettify())


def create_db():
    conexao = sqlite3.connect('Bd_autos.db')
    c = conexao.cursor()
    c.execute(''' CREATE TABLE Consulta(
    Auto text,
    Link_auto text,
    Notificacao_autuacao text,
    Notificacao_penalidade text,
    Ar_Na text
    )    
    ''')

    # Commit as mudanças:
    conexao.commit()

    # Fechar o banco de dados:
    conexao.close()


def cadastrar_demanda_base():
    conexao = sqlite3.connect('Bd_autos.db')
    c = conexao.cursor()

    #Inserir dados na tabela do BD:
    c.execute("INSERT INTO Consulta VALUES (:Auto,:Link_auto,:Notificacao_autuacao,:Notificacao_penalidade,:Ar_Na)",
              {
                  'Auto': N_Autos,
                  'Link_auto': link_auto,
                  'Notificacao_autuacao': link_na,
                  'Notificacao_penalidade': link_np,
                  'Ar_Na': link_ar_na
                  # 'Relatorio_resumido' = link_relat,
                  # 'Edital_Na': situacaoCadastralMotivo,
                  # 'Dou_Na': razaoSociao,
                  # 'Edital_Np': razaoSociao,
                  # 'Dou_Np': razaoSociao
              })

    # Commit as mudanças:
    conexao.commit()

    # Fechar o banco de dados:
    conexao.close()


def exporta_dados():
    conexao = sqlite3.connect('Bd_autos')
    c = conexao.cursor()

    # Inserir dados na tabela:
    c.execute("SELECT *, oid FROM Consulta") # Verificar
    dados = c.fetchall()
    data = (datetime.today().strftime('%Y-%m-%d %H_%M')) # data de geração do arquivo
    dados = pd.DataFrame(dados, columns=['Auto','Link_auto','Notificacao_autuacao','Notificacao_penalidade','Ar_Na'])
    dados.to_excel(f'''dados_finalizados_{data}.xlsx''',sheet_name='Resultado',index=False)

    # Commit as mudanças:
    conexao.commit()

    # Fechar o banco de dados:
    conexao.close()


#Criação do BD_ Somente uma única vez
create_db()

## INSTANCIANDO PLANILHA BASE
table = pd.read_excel('table\Planilha.xlsx')
diretorio = 'autos'
tempo_inicial = time.time()  # Tempo em segundos

if not os.path.exists(diretorio):
    os.mkdir(diretorio)

# Inicio do Laço
for i, N_Autos in enumerate(table['AUTO']):
    if not os.path.exists(diretorio + '\\' + str(N_Autos)):
        os.mkdir(diretorio + '\\' + str(N_Autos))

        # INSTANCIANDO O WEBDRIVER
        navegador = webdriver.Chrome(executable_path=r'./chromedriver.exe', options=option_navegador(), )
        acessa_sior()
        login()
        acessa_tela_incial_auto()
        pesquisa_auto()

        # URL Padrões
        urlBaseSior = 'https://servicos.dnit.gov.br/sior/Infracao/ConsultaAutoInfracao/'
        urlBaseSiorDetaisAuto = 'https://servicos.dnit.gov.br/sior/Infracao/ConsultaAutoInfracao/Details/'
        urlBaseSiorAr = 'https://servicos.dnit.gov.br/sior/Infracao/NotificacaoConsulta/Download/'
        urlBaseSiorDetails = 'https://servicos.dnit.gov.br/sior/Infracao/NotificacaoConsulta/Details/'
        urlBaseSiorDa = '/sior/Infracao/DefesaAutuacaoConsulta/Details/2491670'

        #LENGHT PADRÃO DE ARQUIVOS
        LenghtAuto = len('ExportarRelatorioAutoInfracao/107120033?numeroAuto=D008521814&amp;indicadorComprovacao=2101&amp;target=_blank')
        LenghtNa = len('DownloadSegundaViaNA/107851973?numeroAuto=D008521814&amp;indicadorComprovacao=2101')
        LenghtNp = len('DownloadSegundaViaNP/107851973?numeroAuto=D008521814&amp;indicadorComprovacao=2101')
        LenghtCodInfra = len('Details/xxxxxxxxx')
        LenghtCodInfraNp = len('DownloadSegundaViaNP/xxxxxxxxx')
        LenghtCodInfraNa = len('DownloadSegundaViaNA/xxxxxxxxx')
        LenghtEditalNa = '/DownloadEdital?nomeArquivo=Edital%20N%C2%BA040-2016_NA-PNCV.pdf&amp;nomeFisico=%5C%5C10.100.11.189%5Csior_arquivos_gerais%5C39%5C1f%5Cad%5C391fad6f858d422987c699dc2f9d8e1a'

        ## TRATAMENTO DE URL NA E NP
        Url = navegador.page_source.encode('utf-8')
        soup = BeautifulSoup(Url, 'html.parser')
        elementos = str(soup.find_all("div", attrs={"class": 'lt-col-3'}))  # Class padrão da Na SIOR
        elementosAuto = str(soup.find_all("div", attrs={"class": 'lt-col-7'}))  # Class padrão Auto SIOR
        elementosDefesa = str(soup.find_all("div", attrs={"class": 'lt-col-10'}))  # Class padrão da Na SIOR

        # PADRÃO DE DOCS DO SIOR
        padrao_auto = 'ExportarRelatorioAutoInfracao/'
        padrão_Na = 'DownloadSegundaViaNA/'
        padrão_Np = 'DownloadSegundaViaNP/'
        padrão_Ar = 'Download/'
        padrao_CodInfra_Ar_Na = '/Details/'
        padrao_CodInfra_Na = 'DownloadSegundaViaNA/'
        padrao_CodInfra_Np = 'DownloadSegundaViaNP/'

        # ## Posição dos dados na Html
        posicaoAuto = elementosAuto.find(padrao_auto)
        posicaoNa = elementos.find(padrão_Na)
        posicaoNp = elementos.find(padrão_Np)
        posicaoCodInfraNa = elementos.find(padrao_CodInfra_Ar_Na) + 1  # Exclusivo

        # Url Tratada
        urlDownloadAuto = re.sub('amp;',"",elementosAuto[posicaoAuto:posicaoAuto + LenghtAuto])  # Possibilidade 1
        urlDownloadNa = re.sub('amp;',"",elementos[posicaoNa:posicaoNa+LenghtNa])
        urlDownloadNp = re.sub('amp;',"",elementos[posicaoNp:posicaoNp+LenghtNp])
        urlDownloadArNa = elementos[-posicaoCodInfraNa:posicaoCodInfraNa + LenghtCodInfra]
        posicaoCodInfraNa = urlDownloadNa.find(padrao_CodInfra_Na)
        posicaoCodInfraNp = urlDownloadNp.find(padrao_CodInfra_Np)
        codInfracaoNa = urlDownloadNa[len(padrao_CodInfra_Na):LenghtCodInfraNa]
        codInfracaoNp = urlDownloadNp[len(padrao_CodInfra_Np):LenghtCodInfraNp]

        # Links
        link_auto = (urlBaseSior + urlDownloadAuto)
        link_na = (urlBaseSior + urlDownloadNa)
        link_np = (urlBaseSior + urlDownloadNp)
        link_ar_na = (urlBaseSiorAr + urlDownloadArNa)

        download_na_np_ait_arna()
        download_relatorio_resumido()
        download_edital_dou_na()
        download_edital_dou_np()
        acessa_tela_consulta_auto()

        # verifica_da_sa_recursos()  # Parei aqui, não clica na statebox de Da/sa/Recursos // Tentar outro método
        cadastrar_demanda_base()

        print('Auto {} | Sucesso | {} |'.format(N_Autos,time.strftime("%H:%M:%S")))
    else:
        print(f'O diretório de pasta {N_Autos} já existe!')


# try:
#     exporta_dados()     ##Erro ao exportar
# except:
#     print('Erro ao exportar!')
tempo_final = time.time()
resultado = int(tempo_final - tempo_inicial)
print(time.strftime("%H:%M:%S", time.gmtime(resultado)))
