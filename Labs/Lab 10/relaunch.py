import docker
import time

client = docker.from_env()
containers = ["adminer", "mysql"]

def relaunch():
    while True:
        for container_name in containers:
            container = client.containers.get(container_name)

            if container.status != "running":
                print(f"relaunching {container_name}")
                container.start()
