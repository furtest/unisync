# Copyright (C) 2025 Paul Retourné
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from argparser import create_argparser
from config import RootsConfig, ServerConfig, Config, load_config
from synchroniser import Synchroniser

def main():
    parser = create_argparser()
    base_namespace = parser.parse_args()

    config_path = os.path.expanduser("~/.config/unisync/config.ini")
    if base_namespace.config != None and os.path.isfile(base_namespace.config):
        config = load_config(base_namespace.config)
    elif os.path.isfile(config_path):
        config = load_config(config_path)
    else:
        # TODO make the command line arguments work and override the config options
        pass

    synchroniser = Synchroniser(
            config.roots.remote,
            config.roots.local,
            config.server.user,
            config.server.ip if config.server.ip != "" else config.server.hostname,
            config.server.port,
            config.unison.bools,
            config.unison.values
    )

    if synchroniser.create_ssh_master_connection() != 0:
        print("Connection failed quitting")
        return 1
    print("Connected to the remote.")

    synchroniser.sync_files(["salut"])

    synchroniser.close_ssh_master_connection()



if __name__ == "__main__":
    main()
