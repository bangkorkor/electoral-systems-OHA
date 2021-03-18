'''
Questo script ottiene i dati delle elezioni della Camera del 2001 in formato tabulare tramite web scraping.
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup

# liste che conterranno i dati trovati, diventeranno poi righe di dataframe
voti_uninominale = []
voti_plurinominale = []

# ottengo la BeautifulSoup della pagina di partenza
HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)  AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/44.0.2403.157 Safari/537.36', 
                'Accept-Language': 'en-US, en;q=0.5'}) 
base_url = 'https://elezionistorico.interno.gov.it'
start_page = '/index.php?tpel=C&dtel=13/05/2001&tpa=I&tpe=A&lev0=0&levsut0=0&es0=S&ms=S'
page = requests.get(base_url + start_page, headers=HEADERS)
soup = BeautifulSoup(page.content, 'html.parser')

# lista delle circscrizioni plurinominali dal menu a tendina
circoscrizioni = soup.find(id="collapseFour").find_all("li")

for circ in circoscrizioni:
    # ottengo la BeautifulSoup della pagina della circoscrizione
    circ_link = circ.find('a')
    circ_page = requests.get(base_url + circ_link['href'], headers=HEADERS)
    circ_soup = BeautifulSoup(circ_page.content, 'html.parser')
    
    # aggiungo i voti della quota proporzionale a voti_proporzionale
    if circ_link.contents[0] != "VALLE D'AOSTA":
        rows_proporzionale = circ_soup.find('table',class_='dati').find_all('tr')
        
        for i, row in enumerate(rows_proporzionale):
            if i != 0 and i != len(rows_proporzionale)-1:
                res = {'Circoscrizione': circ_link.contents[0]}

                res['Partito'] = row.find(id='lista'+str(i-1)).find('a').contents[0].replace(u'\xa0','').strip(' ')
                res['Voti'] = row.find_all('td')[1].contents[0].replace('.','').strip(' ')
                voti_plurinominale.append(pd.Series(res))

    # lista dei collegi in questa circoscrizione dal menu a tendina
    collegi = circ_soup.find(id='collapseFive').find_all('li')

    for col in collegi:
        # ottengo la BeautifulSoup della pagina del collegio
        col_link = col.find('a')
        col_page = requests.get(base_url + col_link['href'] + '&unipro=uni', headers=HEADERS)
        col_soup = BeautifulSoup(col_page.content, 'html.parser')

        # lista delle righe della tabella
        rows_uninominale = col_soup.find('table', class_='dati').find_all('tr')
        
        # aggiungo i voti della quota uninominale a voti_uninominale
        for i in range(1, len(rows_uninominale)-1, 2):
            columns = rows_uninominale[i].find_all('td')
            res = {'Collegio': col_link.contents[0].upper().strip(' ')}
            res['Candidato'] = columns[0].contents[0].strip(' ')

            liste = rows_uninominale[i+1].find_all('td')[2]
            res['Lista'] = liste.contents[1].replace(u'\xa0','').strip(',').strip(' ')
            if len(liste) > 2:
                for i in range(3,len(liste),2):
                    res['Lista'] = liste.contents[i].replace(u'\xa0','').strip(',').strip(' ') + ' - ' + res['Lista']

            res['Partito'] = res['Lista']
            res['PartitoCollegato'] = res['Lista']
            res['Voti'] = columns[5].contents[0].replace('.','').strip(' ')
            voti_uninominale.append(pd.Series(res))
    
    print(circ_link.contents[0])

# salvo i risultati ottenuti su file
pd.concat(voti_uninominale,axis=1).T.to_csv('voti_uninominale.csv', index=False)
pd.concat(voti_plurinominale,axis=1).T.to_csv('voti_plurinominale.csv', index=False)