from covid.disease_objects.disease import Disease



class Population:
    def __init__(self, cfg, startdate=None, multipliers=None):
        self.disease = Disease(cfg)

        self.state = self.disease.backfill(
            cfg['POPULATION'].getint('DAYS_PREPROJECT'),
            cfg['POPULATION'].getfloat('SICK'), startdate=startdate,multipliers=multipliers)
        self.total = cfg['POPULATION'].getfloat('TOTAL')
        self.infected = self.state.infected  # Note - this will NOT reconcile to sick, due to invisible incubators.
        self.uninfected = self.total - self.infected
        self.dead = 0.0
        self.recovered = 0.0

    @property
    def pop(self):
        self.uninfected + self.infected + self.dead + self.recovered
        assert abs(self.uninfected + self.infected + self.dead + self.recovered - self.total) < 0.001
        return self.total

    def report(self, susceptible_contact_frac=1.0, growth_mult=1.0,new_infected=0.0):
        ret = {str(state): cases for state, cases in self.state.report().items()}
        ret['DEAD'] = self.dead
        ret['UNINFECTED'] = self.uninfected
        ret['RECOVERED'] = self.recovered
        ret['NEW_INFECTED'] = new_infected
        ret['R_E'] = susceptible_contact_frac * self.disease.r0 * growth_mult
        return ret

    def roll(self, growth_mult=1.0):
        start_pop = self.pop
        susceptible_contact_frac = self.uninfected / (self.total - self.dead)
        contacts, deaths, recoveries = self.state.roll_nightly(growth_mult=growth_mult)
        new_infected = susceptible_contact_frac * contacts
        self.state.infect(new_infected)
        self.uninfected -= susceptible_contact_frac * contacts
        self.infected += new_infected - deaths - recoveries
        self.dead += deaths
        self.recovered += recoveries
        self.growth_mult = growth_mult
        assert abs(self.infected - self.state.infected) < 0.001
        end_pop = self.pop
        assert abs(start_pop - end_pop) < 0.001
        return self.report(
            susceptible_contact_frac=susceptible_contact_frac,
            growth_mult=growth_mult,
            new_infected=new_infected)










