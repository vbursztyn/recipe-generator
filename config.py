from yaml import load


def get_config():
    with open('config.yaml', 'r') as config_f:
        return load(config_f.read())