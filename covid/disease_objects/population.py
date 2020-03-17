from covid.disease_objects.disease import Disease


class Population:
    def __init__(self, cfg):
        self.disease = Disease(cfg)
        self.init_well = cfg['POPULATION']['WELL']
        self.init_sick = cfg['POPULATION']['SICK']





