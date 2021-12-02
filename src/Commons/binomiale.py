"""
The system works in the following manner: Parties and independent candidates group themselves into lists or coalitions, basically electoral blocs. 
Each list proposes up to two candidates per electoral region, province, or other geographical unit. 
Votes are first tallied by list instead of by candidate, and unless the list which obtained the first majority has double the voting 
as the second majority, each of the two lists gets one of their candidates, the one who got the most voting, into office
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# associazioni = {}
# associazioni_aosta = {}

# def dividi_partiti(*a, data, **kwargs):
#     global associazioni
#     dataframe = data.copy()
#     for index, row in dataframe.iterrows():
#         if row['Partito'] not in associazioni:
#             associazioni[row['Partito']] = row['Coalizione']




# def input_valle_daosta(*a, data, **kwargs):
#     global dataset_finale
#     dataframe = data.copy()
#     for index, row in dataframe.iterrows():
#         dataset_finale.append({'Ente': row['Ente'], 'Coalizione': row['Lista'], 'Partito': row['Lista'], 'Voti': row['Voti'], 'Seggi': 0}, ignore_index=True)


# def input_italia(*a, data, **kwargs):
#     global dataset_finale
#     dataframe = data.copy()
#     for index, row in dataframe.iterrows():
#         dataset_finale.append({'Ente': row['Ente'], 'Coalizione': row['Coalizione'], 'Partito': row['Partito'], 'Voti': row['Voti'], 'Seggi': 0}, ignore_index=True)


# def input_estero(*a, data, **kwargs):
#     global dataset_finale
#     dataframe = data.copy()
#     for index, row in dataframe.iterrows():
#         dataset_finale.append({'Ente': row['Ente'], 'Coalizione': row['Coalizione'], 'Partito': row['Lista'], 'Voti': row['Voti'], 'Seggi': 0}, ignore_index=True)
#         print(row)
#     print(dataset_finale)



def binomiale_valle_daosta(*a, data, **kwargs):
    dataframe_aosta = data.copy()

    enti = list(set(dataframe_aosta['Ente']))
    enti.sort()
    print(enti)

    partiti = dataframe_aosta.groupby(['Ente'])['Partito'].apply(list)
    voti = dataframe_aosta.groupby(['Ente'])['Voti'].apply(list)

    dataframe_aosta = pd.DataFrame(columns = ['Ente', 'Partito', 'Voti', 'Seggi'])

    for ente in enti:
        if (voti[ente][0] < voti[ente][1] * 2):
            dataframe_aosta = dataframe_aosta.append({'Ente': ente, 'Partito': partiti[ente][0], 'Voti': voti[ente][0], 'Seggi': 1}, ignore_index=True)
            dataframe_aosta = dataframe_aosta.append({'Ente': ente, 'Partito': partiti[ente][1], 'Voti': voti[ente][1], 'Seggi': 1}, ignore_index=True)
        else:
            dataframe_aosta = dataframe_aosta.append({'Ente': ente, 'Partito': partiti[ente][0], 'Voti': voti[ente][0], 'Seggi': 2}, ignore_index=True)           


    # voti_primo = dataframe_aosta.iloc[0, dataframe_aosta.columns.get_loc('VOTI_LISTA')]
    # voti_secondo = dataframe_aosta.iloc[1, dataframe_aosta.columns.get_loc('VOTI_LISTA')]

    
    
    # if(voti_primo < voti_secondo * 2):
    #     dataframe_aosta.iloc[0:2, dataframe_aosta.columns.get_loc('Seggi')] = 1
    #     dataframe_aosta.iloc[2:, dataframe_aosta.columns.get_loc('Seggi')] = 0
    # else:
    #     dataframe_aosta.iloc[0, dataframe_aosta.columns.get_loc('Seggi')] = 2
    #     dataframe_aosta.iloc[1:, dataframe_aosta.columns.get_loc('Seggi')] = 0



    # dataframe_aosta = dataframe_aosta.rename(columns={'Voti': 'Numero'})

    print(dataframe_aosta)

    return dataframe_aosta
    



# def binomiale_valle_daosta(*a, data, **kwargs):
#     """Function that elect 2 politicians of Valle D'Aosta region"""
#     #print("\n---> ELEGGO IL SEGGIO DELLA VALLE D'AOSTA <---\n")

#     # Copies data taken from with pandas's library function
#     dataframe_aosta = data.copy()
#     # Sorting values
#     dataframe_aosta.sort_values('VOTI_LISTA', ascending=False, inplace=True)

#     dataframe_aosta['Seggi'] = 0


#     voti_primo = dataframe_aosta.iloc[0, dataframe_aosta.columns.get_loc('VOTI_LISTA')]
#     voti_secondo = dataframe_aosta.iloc[1, dataframe_aosta.columns.get_loc('VOTI_LISTA')]

    
    
#     if(voti_primo < voti_secondo * 2):
#         dataframe_aosta.iloc[0:2, dataframe_aosta.columns.get_loc('Seggi')] = 1
#         dataframe_aosta.iloc[2:, dataframe_aosta.columns.get_loc('Seggi')] = 0
#     else:
#         dataframe_aosta.iloc[0, dataframe_aosta.columns.get_loc('Seggi')] = 2
#         dataframe_aosta.iloc[1:, dataframe_aosta.columns.get_loc('Seggi')] = 0



#     dataframe_aosta = dataframe_aosta.rename(columns={'Voti': 'Numero'})

#     #print(dataframe_aosta)

#     return dataframe_aosta


def binomiale_estero(*a, data, **kwargs):

    dataframe_estero = data.copy()
    dataframe_estero['Seggi'] = 0

    enti = list(set(dataframe_estero['Ente']))
    enti.sort()
    print(enti)

    coalizioni = dataframe_estero.groupby(['Ente'])['Coalizione'].apply(list)
    partiti = dataframe_estero.groupby(['Ente'])['Partito'].apply(list)
    voti = dataframe_estero.groupby(['Ente'])['Voti'].apply(list)

    # print(list(set(dataframe_estero["Ente"])))
    #dataframe = dataframe_estero.groupby(['Ente'])['Lista'].apply(list)
    #print(dataframe)
    
    dataframe_estero = pd.DataFrame(columns = ['Ente', 'Coalizione', 'Partito', 'Voti', 'Seggi'])
    
    for ente in enti:

        if (voti[ente][0] < voti[ente][1] * 2):
            dataframe_estero = dataframe_estero.append({'Ente': ente, 'Coalizione': coalizioni[ente][0], 'Partito': partiti[ente][0], 'Voti': voti[ente][0], 'Seggi': 1}, ignore_index=True)
            dataframe_estero = dataframe_estero.append({'Ente': ente, 'Coalizione': coalizioni[ente][1], 'Partito': partiti[ente][1], 'Voti': voti[ente][1], 'Seggi': 1}, ignore_index=True)
        else:
            dataframe_estero = dataframe_estero.append({'Ente': ente, 'Coalizione': coalizioni[ente][0], 'Partito': partiti[ente][0], 'Voti': voti[ente][0], 'Seggi': 2}, ignore_index=True)           

    print(dataframe_estero)
    
    return dataframe_estero


def binomiale_italia(*a, data, **kwargs):
    dataframe_italia = data.copy()

    dataframe_italia = dataframe_italia.sort_values(['Regione', 'Ente', 'Voti'], ascending = (True, True, False))
    print(dataframe_italia)

    enti = list(set(dataframe_italia['Ente']))
    enti.sort()
    print(enti)

    coalizioni = dataframe_italia.groupby(['Ente'])['Coalizione'].apply(list)
    partiti = dataframe_italia.groupby(['Ente'])['Partito'].apply(list)
    voti = dataframe_italia.groupby(['Ente'])['Voti'].apply(list)
    print(partiti)
    print(voti)

    dataframe_italia = pd.DataFrame(columns = ['Ente', 'Coalizione', 'Partito', 'Voti', 'Seggi'])
    
    for ente in enti:

        if (voti[ente][0] < voti[ente][1] * 2):
            dataframe_italia = dataframe_italia.append({'Ente': ente, 'Coalizione': coalizioni[ente][0], 'Partito': partiti[ente][0], 'Voti': voti[ente][0], 'Seggi': 1}, ignore_index=True)
            dataframe_italia = dataframe_italia.append({'Ente': ente, 'Coalizione': coalizioni[ente][1], 'Partito': partiti[ente][1], 'Voti': voti[ente][1], 'Seggi': 1}, ignore_index=True)
        else:
            dataframe_italia = dataframe_italia.append({'Ente': ente, 'Coalizione': coalizioni[ente][0], 'Partito': partiti[ente][0], 'Voti': voti[ente][0], 'Seggi': 2}, ignore_index=True)           


    # print(dataframe_italia)
    
    return dataframe_italia



def binomiale_assegna_seggi(*a, dataframe_italia, dataframe_aosta, dataframe_estero, **kwargs):

    seggi_assegnati = {}
    dataframe_italia = dataframe_italia.sort_values(['Coalizione'], ascending = True)
    dataframe_italia.loc[dataframe_italia['Coalizione'] == 'NO COALIZIONE', 'Coalizione'] = dataframe_italia['Partito']

    dataframe_estero = dataframe_estero.sort_values(['Coalizione'], ascending = True)
    dataframe_estero.loc[dataframe_estero['Coalizione'] == 'NO COALIZIONE', 'Coalizione'] = dataframe_estero['Partito']

    dataframe_aosta = dataframe_aosta.sort_values(['Partito'], ascending = True)

    coalizioni = list(set(dataframe_italia['Coalizione']))
    partiti = list(set(dataframe_aosta['Partito']))


    for coalizione in coalizioni:
        seggi_assegnati[coalizione] = dataframe_italia.loc[dataframe_italia['Coalizione'] == coalizione, 'Seggi'].sum() + dataframe_estero.loc[dataframe_estero['Coalizione'] == coalizione, 'Seggi'].sum()
        # seggi_assegnati[coalizione] = seggi_assegnati[coalizione] + dataframe_estero.loc[dataframe_estero['Coalizione'] == coalizione, 'Seggi'].sum()

        # seggi_assegnati[coalizione] = dataframe_estero.loc[dataframe_estero['Coalizione'] == coalizione, 'Seggi'].sum()

    for partito in partiti:
        seggi_assegnati[partito] = dataframe_aosta.loc[dataframe_aosta['Partito'] == partito, 'Seggi'].sum()
        
    print(seggi_assegnati)


    return seggi_assegnati





    
    # dataframe_finale = pd.DataFrame(columns = ['Coalizione', 'Partito', 'Seggi'])

    
    # partiti = list(set(dataframe_italia["Partito"]))
    # partiti.sort()
    # print(partiti)

    # seggi = dataframe_italia.groupby(['Partito'])['Seggi'].apply(list)
    # print(seggi)
    
    # for partito in partiti:
    #     sum(seggi[partito])
    #     dataframe_finale = dataframe_finale.append({'Coalizione': ente, 'Partito': liste[ente][0], 'Voti': voti[ente][0], 'Seggi': 1}, ignore_index=True)




# SEZIONE VISUALIZZAZIONE <-------------------------------------------------------- #

def show_result(result):
    
    dataOutput = pd.DataFrame(result.items(), columns =['Partito', 'Seggi'])
    dataOutput['Seggi'] = dataOutput['Seggi'].astype(int)
    dataOutput['Percentuali'] = round(dataOutput['Seggi'] / 214, 5)
    dataOutput = dataOutput.sort_values(['Seggi'], ascending = False)


    labels = []
    for index, row in dataOutput.iterrows():
        labels.append("{:.2f}%\n({:d} seats)".format(row['Percentuali'] * 100, row['Seggi']))

    print(dataOutput)
    
    fig, ax = plt.subplots(figsize=(15, 9), subplot_kw=dict(aspect="equal"))

    data = dataOutput['Seggi']
    partiti = dataOutput['Partito']

    # frame = []
    # exp = 0.01
    # for index in range(len(dataOutput)):
    #     frame.append(exp)
    #     exp *= 1.4

    # def func(pct, allvals):
    #     absolute = int(pct/100.*np.sum(allvals))
    #     return "{:.1f}%\n({:d} seats \ {:f})".format(pct, absolute, pct)
    #     autopct=lambda pct: func(pct, data)


    wedges, texts = ax.pie(data, labels = labels, labeldistance = 0.6,
                                      textprops=dict(color="black"), explode = None)

    ax.legend(wedges, partiti,
              title="Coalizione/Partito",
              loc="upper left",
              bbox_to_anchor=(1.01, 0.08, 0.5, 1))

    plt.setp(texts, size=4, weight="bold")

    ax.set_title("Distribuzione Nazionale Camera dei Deputati 2013 con Legge Binomiale", loc='left')



    plt.savefig('./binomiale.png', dpi=300)
    plt.show()



file1 = pd.read_csv('/home/poliradio/AleZito/SimulatoreSistemiElettorali-2/LeggiElettorali/Binomiale/Data/Circoscrizione_Estera/voti_estero.csv')
file2 = pd.read_csv('/home/poliradio/AleZito/SimulatoreSistemiElettorali-2/LeggiElettorali/Binomiale/Data/Valle_Aosta/voti_valle_d_aosta.csv')
file3 = pd.read_csv('/home/poliradio/AleZito/SimulatoreSistemiElettorali-2/LeggiElettorali/Binomiale/Data/Regione/voti_province.csv')


italia = file3.copy()
estero = file1.copy()
aosta = file2.copy()

seggi_estero = binomiale_estero(data = estero)
seggi = binomiale_italia(data = italia)
seggi_aosta = binomiale_valle_daosta(data = aosta)
result = binomiale_assegna_seggi(dataframe_italia = seggi, dataframe_estero = seggi_estero, dataframe_aosta = seggi_aosta)
show_result(result = result)

