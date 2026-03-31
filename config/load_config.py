import os
import yaml

class ConfigLoader:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_dir = os.path.join(self.project_root, "config")
        self.config_filenames = ["config_dev.yaml", "config.yaml"]
        self.config = self._load_config()

    def _load_config(self):
        for filename in self.config_filenames:
            config_path = os.path.join(self.config_dir, filename)
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    return yaml.safe_load(f)
        
        raise FileNotFoundError(f"None of the config files found: {self.config_filenames}")

    def get(self, *keys, default=None):
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

# Singleton instance
CONFIG = ConfigLoader()