from covid.disease_objects.disease import Disease

class Population:

    def __init__(self, cfg):
        self.uninfected = cfg['POPULATION']['UNINFECTED']
        self.disease = Disease(cfg)


