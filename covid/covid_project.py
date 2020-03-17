import configparser
from covid.disease_objects.population import Population


cfg = configparser.ConfigParser()
cfg.read("../Baseline.ini")
pop = Population(cfg)
backfill = pop.disease.backfill(15)


