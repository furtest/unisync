# Copyright (C) 2025 Paul Retourné
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess

from pathlib import Path, PosixPath

class PathsManager:

    def __init__(self, local_dir:PosixPath, cache_dir:PosixPath):
        """
        Creates a PathsManager with the necessary data
        Args:
            local_dir: Path to the top directory of the synchronisation
            cache_dir: Path to the cache directory that contains the paths file
        """
        if not local_dir.is_dir():
            raise ValueError("Invalid local directory")
        self.local_dir = local_dir

        if not cache_dir.is_dir():
            raise ValueError("Invalid cache directory")
        self.cache_dir = cache_dir

        self.paths_file:PosixPath = self.cache_dir / "paths"
        if not self.paths_file.is_file():
            raise ValueError("The paths file does not exist")


    def user_select_files(self, choice_timeout:int=120) -> list[str]:
        """
        Make the user select files in the top directory.
        Currently uses nnn for the selection.
        The goal is to replace it in order to avoid using external programs.
        Args:
            choice_timeout: Time given to make choices in nnn
        Returns:
            list[str]: The list of paths that was selected
        """
        command = [
                "/usr/bin/nnn",
                "-H",
                "-p", "-",
                self.local_dir
                ]
        nnn_process = subprocess.Popen(command, stdout=subprocess.PIPE)
        try:
            ret_code = nnn_process.wait(timeout=choice_timeout)
        except subprocess.TimeoutExpired as e:
            print("Choice timeout expired", file=sys.stderr)
            raise e

        if ret_code != 0:
            print("File selection failed", file=sys.stderr)
            raise subprocess.CalledProcessError("File selection failed")

        paths_list:list[str] = []
        while (next_path := nnn_process.stdout.readline()) != b'':
            next_path = next_path.decode().strip()
            # Make the path relative to the top directory
            next_path = next_path[len(self.local_dir):].lstrip("/")
            paths_list.append(next_path)
        return paths_list

    def get_paths_to_sync(self) -> list[str]:
        """
        Return the paths to synchronise as list.
        """
        paths:list[str] = self.paths_file.read_text().split("\n")
        if paths[-1] == "":
            paths.pop()
        return paths


