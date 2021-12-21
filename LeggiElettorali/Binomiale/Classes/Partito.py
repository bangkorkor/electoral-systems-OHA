import pandas as pd
import yaml

conf = """
metaclasses:
  - logger # aggiunge automaticamente una funzione log
  - subclass

subclass:
    - PolEnt
"""

conf = yaml.safe_load(conf)

metas_p = list(map(eval, conf.pop("metaclasses")))
metas_p.append(cleanup)
metas_p
comb_p = type("combPol", tuple(metas_p), {})


class Partito(metaclass=comb_p, **conf):
    def elect(self, lane, district, seats, **info):
        return True

    def filter(self, district, *, total, row, dataframe, sbarramenti, **kwargs):
        return True
