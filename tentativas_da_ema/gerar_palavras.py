#PARA CORRER: python3 gerar_palavras.py <palavra_que_queremos_sinonimos>
#Devolve uma lista de palavras

import requests
from bs4 import BeautifulSoup
import sys

# URL da página que você quer analisar
url = "https://www.dicio.com.br/"+sys.argv[1]+"/"

# Obter o HTML da página
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Criar o objeto BeautifulSoup para fazer o parse do HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Exemplo: Obter o título da página -----> NAO USADO MAS SE PRECISAR ESTA CA
    # titulo = soup.title.string
    # print("Título da página:", titulo)
    
    # Exemplo: Encontrar palavras sinónimas
    significado = soup.find('p', {'class': 'adicional sinonimos'})
    if significado:
        #Processo para filtrar e ficar so com as palavras
        resposta = significado.text.strip()
        resposta = resposta.split("\n")[1]
        resposta = resposta.strip()
        resposta = resposta.split(",")

        # Converter a lista de palavras para uma string
        resposta = ", ".join(resposta)
        
        print(resposta)
    else:
        print("Significado não encontrado.")
else:
    print(f"Erro ao acessar a página. Código de status: {response.status_code}")
