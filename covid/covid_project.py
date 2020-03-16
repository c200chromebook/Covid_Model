import configparser
from covid.disease_objects.population import Population

def main():
    cfg = configparser.ConfigParser()
    cfg.read("../Baseline.ini")
    pop = Population(cfg)
    print("OK")



if __name__ == '__main__':
    main()