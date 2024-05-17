#!/usr/bin/python3
"""
This script automates the deployment of web_static
content to multiple servers.
It imports two previously defined tasks:
1. 'pack_web_static' - to compress the web_static content
    into a .tgz archive.
2. 'do_deploy_web_static' - to upload and deploy
    the compressed archive to multiple servers.

The 'deploy' function orchestrates these tasks,
ensuring a streamlined deployment process.
"""
pack_web_static = __import__('1-pack_web_static')
do_deploy_web_static = __import__('2-do_deploy_web_static')


def deploy():
    """
    Deploy the compressed web_static content to multiple servers.

    This function first packs the web_static content
    into a compressed archive
    using the 'pack_web_static' task. Then,
    it deploys the compressed archive
    to multiple servers using the 'do_deploy_web_static' task.
    """
    ar_path = pack_web_static.do_pack()
    do_deploy_web_static.do_deploy(ar_path)
