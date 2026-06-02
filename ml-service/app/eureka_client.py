from py_eureka_client import eureka_client
from app.config import Config


async def register_with_eureka():
    await eureka_client.init_async(
        eureka_server=Config.EUREKA_SERVER,
        app_name=Config.APP_NAME,
        instance_port=Config.APP_PORT,
        instance_host="host.docker.internal"
    )