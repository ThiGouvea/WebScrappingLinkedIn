import re
import time
import pandas as pd
from selenium import webdriver
from getpass import getpass
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

email = str(input('Digite o email: '))
password = getpass()
link_pesquisa = 'https://www.linkedin.com/search/results/people/?keywords=tech%20recruiter&origin=CLUSTER_EXPANSION&sid=4d5'


options = Options()
options.add_argument('--headless')
navegador = webdriver.Firefox()
navegador.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
navegador.find_element('xpath', '//*[@id="username"]').send_keys(email)
navegador.find_element('xpath', '//*[@id="password"]').send_keys(password)
navegador.find_element('xpath', '/html/body/div/main/div[2]/div[1]/form/div[3]/button').click()
url = navegador.current_url
tabela = []
erros = 0
navegador.get(link_pesquisa)


for i in range(0, 99, 1):
    while url != link_pesquisa:
        url = navegador.current_url
        time.sleep(3)

    navegador.execute_script("window.scrollTo(0, 1080)")
    time.sleep(1)
    site = BeautifulSoup(navegador.page_source, 'html.parser')
    pessoas = site.findAll('div', attrs={'class': 'entity-result__item'})

    try:
        for pessoa in pessoas:
            nome = pessoa.find('span', attrs={'aria-hidden': 'true'})
            hashtags = pessoa.find('div', attrs={'class': 'entity-result__primary-subtitle t-14 t-black t-normal'})
            cidade = pessoa.find('div', attrs={'class': 'entity-result__secondary-subtitle t-14 t-normal'})
            cidade = str(cidade)
            cidade = re.sub('[-<>!/]', '', cidade[cidade.find('<!-- -->'):-5])
            if nome is None:
                nome = ''
            else:
                nome = nome.text

            if hashtags is None:
                hashtags = ''
            else:
                hashtags = hashtags.text

            if cidade is None:
                cidade = ''

            tabela.append([nome.replace('\n', ''), hashtags.replace('\n', ''), cidade.replace('\n', '')])
            print(nome + hashtags + cidade + '\n')


        idember = site.find('button', attrs={'aria-label': 'Avançar'})
        idember = str(idember)
        idember = re.sub('[-<>!/"]', '', idember[idember.find('id="ember') + 9:idember.find('type="button') - 2])
        xpath = f'//*[@id = "ember{idember}"]'
        time.sleep(2)
        navegador.find_element('xpath', xpath).click()
        time.sleep(2)
        url = navegador.current_url
        link_pesquisa = navegador.current_url
    except:
        print('pagina não encontrada')
        navegador.refresh()
        time.sleep(5)
        erros += 1
        if erros >= 50:
            break
        continue




todas_informacoes = pd.DataFrame(tabela, columns=['Nome', 'Hashtags', 'Cidade'])
todas_informacoes.to_excel('TabelaPessoas.xlsx', index=False)



