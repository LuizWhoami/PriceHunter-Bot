import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os


dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir=" + dir_path + "/pasta/sessao")
driver = webdriver.Chrome(chrome_options2)
url = 'https://www.mercadolivre.com.br/afiliados/hub'
sleep(20)

try:
    driver.get(url)
    nome = driver.find_elements(By.CLASS_NAME, 'poly-component__title')
    nome = [e.text for e in nome]
    nom = nome[-1]
    print(nome)
    sleep(20)
    exit()
    print('PAgina sendo carregada')
    sleep(15)

    html_da_pagina = driver.page_source

    print('conexão com sucesso')

    soup = BeautifulSoup(html_da_pagina, 'html.parser')

    pega_nome = soup.find_all('div', class_='poly-card')

    resultados = []
    
    for itens in pega_nome:
   
        produto = itens.find('a')
        preco = itens.find('span', class_='andes-money-amount')
        desconto = itens.find('span', class_='poly-price__disc_label')
        imagem = itens.find('img', class_='poly-component__picture')

        if produto and preco and desconto: 
            produto1 = produto.text.strip()
            preco1 = preco.text.strip()
            desconto1 = desconto.text.strip()   

            tag_imagem = itens.find('img')
            link_imagem = tag_imagem['src']
            link_imagens = link_imagem.strip()

            tag_link = itens.find('a')
            link = tag_link['href'] if tag_link else "Link não encontrado"
            linkis = link.strip()

            dados = {
                'Produto': produto1,
                'Preço': preco1,
                'Desconto': desconto1,
                'Link': linkis,
                'Imagem': link_imagens
            }

            resultados.append(dados)

        if produto:
            print(f'Imagem: {link_imagens}')
            print(f'Produto: {produto1}')
            print(f'Preço:  {preco1} ')
            if desconto1:   
                print(f'Desconto: {desconto1}')
            else:
                print('Sem desconto')
            print(f'Link: {linkis} \n \n')
        else:
            print(f'Ocorreu um erro {produto and preco and desconto}')

except:
    pass


df = pd.DataFrame(resultados)
df.to_excel('Produtos.xlsx', index=False, engine='openpyxl')
print('Dados salvos')

chat_id = '-5102848021'
token = '8788032847:AAEOwVrWD-Y017Qk4Mewm6VSF8Yh9JllLNE'


for index, linha in df.iterrows():
    produto2 = linha['Produto']
    preco2 = linha['Preço']
    desconto2 = linha['Desconto']
    link2 = linha['Link']
    imagem2 = linha['Imagem']

    mensagem = (
        f"{'-'*100} \n"
        f"📦 Produto: {produto2} \n \n"
        f"💰 Preço: {preco2} \n \n"
        f"📉 Desconto: {desconto2} \n \n"
        f"🔗 Link: {link2} \n \n"
        f"{imagem2} \n \n"
        f"{'-'*100}"
    )
    
    url_telegram = f'https://api.telegram.org/bot{token}/sendMessage'
    sleep(10)
    payload = {
        'chat_id': chat_id,
        'token': token,
        'text': mensagem,
        'disable_web_page_preview': False
    }

    resposta = requests.post(url_telegram, payload)

    if resposta.status_code == 200:
        print('Mensagem enviada com sucesso')
        sleep(2)

    else:
        print(f'Erro {resposta.status_code}')
        print(resposta.text)