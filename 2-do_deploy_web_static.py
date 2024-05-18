#!/usr/bin/python3
"""
This module provides functionality to deploy
web_static content to multiple servers using Fabric3.
"""
import os
from datetime import datetime
from fabric.operations import env, put, run

env.hosts = ['ubuntu@34.232.68.210', 'ubuntu@52.91.150.38']


def do_deploy(archive_path):
    """
    Deploy the web_static content to two servers using Fabric3.

    Uploads the .tgz archive compressed by gzip to the servers,
    extracts the files from the archive, and adds them
    into a new directory for serving.

    :param archive_path: The path to the .tgz archive to be deployed.
    """
    if os.path.isfile(archive_path):
        curr_time = datetime.now().strftime("%Y%m%d%H%M%S")
        new_dir = "web_static_{}".format(curr_time)
        put(archive_path, '/tmp/')
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(new_dir))
        run(('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
                .format(os.path.basename(archive_path), new_dir)))
        run('sudo rm /tmp/{}'.format(os.path.basename(archive_path)))
        run(('sudo mv /data/web_static/releases/{}/web_static/* '
                '/data/web_static/releases/{}/'.format(new_dir, new_dir)))
        run('sudo rm -rf /data/web_static/releases/{}/web_static/'
            .format(new_dir))
        run('sudo rm -rf /data/web_static/current')
        run(('sudo ln -s /data/web_static/releases/{}/ '
                '/data/web_static/current').format(new_dir))