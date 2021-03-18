'''
Questo script sistema i dati delle elezioni della Camera del 2001 per renderli adatti ad essere simulati.
Nello specifico, inserisce il partito e il partito collegato di ogni candidato.
Salva i dati elaborati direttamente in ../Data
'''

import pandas as pd
import random

# carico i voti così come ottenuti dal sito del Ministero dell'Interno
voti_uninominale = pd.read_csv('voti_uninominale.csv')
voti_plurinominale = pd.read_csv('voti_plurinominale.csv')

# creo lista con i partiti della coalizione "LA CASA DELLE LIBERTA'".
# ogni nome compare in maniera proporzionale all'importanza del partito
cdl = [('FORZA ITALIA',280),('ALLEANZA NAZIONALE',115),('LEGA NORD',37),('CCD-CDU',31),('NUOVO PSI',11)]
cdl_nomi = []
for p,n in cdl:
    for i in range(n):
        cdl_nomi.append(p)
random.shuffle(cdl_nomi)

# creo lista con i partiti della coalizione "L'ULIVO".
# ogni nome compare in maniera proporzionale all'importanza del partito
ul = [('DEMOCRATICI SINISTRA', 212),('LA MARGHERITA',189),('IL GIRASOLE',24),('COMUNISTI ITALIANI',24),
            ('REPUBBLICANI EUROPEI',8),('SVP',8),("PS D'AZ-SARD.NATZ.",8)]
ul_nomi = []
for p,n in ul:
    for i in range(n):
        ul_nomi.append(p)
random.shuffle(ul_nomi)

# liste uninominali da non collegare a nessun partito della quota proporzionale
autonomi = ['LA BASSA IN PARLAM.',"VALLEE D'AOSTE",'BUONANNO','POPOLARI EUROPEI','LISTA DEL POPOLO','LISTA ALTERNATIVA','POP.ALTO MILANESE']

for index,r in voti_uninominale.iterrows():
    if r['Lista'] == "CASA DELLE LIBERTA'" or r['Lista'] == "FI-LG NORD (AOSTA)":
        p = cdl_nomi.pop(0)
        voti_uninominale.at[index,'Partito'] = p
        voti_uninominale.at[index,'PartitoCollegato'] = p

        #scommentare per collegare la coalizione "LA CASA DELLE LIBERTA'" alla lista civetta 'ABOLIZIONE SCORPORO'
        #voti_uninominale.at[index,'PartitoCollegato'] = 'ABOLIZIONE SCORPORO'

    elif r['Lista'] == "L'ULIVO" or r['Lista'] == "L'ULIVO - SVP" or r['Lista'] == "L'ULIVO - CON ILLY PER TRIESTE":
        p = ul_nomi.pop(0)
        voti_uninominale.at[index,'Partito'] = p
        voti_uninominale.at[index,'PartitoCollegato'] = p

        #scommentare per collegare la coalizione "L'ULIVO'" alla lista civetta 'PAESE NUOVO'
        #voti_uninominale.at[index,'PartitoCollegato'] = 'PAESE NUOVO'

    elif r['Lista'] == 'SOCIALISTI AUTONOMI':
        p = 'SOCIAL.AUTON.'
        voti_uninominale.at[index,'Partito'] = p
        voti_uninominale.at[index,'PartitoCollegato'] = p

    elif r['Lista'] == 'VALLE CAMONICA - LIBDEM.BASTA':
        p = 'LIBDEM.BASTA'
        voti_uninominale.at[index,'Partito'] = p
        voti_uninominale.at[index,'PartitoCollegato'] = p

    elif r['Lista'] == 'AN (AOSTA)':
        p = 'ALLEANZA NAZIONALE'
        voti_uninominale.at[index,'Partito'] = p
        voti_uninominale.at[index,'PartitoCollegato'] = p

    elif r['Lista'] in autonomi:
        voti_uninominale.at[index,'PartitoCollegato'] = ''

# controllo che non ci siano candidati uninominali non collegati a nessun partito della quota proporzionale
for _,r in voti_uninominale.iterrows():
    if not len(voti_plurinominale[voti_plurinominale['Partito'] == r['PartitoCollegato']].index) > 0 and not r['Partito'] in autonomi:
        print('ERRORE:',r['Lista'], r['Partito'])

# scrivo i risultati su file
voti_uninominale.to_csv('../Data/Collegio/voti_uninominale.csv', index=False)
voti_plurinominale.to_csv('../Data/Circoscrizione/voti_plurinominale.csv', index=False)
