from configparser import ConfigParser


class State:
    def __hash__(self):
        return hash(self.state_name)

    def __eq__(self, other):
        return self.state_name == other.state_name

    def __str__(self):
        return self.state_name

    def __repr__(self):  # This is a white lie, and is very handy.
        return self.state_name

    def __init__(self, cfg: ConfigParser, state_name):
        self.state_name = state_name
        if state_name in cfg['GROWTH_TIMING']:
            self.percent_of_infections = float(cfg['GROWTH_TIMING'][state_name])
        else:
            self.percent_of_infections = 0.0
        if state_name in cfg['VISIBLE']:
            self.visible = cfg['VISIBLE'].getboolean(state_name)
        else:
            self.visible = True


