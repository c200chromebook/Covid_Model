import configparser
import pandas as pd
import matplotlib.pyplot as plt

from covid.disease_objects.population import Population
from datetime import datetime, timedelta
plt.close('all')


cfg = configparser.ConfigParser()
cfg.read("../Baseline.ini")
startdate = datetime.strptime(cfg['MODEL']['START_DATE'],"%Y-%m-%d")
pop = Population(cfg)
reports = [pop.report()]
dates = [startdate]
for day in range(cfg['MODEL'].getint('PROJECTION_PERIOD')):
    pop.roll()
    reports.append(pop.report())
    dates.append(startdate + timedelta(days=day+1))
results = pd.DataFrame(reports)
results.set_axis(0, dates)
chart1=results[['UNINFECTED','INCUBATION','INFECTIOUS','SICK','HOSPITAL','VENT','RECOVERED','DEAD']].plot.area()
chart2=results[['NEW_INFECTED']].plot.area()
