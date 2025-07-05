# Copyright (C) 2025 Paul Retourné
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse

def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
            prog='unisync',
            description='File synchronisation application',
            epilog="""
            Copyright © 2025 Paul Retourné.
            License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>."""
            )
    parser.add_argument("local", nargs="?")
    parser.add_argument("remote", nargs="?")

    remote_addr_group = parser.add_mutually_exclusive_group()
    remote_addr_group.add_argument("--ip")
    remote_addr_group.add_argument("--hostname")

    parser.add_argument("--config", help="Path to the configuration file", metavar="path_to_config")
    return parser
