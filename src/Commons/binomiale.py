import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys



def binomiale_valle_daosta(*a, data, **kwargs):
    """Function that elect 2 politicians of Valle D'Aosta region"""
    #print("\n---> ELEGGO IL SEGGIO DELLA VALLE D'AOSTA <---\n")

    # Copies data taken from with pandas's library function
    dataframe_aosta = data.copy()
    # Sorting values
    dataframe_aosta.sort_values('VOTI_LISTA', ascending=False, inplace=True)

    dataframe_aosta['Seggi'] = 0


    voti_primo = dataframe_aosta.iloc[0, dataframe_aosta.columns.get_loc('VOTI_LISTA')]
    voti_secondo = dataframe_aosta.iloc[1, dataframe_aosta.columns.get_loc('VOTI_LISTA')]

    # The system works in the following manner: Parties and independent candidates group themselves into lists or coalitions, basically electoral blocs. 
    # Each list proposes up to two candidates per electoral region, province, or other geographical unit. 
    # Votes are first tallied by list instead of by candidate, and unless the list which obtained the first majority has double the voting 
    # as the second majority, each of the two lists gets one of their candidates, the one who got the most voting, into office
    
    if(voti_primo < voti_secondo * 2):
        dataframe_aosta.iloc[0:2, dataframe_aosta.columns.get_loc('Seggi')] = 1
        dataframe_aosta.iloc[2:, dataframe_aosta.columns.get_loc('Seggi')] = 0
    else:
        dataframe_aosta.iloc[0, dataframe_aosta.columns.get_loc('Seggi')] = 2
        dataframe_aosta.iloc[1:, dataframe_aosta.columns.get_loc('Seggi')] = 0



    dataframe_aosta = dataframe_aosta.rename(columns={'Voti': 'Numero'})

    #print(dataframe_aosta)

    return dataframe_aosta


def binomiale_estero(*a, data, **kwargs):

    dataframe_estero = data.copy()
    dataframe_estero['Seggi'] = 0
    # print(dataframe_estero)


    #list(set(dataframe_estero["Ente"]))

    enti = list(set(dataframe_estero["Ente"]))
    enti.sort()
    print(enti)

    liste = dataframe_estero.groupby(['Ente'])['Lista'].apply(list)
    voti = dataframe_estero.groupby(['Ente'])['Voti'].apply(list)

    # print(list(set(dataframe_estero["Ente"])))
    #dataframe = dataframe_estero.groupby(['Ente'])['Lista'].apply(list)
    #print(dataframe)

    
    dataframe_estero = pd.DataFrame(columns = ['Ente', 'Lista', 'Voti', 'Seggi'])
    

    for ente in enti:
        # print(liste[ente])
        # print(voti[ente])

        if (voti[ente][0] < voti[ente][1] * 2):
            dataframe_estero = dataframe_estero.append({'Ente': ente, 'Lista': liste[ente][0], 'Voti': voti[ente][0], 'Seggi': 1}, ignore_index=True)
            dataframe_estero = dataframe_estero.append({'Ente': ente, 'Lista': liste[ente][1], 'Voti': voti[ente][1], 'Seggi': 1}, ignore_index=True)
        else:
            dataframe_estero = dataframe_estero.append({'Ente': ente, 'Lista': liste[ente][0], 'Voti': voti[ente][0], 'Seggi': 2}, ignore_index=True)           

    print(dataframe_estero)
        

        # subdataframe = dataframe_estero[dataframe_estero["Ente"] == ente]
        # voti_primo = subdataframe.iloc[0, subdataframe.columns.get_loc('Voti')]
        # voti_secondo = subdataframe.iloc[1, subdataframe.columns.get_loc('Voti')]
    sys.exit()

    # subdataframe = dataframe_estero[dataframe_estero["Ente"] == 'RESTO DEL MONDO']
    # print(subdataframe)
    
    # voti_primo = subdataframe.iloc[0, subdataframe.columns.get_loc('Voti')]
    # voti_secondo = subdataframe.iloc[1, subdataframe.columns.get_loc('Voti')]
    # index_primo = subdataframe.index[subdataframe['Ente'] == 'RESTO DEL MONDO'].tolist()

    # print(index_primo)
    sys.exit()

    # The system works in the following manner: Parties and independent candidates group themselves into lists or coalitions, basically electoral blocs. 
    # Each list proposes up to two candidates per electoral region, province, or other geographical unit. 
    # Votes are first tallied by list instead of by candidate, and unless the list which obtained the first majority has double the voting 
    # as the second majority, each of the two lists gets one of their candidates, the one who got the most voting, into office
    
    if(voti_primo < voti_secondo * 2):
        subdataframe.iloc[0:2, subdataframe.columns.get_loc('Seggi')] = 1
        subdataframe.iloc[2:, subdataframe.columns.get_loc('Seggi')] = 0
    else:
        subdataframe.iloc[0, subdataframe.columns.get_loc('Seggi')] = 2
        subdataframe.iloc[1:, subdataframe.columns.get_loc('Seggi')] = 0

    print(subdataframe)
    sys.exit()

    return dataframe_estero

file1 = pd.read_csv('/home/poliradio/AleZito/SimulatoreSistemiElettorali-2/LeggiElettorali/Binomiale/Data/Circoscrizione_Estera/voti_estero.csv')
data = file1.copy()
binomiale_estero(data = data)