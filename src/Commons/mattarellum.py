'''
Questo modulo contiene le funzioni necessarie alla simulazione elettorale del Mattarellum.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def select_vincente_mattarellum(*a, data, **kwargs):
    '''
        Viene chiamato nel contesto di un collegio.
        Individua il vincitore di un collegio uninominale e ritorna un dataframe del tipo |PartitoCollegato|VotiVincenti|
        composto da una sola riga, dove "PartitoCollegato" è il partito a cui era collegato il vincitore del collegio
        e "VotiVincenti" è il numero di voti necessario a vincere quel collegio (voti del secondo + 1).
        
        Parameters
        ----------
        data: dataframe del tipo |Candidato|Lista|Partito|PartitoCollegato|Voti| contente i voti del collegio
    '''
    
    # ordino per numero di voti discendente
    data.sort_values('Voti', ascending=False, inplace=True, ignore_index=True)
    
    # ritorno un nuovo dataframe con il PartitoCollegato della prima riga e i Voti della 
    res = pd.DataFrame(columns=['PartitoCollegato','VotiVincenti'])
    if data.at[0,'PartitoCollegato'] != '':
        return res.append({'PartitoCollegato': data.at[0,'PartitoCollegato'], 'VotiVincenti': data.at[1,'Voti']+1}, ignore_index=True)
    else:
        return res


def merge_votivincenti_mattarellum(*a, data, voti_proporzionale, **kwargs):
    '''
    Viene chiamato nel contesto di una circoscrizione.
    Calcola la cifra elettorale circoscrizionale di ogni partito, effettuando lo scorporo.
    Ritorna un dataframe del tipo |Partito|Voti|Cifra| con i dati della circoscrizione.
    
    Parameters
    ----------
    data: dataframe del tipo |PartitoCollegato|Voti|VotiVincenti| con i dati dei collegi di questa cirscoscrizione già aggregati
    voti_proporzionali: dataframe del tipo |Partito|Voti| con i voti di questa cirscoscrizione
    '''
    # unisco i due dataframe
    res = data.copy()
    res.rename(columns = {'PartitoCollegato':'Partito'}, inplace=True)
    res = pd.merge(res, voti_proporzionale, on='Partito', how='outer')
    res.fillna(value=0, inplace=True)

    # effettuo lo scorporo
    res['Cifra'] = res['Voti'] - res['VotiVincenti']
    return res[['Partito','Voti','Cifra']]
    

def hare_mattarellum(*a, data, seggi_totali, **kwargs):
    '''
    Viene chiamato nel contesto della nazione.
    Calcolo la distrubuzione nazionale dei seggi usando il metodo Hare dei quozienti e dei più alti resti.
    Ritorna un dataframe del tipo |Partito|Seggi| con i seggi a livello di nazione.

    Parameters
    ----------
    data: dataframe del tipo |Partito|Voti|Cifra| con i dati delle circoscrizioni già aggregati
    seggi_totali: numero di seggi da assegnare a livello nazionale nella quota proporzionale
    '''

    print('calcolo distribuzione nazionale')
    
    res = data.copy()

    # calcolo il quoziente, i seggi e i resti per ogni partito
    q = int(res['Cifra'].sum() / seggi_totali)
    res['Seggi'] = res['Cifra'] // q
    res['Seggi'] = res['Seggi'].astype(int)
    res['Resto'] = res['Cifra'] / q - res['Seggi']
    
    # assegno i seggi rimanenti in ordine di resto, cifra discendente
    res.sort_values(['Resto','Cifra'], ascending=False, inplace=True)
    r = seggi_totali - res['Seggi'].sum()
    res.iloc[:r, res.columns.get_loc('Seggi')] += 1
    return res


def assegna_seggi_circoscrizione_mattarellum(*, information, distribution, district_votes, seggi_circoscrizione, **kwargs):
    '''
    Viene chiamato nel contesto di una circoscrizione.
    A partire dalle cifre circoscrizionali e dalla distribuzione nazionale dei seggi,
    assegna ad ogni partito i seggi che gli spettano sicuramente in questa circoscrizione.
    Ritorna un dataframe del tipo |Partito|Seggi|Resto|SeggiCircoscrizione|.

    Parameters
    ----------
    information: informazioni passate dal livello superiore (Nazione)
    distribution: dataframe del tipo |Partito|Seggi| contenente la distibuzione nazionale dei seggi
    district_votes: dataframe del tipo |Partito|Voti|Cifra| contenente i voti e le cifre elettorali circoscrizionali relativi a questa circoscrizione
    seggi_circoscrizione: numero di seggi da assegnare in questa circoscrizione nella quota proporzionale
    '''
    
    print('calcolo distribuzioni locali')

    district_votes.set_index('Partito', inplace=True)

    # calcolo il quoziente elettorale circoscrizionale
    somma_cifre = 0
    for _,r in distribution.iterrows():
        somma_cifre += district_votes.at[r['Partito'],'Cifra']
    q = somma_cifre / seggi_circoscrizione

    # assegno ad ogni partito i seggi che gli spettano sicuramente e mi segno il resto
    res = []
    for _,r in distribution.iterrows():
        cifra = district_votes.at[r['Partito'],'Cifra']
        seggi_assegnati = cifra // q
        res.append(pd.Series({'Partito':r['Partito'],'Seggi': seggi_assegnati, 'Resto': cifra / q - seggi_assegnati, 'SeggiCircoscrizione': seggi_circoscrizione}))
    
    return pd.concat(res, axis=1).T


def correggi_mattarellum(distretto, distribuzione_ideale, distribuzione_raccolta, info_locali, *info_comuni):
    '''
    Viene chiamato nel contesto della nazione.
    Corregge le distribuzioni locali dei seggi in base ai seggi rimasti e ai seggi che spettano
    a ciascun partito a livello nazionale.
    Ritorna un dizionario contenente tutte le distribuzioni locali dei seggi corrette.

    Parameters
    ----------
    distretto: la nazione
    distribuzione_ideale: dataframe del tipo |Partito|Seggi| con la distribuzione nazionale dei seggi
    distribuzione_raccolta: dizionario del tipo circoscrizione:distribuzione, dove distribuzione è un dataframe del tipo |Partito|Seggi| con i seggi già assegnati in quella circoscrizione
    info_locali: dizionario del tipo circoscrizione:info dove info è un dizionario che contiene i resti dei partiti e i seggi da assegnare in quella circoscrizione
    *info_comuni: informazioni comuni a tutta la lane
    '''

    print('correggo distribuzioni locali')
    
    distribuzione_ideale.set_index('Partito', inplace=True)

    # ottenog lista di tuple (circ, numseggi) ordinata per numero di seggi
    circoscrizioni = []
    for k,v in info_locali.items():
        circoscrizioni.append((k, v[list(v.keys())[0]]['SeggiCircoscrizione'])) 
    circoscrizioni.sort(key= lambda e: e[1])

    # ottengo dizionario del tipo partito: seggi_già_assegnati
    seggi_gia_assegnati = {}
    for k,v in distribuzione_raccolta.items():
        for _,r in v.iterrows():
            if r['Partito'] in seggi_gia_assegnati:
                seggi_gia_assegnati[r['Partito']] += r['Seggi']
            else:
                seggi_gia_assegnati[r['Partito']] = r['Seggi']
        v.set_index('Partito', inplace=True)

    # ottengo dizionario del tipo partito: seggi_dovuti_rimanenti
    seggi_dovuti = {}
    for k,v in seggi_gia_assegnati.items():
        seggi_dovuti[k] = distribuzione_ideale.at[k,'Seggi'] - v

    # finisco di assegnare i seggi rimasti nelle varie circoscrizioni
    for k,s in circoscrizioni:
        cur_distrib = distribuzione_raccolta[k] # distribuzione locale da correggere
        cur_info = info_locali[k] # info di questa circoscrizione

        # ottengo lista di tuple del tipo (partito, resto) ordinate per resto decrescente
        keys = []
        for k,v in cur_info.items():
            cur_info[k]['RestoUsato'] = False
            keys.append((k,cur_info[k]['Resto']))
        keys.sort(key= lambda e: e[1], reverse=True)
        
        seggi_da_assegnare = s - cur_distrib['Seggi'].sum()
        
        # assegno tutti i seggi rimasti in questa circoscrizione ai partiti in ordine di resto
        # e escludendo man mano quelli che non hanno più seggi spettanti a livello nazionale
        i = 0
        while seggi_da_assegnare > 0:
            cur_partito = keys[i][0]
            if seggi_dovuti[cur_partito] > 0:
                cur_distrib.at[cur_partito,'Seggi'] += 1
                cur_info[cur_partito]['RestoUsato'] = True
                seggi_da_assegnare -= 1
                seggi_dovuti[cur_partito] -=1
            i = (i + 1) % len(keys)

    # elimino da seggi_dovuti tutti i partiti che hanno avuto tutti i loro voti
    seggi_dovuti = {k:v for (k,v) in seggi_dovuti.items() if v > 0}
   
    # se alcuni partiti devono ricevere ancora dei voti li assegno a partire dalle circoscrizioni
    # in cui non hanno usato i loro resti
    for k1,v1 in seggi_dovuti.items():
        resti_circoscrizioni = []
        for k2,v2 in info_locali.items():
            resti_circoscrizioni.append((k2, v2[k1]['Resto'], v2[k1]['RestoUsato']))
        resti_circoscrizioni.sort(key= lambda e: (not e[2],e[1]), reverse=True)

        for i in range(int(v1)):
            distribuzione_raccolta[resti_circoscrizioni[i%len(resti_circoscrizioni)][0]].at[k1,'Seggi'] += 1
    
    # costruisco e ritorno il dizionario con le distribuzioni locali corrette
    return {k: v.reset_index() for k, v in distribuzione_raccolta.items()}, {}, {}


def show_chart(final_result):
    '''
    Produce un output visuale dei risultati finali della simulazione, nello specifico un pie chart.

    Parameters
    ----------
    final_result: lista di tuple del tipo (distretto, lane, partito, seggi_assegnati)
    '''

    # ottengo dizionario del tipo partito: seggi_assegnati_totali
    seats_dict = {}
    for c,l,p,s in final_result:
        if p in seats_dict.keys():
            seats_dict[p] += s
        else:
            seats_dict[p] = s

    # trasformo il dizionario in una lista di tuple ordinate per seggi decrescente
    part_seats = [(p,s) for p,s in seats_dict.items()]
    part_seats.sort(key= lambda e: e[1], reverse=True)
    
    # output human-readable dei risultati finali
    print(part_seats)

    # ottengo la lista dei partiti
    labels_list = [p for p,s in part_seats]
    labels = (*labels_list,)

    # ottengo al lista dei seggi
    sizes = [s for p,s in part_seats]
    
    # ottengo la lista dei colori
    all_colors = ['#1f78b4','#33a02c','#e31a1c','#ff7f00','#00796B','#6a3d9a','#b15928','#a6cee3','#b2df8a','#fb9a99','#fdbf6f','#4DB6AC','#cab2d6','#ffff99','#9E9E9E']
    colors = [all_colors[i%len(all_colors)] for i in range(len(part_seats))]
    
    explode = (*[0.15 for i in range(len(part_seats))],)

    # genero e mostro il pie chart
    patches, texts, third  = plt.pie(sizes, explode=explode, labels=labels,labeldistance=1.25, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=180)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.show()