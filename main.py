import requests
from bs4 import BeautifulSoup


url = 'https://lista.mercadolivre.com.br/pc'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print('conexão com sucesso')

    soup = BeautifulSoup(response.content, 'html.parser')

    pega_nome = soup.find_all('div', class_='poly-card__content')
    
    for itens in pega_nome:

        produto = itens.find('h3')
        preco = itens.find('span', class_='andes-money-amount')
        desconto = itens.find('span', class_='andes-money-amount__discount')

        tag_link = itens.find('a')
        link = tag_link['href'] if tag_link else "Link não encontrado"
        if produto:
            print(f'Produto: {produto.text.strip()}')
            print(f'Preço:  {preco.text.strip()} ')
            if desconto:   
                print(f'Desconto: {desconto.text}')
            else:
                print('Sem desconto')
            print(f'Link: {link} \n \n')


#Integração com telegram

id = '6522307847'
key = 