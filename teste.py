import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir=" + dir_path + "/pasta/sessao")
driver = webdriver.Chrome(chrome_options2)
url = 'https://www.mercadolivre.com.br/afiliados/hub'
driver.get(url)

sleep(5)
actions = ActionChains(driver)
for i in range(40):
    actions.send_keys(Keys.END)
    actions.pause(2)
    sleep(2)
actions.perform()
sleep(30)
try:
    produto = driver.find_elements(By.CLASS_NAME, 'poly-component__title')
    cifrao = driver.find_elements(By.CLASS_NAME, 'andes-money-amount__currency-symbol')
    preco = driver.find_elements(By.CLASS_NAME, 'andes-money-amount__fraction')
    virgula_dinh = driver.find_elements(By.CLASS_NAME, 'andes-money-amount__cents')
    
    desconto = driver.find_elements(By.CLASS_NAME, 'andes-money-amount__discount')

    img = driver.find_elements(By.CLASS_NAME, 'poly-component__picture')

    resultados = []
    for produtos, cifra, preso, virgula, descon, imagems in zip(produto, cifrao, preco, virgula_dinh, desconto, img):
       prod = produtos.text.strip()
       prec = cifra.text.strip()
       pres = preso.text.strip()
       virg = virgula.text.strip()
       desco = descon.text.strip()

       imagem = imagems.get_attribute('src')
       linkss = produtos.get_attribute('href')
       print(f'Produto: {prod} \n Preço: {prec}{pres} 0,{virg} \n Desconto: {desco}')
       print(f'Link: {linkss}')
       print(f'Imagem: {imagem}')

       dados = {
            'Produto': prod,
            'Cifrão': prec,
            'Preço': pres,
            'Virgula': virg,
            'Desconto': desco,
            'Link': linkss,
            'Imagem': imagem
        }
       resultados.append(dados)
    sleep(5)

except Exception as e:
    print(e)

df = pd.DataFrame(resultados)
df.to_excel('Produtos.xlsx', index=False, engine='openpyxl')
print('Dados salvos')

chat_id = '-5102848021'
token = '8788032847:AAEOwVrWD-Y017Qk4Mewm6VSF8Yh9JllLNE'


for index, linha in df.iterrows():
    produto2 = linha['Produto']
    cifra = linha['Cifrão']
    preco2 = linha['Preço']
    virgula = linha['Virgula']
    desconto2 = linha['Desconto']
    link2 = linha['Link']
    imagem2 = linha['Imagem']

    mensagem = (
        f"{'-'*100} \n"
        f"📦 Produto: {produto2} \n \n"
        f"💰 Preço: {cifra} {preco2} 0,{virgula} \n \n"
        f"📉 Desconto: {desconto2} \n \n"
        f"🔗 Link: {link2} \n \n \n \n "
        f" {imagem2} "
        f"{'-'*100}"
    )
    
    url_telegram = f'https://api.telegram.org/bot{token}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'token': token,
        'text': mensagem,
        'disable_web_page_preview': False
    }
    
    resposta = requests.post(url_telegram, payload)
    sleep(5)
    if resposta.status_code == 200:
        print('Mensagem enviada com sucesso')
        sleep(2)

    else:
        print(f'Erro {resposta.status_code}')
        print(resposta.text)