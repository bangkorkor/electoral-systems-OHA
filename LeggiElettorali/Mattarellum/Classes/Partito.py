import pandas as pd
import numpy as np
import yaml


# inizializzo questa classe usando una configurazione yaml
# creo una metaclasse metas_p che eredita da loger, PolEnt e party ed è subclass di PolEnt
conf = 'metaclasses:\n  - logger\n  - PolEnt\n  - party\n\nsubclass:\n  - PolEnt'

conf = yaml.safe_load(conf)

metas_p = list(map(eval, conf.pop("metaclasses")))
metas_p.append(cleanup)

# istanzio la metaclasse, ottenendo la classe comb_p
comb_p = type("combPol", tuple(metas_p), {})

class Partito(metaclass=comb_p, **conf):
    '''
    Questa classe è una PolEnt usata per rappresentare un partito politico.
    '''
    
    def filter(self, district, *, total, row, dataframe, sbarramenti, **kwargs):
        '''
        Viene chiamato dai totals per filtrare questo tipo di PolEnt.
        Quando la Nazione usa un totals con sbarramento "soglia" applica la soglia del 4%,
        cioè ritorna True solo se l'istanza su cui viene invocato questo metodo ha raggiunto
        almeno il 4% dei voti totali nelle circoscrizioni plurinominali.

        Parameters
        ----------
        district: distretto corrente (Collegio, Circoscrizione o Nazione)
        total: il totals che ha invocato questo metodo
        row: riga del dataframe con chiave corrispondente alla istanza corrente
        dataframe: dataframe su cui sta operando il total
        sbarramenti: sbarramento passato come parametro al total
        '''

        # se la nazione applica lo sbarramento "soglia", sommo i voti del dataframe
        # e ritorno True solo se questa istanza ha almeno il 4%
        if sbarramenti[0] == 'soglia' and district.type == 'Nazione':
            tot_voti = dataframe['Voti'].sum()
            p_voti = row['Voti']
            return p_voti > tot_voti * 0.04
        return True