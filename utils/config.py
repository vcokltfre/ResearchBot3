from yaml import safe_load
from pathlib import Path


class ConfigLoader:
    def __init__(self, file: str = "./config.yml"):
        self.p = Path(file)

        if not self.p.exists():
            raise FileNotFoundError

        self.data = self.load()

    def load(self) -> dict:
        with self.p.open(encoding="utf-8") as f:
            return safe_load(f)

    def reload(self):
        self.data = self.load()

    def __getitem__(self, item: str):
        return self.data[item]

    def get(self, item: str, default=None):
        return self.data.get(item, default)
