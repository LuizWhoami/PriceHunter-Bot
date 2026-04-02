import requests
from bs4 import BeautifulSoup

def enviar():
    
    chat_id = '-5102848021'
    token = '8788032847:AAEOwVrWD-Y017Qk4Mewm6VSF8Yh9JllLNE'

    url_telegram = f'https://api.telegram.org/bot{token}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'token': token,
        "parse_mode": "Markdown",
        'text': f'{produto1} \n {preco1} \n {desconto1}'
    }

    resposta = requests.post(url_telegram, payload)

    if resposta.status_code == 200:
        print('Mensagem enviada com sucesso')

    else:
        print(f'Erro {resposta.status_code}')
        print(resposta.text)

def mercado():
    global produto1, preco1, desconto1
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

            produto1 = produto.text.strip()
            preco1 = preco.text.strip()
            desconto1 = desconto.text.strip()

            tag_link = itens.find('a')
            link = tag_link['href'] if tag_link else "Link não encontrado"
            if produto:
                print(f'Produto: {produto1}')
                print(f'Preço:  {preco1} ')
                if desconto:   
                    print(f'Desconto: {desconto1}')
                else:
                    print('Sem desconto')
                print(f'Link: {link} \n \n')

enviar(mercado())

print(f'Mensgem enviada: \n {produto1}')