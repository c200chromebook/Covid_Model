from covid.disease_objects.course import Course


class Disease:
    def __init__(self, cfg):
        self.r0 = cfg['GROWTH'].getfloat('BASIC_REPRODUCTIVE_NUMBER')
        self.states = {}

        self.courses = {Course(cfg,course) for course in cfg['COURSES']}
        print("HI!")


