#!/usr/bin/python3
"""
deploy web_static to two nginx web servers.
"""
import os
from datetime import datetime
from fabric.operations import env, put, run

env.hosts = ['ubuntu@web01:80', 'ubuntu@web02:80']

def do_deploy(archive_path):
    """upload the archive to the servers , decompress the archive and serve them.
    """
    if os.path.isfile(archive_path):

        put(archive_path, '/tmp/')

        curr_time = datetime.now().strftime("%Y%m%d%H%M%S")
        decompressed_dir = "web_static_{}".format(curr_time)

        run('sudo mkdir /data/web_static/releases/{}/'.format(decompressed_dir))

        run('sudo tar -xvf /tmp/{} -C /data/web_static/releases/{}/'.format(os.path.basename(archive_path), decompressed_dir))
        run('sudo rm /tmp/{}'.format(os.path.basename(archive_path)))
        run('sudo rm /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/{} /data/web_static/current'.format(decompressed_dir))
