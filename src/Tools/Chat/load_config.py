import argparse
import yaml
import os

EXIT_ERR = 84

def load_config(parser: argparse.ArgumentParser):
    parser.add_argument("config", help="path to the yaml config file")

    args = parser.parse_args()

    try:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: config file not found : {args.config}")
        return EXIT_ERR, None
    except yaml.YAMLError as e:
        print(f"Error: failed to parse config file : {e}")
        return EXIT_ERR, None

    if not isinstance(config, dict):
        print("Error: invalid config format")
        return EXIT_ERR, None

    required_keys = ["model", "system"]
    missing = [key for key in required_keys if config.get(key) is None]
    if missing:
        print(f"Error: missing config keys: {', '.join(missing)}")
        return EXIT_ERR, None

    config_dir = os.path.dirname(os.path.abspath(args.config))
    system_path = os.path.join(config_dir, config["system"])

    try:
        with open(system_path, "r") as f:
            config["system"] = f.read()
    except FileNotFoundError:
        print(f"Error: system file not found : {system_path}")
        return EXIT_ERR, None

    return 0, config
