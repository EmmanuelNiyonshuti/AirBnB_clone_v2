#!/usr/bin/python3
from datetime import datetime
from fabric.operations import local
import os


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder.
    """
    if not os.path.exists('versions'):
        os.mkdir('versions')
    curr_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(curr_time)
    try:
        local('tar -cvzf {} ./web_static'.format(archive_name))
        return archive_name
    except Exception:
        return None
