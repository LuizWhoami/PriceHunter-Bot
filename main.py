import requests
from bs4 import BeautifulSoup

#1 abrir a shopee com a peesquisa basica
#2 vai olhar até a pagina 2
#3 analisa os menores preços e maiores
#4 analisa os com mais compras
#5 analisa os 3 melhores em compras e em preços

requisicao = requests.get("https://shopee.com.br/search?keyword=pc&page=0&sortBy=relevancy")
contentss = requisicao.text
soup = BeautifulSoup(requisicao.content, "html.parser")


tag_titulo = soup.find_all('li', class_='ui-search-layout__item')
titulo = []
for tag in tag_titulo:
    titulo.append(tag.text)

preco = soup.find_all('div', class_='poly-component__price')
price = []
for tags in preco:
    price.append(tags.text.replace('Ã', ''))
