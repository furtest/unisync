from dataclasses import dataclass
import ipaddress
from typing import Union

import yaml

@dataclass
class ServerConfig:
    hostname: str = ""
    ip: str = ""
    port: int = 22
    user: str
    sshargs: list

    def __post_init__(self):
        if self.ip == "" and self.hostname == "":
            raise ValueError("A remote must be provided (ip or hostname)")

        if self.ip != "":
            try:
                ipaddress.ip_address(self.ip)
            except ValueError:
                raise ValueError("The provided ip address is invalid")

@dataclass
class RootsConfig:
    local: str
    remote: str

@dataclass
class Config:
    server: ServerConfig
    roots: RootsConfig

    def load_config(config_path:str):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        return config

if __name__ == "__main__":
    config = load_config("config.yaml")
    print(config)
