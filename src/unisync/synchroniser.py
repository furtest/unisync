# Copyright (C) 2025 Paul Retourné
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
import os
import sys
import time
import logging

logger = logging.getLogger(__name__)

class Synchroniser:

    def __init__(self, remote:str, local:str, user:str, ip:str,
                 port:int=22, args_bool:list=[], args_value:dict={}, ssh_settings:dict={}):
        self.remote_dir:str = remote
        self.local:str = local
        self.args_bool:list[str] = args_bool 
        self.args_value:dict[str, str] = args_value 
        self.ssh_settings:dict[str, str] = dict()
        self.remote_user:str = user
        self.remote_ip:str = ip 
        self.remote_port:int = port
    
    def create_ssh_master_connection(self, control_path:str="~/.ssh/control_%C", connection_timeout:int=60) -> int:
        """
        Creates an ssh master connection so the user only has to authenticate once to the remote server.
        The subsequent connections will be made through this master connection which speeds up connecting.
        @control_path: Set the location of the ssh control socket
        @connection_timeout:
            Time given to the user to authenticate to the remote server.
            On slow connections one might want to increase this.
        Returns 0 on success.
        """
        self.control_path = os.path.expanduser(control_path)
        command = [
                "/usr/bin/ssh",
                "-fNT",
                "-M",
                "-S", self.control_path,
                f"{self.remote_user}@{self.remote_ip}",
                "-p", str(self.remote_port)
                ]
        master_ssh = subprocess.Popen(command)
        try:
            ret_code = master_ssh.wait(timeout=connection_timeout)
        except subprocess.TimeoutExpired:
            print("Time to login expired", file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            return 2

        if ret_code != 0:
            print("Login to remote failed", file=sys.stderr)
            return ret_code
        return 0


    def close_ssh_master_connection(self) -> int:
        """
        Close the ssh master connection.
        """
        command = [
                "/usr/bin/ssh",
                "-S", self.control_path,
                "-O", "exit",
                f"{self.remote_user}@{self.remote_ip}",
                "-p", str(self.remote_port)
                ]
        close = subprocess.Popen(command)
        return close.wait()

    def sync_files(self, paths:list, force:bool=False) -> int:
        """
        Synchronises the files.
        """
        return self.sync(
                f"ssh://{self.remote_user}@{self.remote_ip}/{self.remote_dir}/.data",
                self.local,
                paths=paths,
                force=force
                )

    def sync_links(self, ignore:list) -> int:
        """
        Synchronises the links, they must exist already.
        """
        return self.sync(
                f"ssh://{self.remote_user}@{self.remote_ip}/{self.remote_dir}/links",
                self.local,
                ignore=ignore
                )

    def sync(self, remote_root:str, local_root:str,
             paths:list=[], ignore:list=[], force:bool=False) -> int:
        """
        Perform the synchronisation by calling unison.
        @remote_root: The remote root, must be a full root usable by unison.
        @local_root: The local root, must be a full root usable by unison.
        @paths: List of paths to synchronise
        @ignore: List of paths to ignore
            The paths and everything under them will be ignored.
            If you need to ignore some specific files use the arguments.
        @force: Force all changes from remote to local.
            Used mostly when replacing a link by the file.
        Returns: the unison return code see section 6.11 of the documentation
        """
        command = [ "/usr/bin/unison", "-root", remote_root, "-root", local_root ]
        for arg in self.args_bool:
            command.append(f"-{arg}")
        for arg, value in self.args_value.items():
            command.append(f"-{arg}")
            command.append(value)

        sshargs = f"-p {self.remote_port} "
        for arg, value in self.ssh_settings.items():
            sshargs += arg + " " + value + " "
        command.append("-sshargs")
        command.append(sshargs)

        for path in paths:
            command.append("-path")
            command.append(path)

        for path in ignore:
            command.append("-ignore")
            command.append(f"BelowPath {path}")

        if force:
            command.append("-force")
            command.append(remote_root)
            command.append("-batch")

        print(command)
        proc = subprocess.Popen(command)
        ret_code = proc.wait()
        return ret_code

if __name__ == "__main__":
    sync = Synchroniser("/home/furtest/a", "/home/furtest/files/programmation/unisync/a", "furtest", "194.164.198.44", port=8443, args_bool=["auto"])
    print("Creating master connection")
    sync.create_ssh_master_connection()
    print("Connected")

    sync.sync_files(["salut", "a"])
    sync.sync_links(["salut", "a"])

    print("Closing master connection")
    sync.close_ssh_master_connection()
    print("Connection closed")

# roots: remote_files, remote_links, local
# arguments for unison
# force
    
