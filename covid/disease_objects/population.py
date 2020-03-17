from covid.disease_objects.disease import Disease



class Population:
    def __init__(self, cfg):
        self.disease = Disease(cfg)

        self.state = self.disease.backfill(
            cfg['POPULATION'].getint('DAYS_PREPROJECT'),
            cfg['POPULATION'].getfloat('SICK'))
        self.total = cfg['POPULATION'].getfloat('TOTAL')
        self.infected = self.state.infected  # Note - this will NOT reconcile to sick, due to invisible incubators.
        self.uninfected = self.total - self.infected
        self.dead = 0.0
        self.recovered = 0.0
        self.new_infected = 0.0
        self.susceptible_contact_frac =1.0
    @property
    def pop(self):
        self.uninfected + self.infected + self.dead + self.recovered
        assert abs(self.uninfected + self.infected + self.dead + self.recovered - self.total) < 0.001
        return self.total

    def roll(self):
        start_pop = self.pop
        self.susceptible_contact_frac = self.uninfected / (self.total - self.dead)
        contacts, deaths, recoveries = self.state.roll_nightly()
        self.new_infected = self.susceptible_contact_frac * contacts
        self.state.infect(self.new_infected)
        self.uninfected -= self.susceptible_contact_frac * contacts
        self.infected += self.new_infected - deaths - recoveries
        self.dead += deaths
        self.recovered += recoveries
        assert abs(self.infected - self.state.infected) < 0.001
        end_pop = self.pop
        assert abs(start_pop - end_pop) < 0.001

    def report(self):
        ret = {str(state): cases for state, cases in self.state.report().items()}
        ret['DEAD'] = self.dead
        ret['UNINFECTED'] = self.uninfected
        ret['RECOVERED'] = self.recovered
        ret['NEW_INFECTED'] = self.new_infected
        ret['SUSCEPTIBLE_CONTACT_FRAC'] = self.susceptible_contact_frac
        return ret









