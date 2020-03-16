import re


class Course:
    def __init__(self, cfg, course_name):
        self.outcome = cfg[course_name]['OUTCOME']
        self.course = [tuple(state.split(',')) for state in re.findall(r'(\(\w+,\d+\))', cfg[course_name]['COURSE'])]



