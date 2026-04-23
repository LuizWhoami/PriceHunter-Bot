import requests
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from io import BytesIO
import re


dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir=" + dir_path + "/pasta/sessao")
driver = webdriver.Chrome(chrome_options2)
url = 'https://www.mercadolivre.com.br/afiliados/hub'
driver.get(url)


sleep(5)
actions = ActionChains(driver)
for i in range(10):
    actions.send_keys(Keys.END)
    actions.pause(2)
    sleep(2)
actions.perform()
sleep(30)
try:
    resultados = []

    produto = driver.find_elements(By.CLASS_NAME, 'poly-component__title')
    preso = driver.find_elements(By.CLASS_NAME, 'poly-card__content')
    virgula_dinh = driver.find_elements(By.CLASS_NAME, 'andes-money-amount__cents')
    desconto = driver.find_elements(By.CLASS_NAME, 'andes-money-amount__discount')

    img = driver.find_elements(By.CLASS_NAME, 'poly-component__picture')
    for produtos, preso, virgula, descon, imagems in zip(produto, preso, virgula_dinh, desconto, img):
       prod = produtos.text.strip()
       pres = preso.text.strip()
       virg = virgula.text.strip()
       desco = descon.text.strip()

       imagem = imagems.get_attribute('src')
       linkss = produtos.get_attribute('href')

       imagens = requests.get(imagem).content

       print(f'Produto: {prod} \n Preço:{pres},{virg} \n Desconto: {desco}')
       print(f'Link: {linkss}')
       print(f'Imagem: {imagem}')
       exit()
       dados = {
            'Produto': prod,
            'Preço': pres,
            'Virgula': virg,
            'Desconto': desco,
            'Link': linkss,
            'Imagem': imagens
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
    preco2 = linha['Preço']
    virgula = linha['Virgula']
    desconto2 = linha['Desconto']
    link2 = linha['Link']
    imagem2 = linha['Imagem']

    mensagem = (
        f"\n"
        f"📦 {produto2} \n \n"
        f" 💰 Preço:{preco2},{virgula} \n \n"
        f"📉 Desconto: {desconto2} \n \n"
        f"🔗 Link: {link2} \n \n \n \n "
    )
    
    url_telegram2 = f'https://api.telegram.org/bot{token}/sendPhoto'   

    #resposta = requests.post(url_telegram, payload)
    resposta2 = requests.post(url_telegram2,
                              data={
            "chat_id": chat_id,
            "token": token,
            "caption": mensagem
        },
        files={
            "photo": ("img.jpg", BytesIO(imagem2)),
        })

    if resposta2.status_code == 200:
        print('Mensagem enviada com sucesso')
        sleep(2)

    else:
        print(f'Erro {resposta2.status_code}')
        print(resposta2.text)
