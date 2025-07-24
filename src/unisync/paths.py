# Copyright (C) 2025 Paul Retourné
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess

def user_select_files(local_dir:str, choice_timeout:int=120) -> list[str]:
    """
    Make the user select files in the top directory.
    Currently uses nnn for the selection,
    the goal is to replace it in order to avoid using external programs.
    Returns the list of paths selected.
    """
    command = [
            "/usr/bin/nnn",
            "-H",
            "-p", "-",
            local_dir
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
        next_path = next_path[len(local_dir):].lstrip("/")
        paths_list.append(next_path)

    return paths_list



