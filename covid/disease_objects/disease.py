from collections import defaultdict
from datetime import timedelta

from covid.disease_objects.course import Course


class DiseaseState:
    def __init__(self, disease):
        self.disease = disease
        self.course_states = [course.init_state() for course in disease.courses]

    def infect(self, n):
        [state.infect(n * state.course.probability) for state in self.course_states]

    def roll_nightly(self, growth_mult=None):
        contacts, deaths, recoveries = map(sum, zip(*[state.roll(r0=self.disease.r0, growth_mult=growth_mult)
                                                      for state
                                                      in self.course_states]))
        return contacts, deaths, recoveries

    def report(self):
        ret = defaultdict(float)
        for course_state in self.course_states:
            for state, amount in course_state.report().items():
                ret[state] += amount
        return ret

    @property
    def infected(self):
        return sum([x.infected for x in self.course_states])

    def scale(self, factor):
        [course_state.scale(factor) for course_state in self.course_states]


class Disease:
    def __init__(self, cfg):
        self.r0 = cfg['GROWTH'].getfloat('BASIC_REPRODUCTIVE_NUMBER')
        self.states = {}
        self.courses = [Course(cfg, course, self.states) for course in cfg['COURSES']]
        assert sum(course.probability for course in self.courses) == 1.0

    def backfill(self, aging_days, sick, startdate=None, multipliers=None):
        # Runs ignoring population immunity, assumed irrelevant early outbreak.
        state = DiseaseState(self)
        state.infect(1)
        use_mutiples = startdate and multipliers
        if use_mutiples:
            curdate = startdate - timedelta(days=aging_days)
        for _ in range(aging_days):
            contacts, deaths, recoveries = state.roll_nightly(growth_mult=multipliers[curdate] if use_mutiples else 1.0)
            state.infect(contacts)
            if startdate and multipliers:
                curdate += timedelta(days=1)

        report = state.report()
        visible_cases = sum([cases for state, cases in report.items() if state.visible])
        state.scale(sick / visible_cases)
        return state











