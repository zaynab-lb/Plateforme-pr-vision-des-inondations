import os
import socket
import py_eureka_client.eureka_client as eureka_client

from app.config import Config


async def register_with_eureka():
    hostname = os.getenv("EUREKA_INSTANCE_HOSTNAME", socket.gethostname())

    await eureka_client.init_async(
        eureka_server=Config.EUREKA_SERVER,
        app_name=Config.APP_NAME,
        instance_port=Config.APP_PORT,
        instance_host=hostname,
        instance_ip=hostname
    )