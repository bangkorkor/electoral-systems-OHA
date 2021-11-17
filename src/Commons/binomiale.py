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


# file1 = pd.read_csv('/home/poliradio/AleZito/SimulatoreSistemiElettorali-2/LeggiElettorali/Binomiale/Data/Valle_Aosta/voti_valle_d_aosta.csv')
# data = file1.copy()
# binomiale_valle_daosta(data = data)
