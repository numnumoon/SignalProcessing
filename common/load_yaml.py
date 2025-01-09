import yaml


def load_yaml(yaml_file_path):
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


# test
if __name__ == "__main__":
    yamls = load_yaml("setting/CFAR.yaml")
    print(yamls)
