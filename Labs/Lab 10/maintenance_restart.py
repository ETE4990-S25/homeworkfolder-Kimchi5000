container_start_time = {container: time.time() for container in containers}

def maintenance_restart():
    while True:
        for container_name in containers:
            container = client.containers.get(container_name)
            current_time = time.time()

            if current_time - container_start_time[container_name] >= 86400:
                print(f"Performing maintenance restart for {container_name}")
                container.restart()
                container_start_time[container_name] = current_time #Update the start time so maintenance restart occurs every 24hrs

