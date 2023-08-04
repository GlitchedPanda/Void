import json
import sys
from pathlib import Path

class Config:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self._load_config()

    def _load_config(self):
        with open(self.config_file_path, "r") as config_file:
            self.config_data = json.load(config_file)

    def save_config(self):
        with open(self.config_file_path, "w") as config_file:
            json.dump(self.config_data, config_file, indent=4)

    def __getattr__(self, name):
        return self.config_data.get(name)

    def __setattr__(self, name, value):
        if name in ("config_file_path", "config_data"):
            super().__setattr__(name, value)
        else:
            self.config_data[name] = value
            self.save_config()

config_file_path = Path(sys.argv[0]).parent.parent / 'resources' / "Void.json"
config = Config(config_file_path)
