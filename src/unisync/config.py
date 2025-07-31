# Copyright (C) 2025 Paul Retourné
# SPDX-License-Identifier: GPL-3.0-or-later

from configparser import UNNAMED_SECTION
from dataclasses import dataclass, field
from pathlib import Path, PosixPath
import ipaddress
import configparser

@dataclass
class ServerConfig:
    """
    Dataclass keeping the config for connecting to the server
    """
    user: str
    sshargs: list[str] | None = field(default_factory=list)
    hostname: str = ""
    ip: str = ""
    port: int = 22

    def __post_init__(self):
        """
        Make sure a remote is provided and the ip address is valid
        """
        if self.ip == "" and self.hostname == "":
            raise ValueError("A remote must be provided (ip or hostname)")

        if self.ip != "":
            try:
                ipaddress.ip_address(self.ip)
            except ValueError:
                raise ValueError("The provided ip address is invalid")

@dataclass
class RootsConfig:
    """
    Dataclass keeping the paths to the roots to synchronise
    """
    local: str
    remote: str

@dataclass
class UnisonConfig:
    """
    Dataclass keeping unison specific configurations
    """
    bools: list = field(default_factory=list)
    values: dict = field(default_factory=dict)

@dataclass
class OtherConfig:
    """
    Dataclass keeping miscellanous configuration options
    """
    cache_dir_path: PosixPath = Path("~/.unisync").expanduser()

@dataclass
class Config:
    """
    Main dataclass for the configurations
    """
    server: ServerConfig
    roots: RootsConfig
    unison: UnisonConfig
    other: OtherConfig = field(default_factory=OtherConfig)


def load_config(config_path:str) -> Config:
    """
    Load the config from the config file using configparser.
    Args:
        - config_path: The path to the configuration file.
    Returns:
        Config: A populated Config object containing the loaded config.
    """
    config = configparser.ConfigParser(allow_unnamed_section=True, allow_no_value=True)
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

    args_bool = list()
    args_val = dict()
    if "Unison" in config.sections():
        for key, val in config.items("Unison"):
            if key in config["DEFAULT"].keys():
                continue
            elif val == "" or val == None:
                args_bool.append(key)
            else:
                args_val[key] = val
    unison_config = UnisonConfig(args_bool, args_val)

    return Config(server_config, roots_config, unison_config)
