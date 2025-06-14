# Copyright (C) 2025 Paul Retourné
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, field
import ipaddress
from typing import Union, Optional

import pyrallis

@dataclass
class ServerConfig:
    user: str
    sshargs: Optional[list[str]] = field(default_factory=list)
    hostname: str = ""
    ip: str = ""
    port: int = 22

    def __post_init__(self):
        print(self.ip)
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
    cfg = pyrallis.parse(config_class=Config, config_path="/home/furtest/files/programmation/unisync/config.yaml")
