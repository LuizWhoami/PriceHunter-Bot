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
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

chrome_options2.add_argument(f'user-agent={user_agent}')
chrome_options2.add_argument(f"user-data-dir={dir_path}/shopee/sessao")

driver = webdriver.Chrome(options=chrome_options2)

url = 'https://affiliate.shopee.com.br/offer/product_offer'
driver.get(url)


sleep(500)


try:
    resultados = []

    produto = driver.find_elements(By.CLASS_NAME, 'product-offer-list')
    #link = driver.find_elements(By.CLASS_NAME, 'AffiliateItemCard')
    #img = driver.find_elements(By.CLASS_NAME, 'ItemCard__image')
    #price = driver.find_elements(By.CLASS_NAME, 'poly-price__current')
    #price_antes = driver.find_elements(By.CLASS_NAME, 'andes-money-amount--cents-comma')


    for produtos in produto:
       Compras = produtos.find_element(By.CLASS_NAME, 'ItemCardSold__wrap').text
       prod = produtos.find_element(By.CLASS_NAME, 'ItemCard__name').text
       pres = produtos.find_element(By.CLASS_NAME, 'ItemCard__price').text
       
       
       linkss = produtos.get_attribute('href')

       imagem = produtos.get_attribute('src')

       imagens = requests.get(imagem).content

       print(f'Produto: {prod} \n Preço: {pres} \n Compras do produto: {Compras}')
       print(f'Link: {linkss}')
       print(f'Imagem: {imagem}')
       exit()
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