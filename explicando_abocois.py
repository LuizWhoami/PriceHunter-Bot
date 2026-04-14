import requests
from bs4 import BeautifulSoup

url = 'https://www.python.org/blogs/'
resposta = requests.get('url')

if resposta.status_code == 200:
    print('conexão feita')

    soup = BeautifulSoup(resposta.content, 'html.parser')


sleep>102
