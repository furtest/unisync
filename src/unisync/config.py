# Copyright (C) 2025 Paul Retourné
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, field
import ipaddress
import configparser
from configparser import UNNAMED_SECTION

@dataclass
class ServerConfig:
    user: str
    sshargs: list[str] | None = field(default_factory=list)
    hostname: str = ""
    ip: str = ""
    port: int = 22

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

def load_config(config_path:str) -> Config:
    """
    Load the config from the config file using configparser.
    Args:
        - config_path: The path to the configuration file.
    Returns:
        Config: A populated Config object containing the loaded config.
    """
    config = configparser.ConfigParser(allow_unnamed_section=True)
    config.read(config_path)

    # Check if sections are provided
    server_section = "Server" if "Server" in config.sections() else UNNAMED_SECTION
    roots_section = "Roots" if "Roots" in config.sections() else UNNAMED_SECTION

    server_config = ServerConfig(
            config.get(server_section, "user"),
            config.get(server_section, "sshargs", fallback=None),
            config.get(server_section, "hostname", fallback=None),
            config.get(server_section, "ip", fallback=None),
            config.getint(server_section, "port", fallback=None)
        )
    roots_config = RootsConfig(
            config.get(roots_section, "local"),
            config.get(roots_section, "remote")
        )
    return Config(server_config, roots_config)
