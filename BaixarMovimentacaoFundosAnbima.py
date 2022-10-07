### Imports ###
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from os.path import expanduser

path_output = os.path.expanduser("~").replace(
    '\\', '/') + '/OneDrive - Tower Three/Área de Trabalho/Projetos/ANBIMA/'

### Getting url from current day ###
page = requests.get(
    f"https://www.anbima.com.br/pt_br/informar/estatisticas/fundos-de-investimento/fi-consolidado-diario.htm")
soup = BeautifulSoup(page.content, 'html.parser')

final = soup.find(id="informacoes-tecnicas").find('a')['href'][11:]
anbima = 'https://www.anbima.com.br'
url = anbima + final

### Saving url in urls.txt ###
# Reading and getting last url saved
with open(f"{path_output}urls.txt", "r") as f:
    text = f.read()
    last_line = text.split('\n')[-1]

# Comparing last url saved with current url, if they are different, it will save the current url
if last_line != url:
    with open(f"{path_output}urls.txt", "a") as f:
        f.write('\n' + url)
    print(f"Url: {url} adicionada com sucesso!")
else:
    print("Url já existe no arquivo!")

### Extracting table directly from url ###
movimentacao_anbima = pd.read_excel(
    url, skiprows=8, usecols=[0, 8, 9, 10, 11]).iloc[:7]

### Treating Data ###
# Extracting date from url
file_date = url[-12:-4]  # Transformar em data?

# Inserting new column with dataRef
movimentacao_anbima.insert(0, 'dataRef', file_date)
# Changing column names
old_columns = movimentacao_anbima.columns.tolist()
new_columns = ['dataRef', 'classeAnbima', 'movimentacaoDia',
               'movimentacaoMes', 'movimentacaoAno', 'movimentacao12M']
dict_from_list = dict(zip(old_columns, new_columns))
movimentacao_anbima.rename(columns=dict_from_list, inplace=True)

print(movimentacao_anbima)

### Saving Data ###
try:
    movimentacao_anbima.to_excel(
        f'{path_output}files/{file_date}_movimentacaoFundosAnbima.xlsx', index=False, encoding='Latin-ASCII')
    print(f"Arquivo do dia {file_date} salvo com sucesso!")
except:
    print(f"Falha no salvamento do arquivo do dia {file_date}")
