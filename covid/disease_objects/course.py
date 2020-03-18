from collections import defaultdict
from covid.disease_objects.state import State
from covid.util.util import parse_tuple_list


class CourseState:
    def __init__(self, course):
        self.course = course
        self.day_state = [state for state, days in self.course.disease_course for _ in range(days)]
        self.day_cases = [0.0 for _ in range(course.maxlength)]

    @property
    def infected(self):
        return sum(self.day_cases)

    def infect(self, n):
        self.day_cases[0] += n

    def roll(self, r0, growth_mult=1.0):
        contacts = sum([infect_frac * lives * r0 * growth_mult for infect_frac, lives in
                        zip(self.course.infection_fraction_vec, self.day_cases)])
        deaths = self.day_cases[self.course.death_on - 1] * self.course.prob_death if self.course.prob_death else 0.0
        if deaths:
            self.day_cases[self.course.death_on - 1] -= deaths
        self.day_cases.insert(0, 0.0)
        recoveries = self.day_cases.pop()
        return contacts, deaths, recoveries

    def report(self):
        ret = defaultdict(float)
        for state, cases in zip(self.day_state, self.day_cases):
            ret[state] += cases
        return ret

    def scale(self, factor):
        self.day_cases = [factor * cases for cases in self.day_cases]


class Course:
    def __init__(self, cfg, course_name, states):
        def add_state(st):
            if st in states:
                return states[st]
            else:
                new_state = State(cfg, st)
                states[st] = new_state
                return new_state

        course_temp = parse_tuple_list(cfg[course_name]['COURSE'])
        self.prob_death = cfg[course_name].getfloat('PROB_DEATH') if 'PROB_DEATH' in cfg[course_name] else None
        self.death_on = cfg[course_name].getint('DEATH_ON') if self.prob_death else None
        self.disease_course = [(add_state(state_name), int(days)) for state_name, days in course_temp]
        self.probability = cfg['COURSES'].getfloat(course_name)

        total_state_days = defaultdict(int)
        for state, days in self.disease_course:
            total_state_days[state] += days
        daily_infection_fraction = {}
        for state in total_state_days:
            daily_infection_fraction[state] = state.percent_of_infections / float(total_state_days[state])
        self.infection_fraction_vec = [daily_infection_fraction[state]
                                       for state, days in self.disease_course
                                       for _ in range(days)]


    @property
    def maxlength(self):
        return sum([days for state, days in self.disease_course])

    def init_state(self):
        return CourseState(self)





