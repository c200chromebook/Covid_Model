import re
from covid.disease_objects.state import State
from collections import defaultdict

class CourseState:
    def __init__(self, course):
        self.course = course
        self.day_track = [0.0 for _ in range(course.maxlength)]

    @property
    def sick(self):
        return sum(self.day_track)

    def infect(self, n):
        self.day_track[0] += n

    def roll(self, r0):
        contacts = sum([infect_frac * lives * r0 for infect_frac, lives in
                        zip(self.course.infection_fraction_vec, self.day_track)])
        deaths = self.day_track[self.course.death_on-1] * self.course.prob_death if self.course.prob_death else 0.0
        if deaths:
            self.day_track[self.course.death_on-1] -= deaths
        self.day_track.insert(0, 0.0)
        recoveries = self.day_track.pop()
        return contacts, deaths, recoveries


class Course:
    def __init__(self, cfg, course_name, states):
        def add_state(state):
            if state in states:
                return states[state]
            else:
                new_state = State(cfg, state)
                states[state] = new_state
                return new_state

        course_temp = [tuple(state.strip('()').split(',')) for state in re.findall(r'(\(\w+,\d+\))', cfg[course_name]['COURSE'])]
        self.prob_death = cfg[course_name].getfloat('PROB_DEATH') if 'PROB_DEATH' in cfg[course_name] else None
        self.death_on = cfg[course_name].getint('DEATH_ON') if self.prob_death else None
        self.course = [(add_state(state_name), int(days)) for state_name, days in course_temp]
        self.probability = cfg['COURSES'].getfloat(course_name)

        total_state_days = defaultdict(int)
        for state, days in self.course:
            total_state_days[state] += days
        daily_infection_fraction = {}
        for state in total_state_days:
            daily_infection_fraction[state] = state.percent_of_infections / float(total_state_days[state])
        self.infection_fraction_vec = [daily_infection_fraction[state]
                                       for state, days in self.course
                                       for _ in range(days)]


    @property
    def maxlength(self):
        return sum([days for state, days in self.course])

    def init_state(self):
        return CourseState(self)





