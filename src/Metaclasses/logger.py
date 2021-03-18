import pandas as pd


class logger(type):
    def __new__(mcs, *args, **kwargs):
        o_log = args[2].get('log', lambda *a, **k: None)
        o_init = args[2].get('__init__', lambda *a, **k: None)

        def log(self, district, lane_name, **info):
            '''
            Registra delle informazioni nel log di una lane

            Parameters
            ----------
            district: distretto al quale si riferiscono le info
            lane_name: la lane della quale mi interessa registrare le info
            **info: informazioni passate come key arguments
            '''

            o_dic = self.logs.get(lane_name, {})
            o_dic[district] = pd.Series(info)
            self.logs[lane_name] = o_dic

        def get_log(self, lane):
            '''
            Restituisce un dataframe contenente i log di una lane

            Parameters
            ----------
            lane: la lane di cui voglio ottenere i log
            '''

            infos = list(self.logs.get(lane,{}).values())
            return pd.DataFrame(infos)

        def __init__(self, *a, **k):
            self.logs = {}
            return o_init(self, *a, **k)

        args[2]['log'] = log
        args[2]['get_log'] = get_log
        args[2]['__init__'] = __init__
        return super().__new__(mcs, *args, **kwargs)

    @classmethod
    def parse_conf(mcs, conf):
        return conf
