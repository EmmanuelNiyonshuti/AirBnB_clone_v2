#!/usr/bin/python3
"""
This script provides functionality to clean old web_static archives.
"""
from fabric.api import env, local, run, cd
import os

env.hosts = ['ubuntu@34.232.68.210', 'ubuntu@52.91.150.38']


def do_clean(number=0):
    """
    Deletes out-of-date archives, keeping only the most recent versions.

    :param number: The number of archives to keep
    (default is 0, which keeps only the most recent one).
    """
    number = int(number)
    if number < 1:
        number = 1

    """Clean local archives"""
    local_archives = sorted(os.listdir('versions'))
    archives_to_delete_local = local_archives[:-number]

    for archive in archives_to_delete_local:
        local("rm versions/{}".format(archive))

    """Clean remote archives"""
    with cd("/data/web_static/releases"):
        remote_archives = run('ls -tr').split()
        remote_archives = [a for a in remote_archives if 'web_static_' in a]
        archives_to_delete_remote = remote_archives[:-number]

        for archive in archives_to_delete_remote:
            run("sudo rm -rf /data/web_static/releases/{}".format(archive))
