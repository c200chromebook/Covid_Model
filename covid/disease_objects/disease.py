from covid.disease_objects.course import Course


class DiseaseState:
    def __init__(self, disease):
        self.disease = disease
        self.states = [course.init_state() for course in disease.courses]

    def infect(self,n):
        [state.infect(n * state.course.probability) for state in self.states]

    def roll_nightly(self):
        contacts, deaths, recoveries = map(sum, zip(*[state.roll(self.disease.r0) for state in self.states]))
        return contacts, deaths, recoveries


class Disease:
    def __init__(self, cfg):
        self.r0 = cfg['GROWTH'].getfloat('BASIC_REPRODUCTIVE_NUMBER')
        self.states = {}
        self.courses = [Course(cfg, course, self.states) for course in cfg['COURSES']]
        assert sum(course.probability for course in self.courses) == 1.0

    def backfill(self, ageing_days):
        state = DiseaseState(self)
        state.infect(1)
        for _ in range(ageing_days):
            contacts, deaths, recoveries = state.roll_nightly()
            state.infect(contacts)
        return state











