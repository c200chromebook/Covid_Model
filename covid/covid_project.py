from datetime import datetime, timedelta
import configparser
import pandas as pd
import matplotlib.pyplot as plt

from covid.disease_objects.growth_scaling import GrowthScaling
from covid.disease_objects.population import Population

plt.close('all')

cfg = configparser.ConfigParser()
cfg.read("../Baseline.ini")
startdate = datetime.strptime(cfg['MODEL']['START_DATE'], "%Y-%m-%d")


multipliers = GrowthScaling(cfg)
pop = Population(cfg, startdate=startdate, multipliers=multipliers)
reports = [pop.report()]
dates = [startdate]
for day in range(cfg['MODEL'].getint('PROJECTION_PERIOD')):
    curdate = startdate + timedelta(days=day + 1)
    reports.append(pop.roll(multipliers[curdate]))
    dates.append(curdate)

results = pd.DataFrame(reports)
results.set_axis(0, dates)
#chart1 = results[['UNINFECTED', 'INCUBATION', 'INFECTIOUS', 'SICK', 'HOSPITAL', 'VENT', 'RECOVERED', 'DEAD']].plot.area()
chart1 = results[['INFECTIOUS', 'SICK', 'HOSPITAL', 'VENT']].plot.area()
chart2 = results[['NEW_INFECTED']].plot.area()
chart2 = results[['R_E']].plot.area()
results.to_clipboard(excel=True)
