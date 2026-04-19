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



dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir=" + dir_path + "/pasta/sessao")
driver = webdriver.Chrome(chrome_options2)
url = 'https://www.mercadolivre.com.br/afiliados/hub'
driver.get(url)


sleep(15)
actions = ActionChains(driver)
for i in range(1):
    actions.send_keys(Keys.END)
    actions.pause(2)
actions.perform()

try:
    resultados = []

    produto = driver.find_elements(By.CLASS_NAME, 'poly-card')
    link = driver.find_elements(By.CLASS_NAME, 'poly-component__title')
    img = driver.find_elements(By.CLASS_NAME, 'poly-component__picture')
    price = driver.find_elements(By.CLASS_NAME, 'poly-price__current')
    price_antes = driver.find_elements(By.CLASS_NAME, 'andes-money-amount--cents-comma')


    for produtos, imagems, lin, pri_an, pricee in zip (produto, img, link, price, price_antes):
       pres_anterior = produtos.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
       virg_anterior = produtos.find_element(By.CLASS_NAME, 'andes-money-amount__cents').text
       prod = produtos.find_element(By.CLASS_NAME, 'poly-component__title').text
       pres = pri_an.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
       virg = pri_an.find_element(By.CLASS_NAME, 'andes-money-amount__cents').text
       desco = produtos.find_element(By.CLASS_NAME, 'poly-price__disc--pill').text
       
       
       linkss = lin.get_attribute('href')

       imagem = imagems.get_attribute('src')

       imagens = requests.get(imagem).content

       print(f'Produto: {prod} \n Preço Anterior: R${pres},{virg} \n Preço Atual: R${pres_anterior},{virg_anterior} \n Desconto: {desco}')
       print(f'Link: {linkss}')
       print(f'Imagem: {imagem}')
       
       dados = {
            'Produto': prod,
            'Preço': pres,
            'Preço_Anterior': pres_anterior,
            'Virgula': virg,
            'Virgula_Anterior': virg_anterior,
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

chat_id = ''
token = ''


for index, linha in df.iterrows():
    produto2 = linha['Produto']
    preco2 = linha['Preço']
    preco3 = linha['Preço_Anterior']
    virgula = linha['Virgula']
    virgula3 = linha['Virgula_Anterior']
    desconto2 = linha['Desconto']
    link2 = linha['Link']
    imagem2 = linha['Imagem']

    mensagem = (
        f"\n"
        f"📦 {produto2} \n \n"
        f" ❌​ Preço Anterior:R$ {preco3},{virgula3} \n \n"
        f" 💰 ​ Preço Atual:R$ {preco2},{virgula} \n \n"
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
