import configparser
import pandas as pd
from covid.disease_objects.population import Population


cfg = configparser.ConfigParser()
cfg.read("../Baseline.ini")
pop = Population(cfg)
reports = [pop.report()]
for _ in range(cfg['MODEL'].getint('PROJECTION_PERIOD')):
    pop.roll()
    reports.append(pop.report())
pd.DataFrame(reports).to_clipboard(excel=True)



