import json
import os
import time
import threading
import matplotlib.pyplot as plt

LOG_FILE = "log_counts.json"
WAIT_TIME = 1  # Time between checks

# Function to load the JSON log summary
def load_logs(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Problem reading the log summary:", e)
        return {}

# Keeps track of new messages
previous_criticals = {}

# Main monitoring function
def watch_logs():
    last_updated = 0

    while True:
        if os.path.exists(LOG_FILE):
            current_time = os.path.getmtime(LOG_FILE)
            if current_time != last_updated:
                last_updated = current_time
                logs = load_logs(LOG_FILE)

                print("\nLog Summary")
                for level, msgs in logs.items():
                    total = sum(msgs.values())
                    print(f"{level}: {total} entries")

                    if level == "CRITICAL":
                        for msg, count in msgs.items():
                            old_count = previous_criticals.get(msg, 0)
                            if count > old_count:
                                print(f"NEW CRITICAL: {msg} ({count})")
                                previous_criticals[msg] = count

        time.sleep(WAIT_TIME)

# Main function for plotting
def plot_logs():
    plt.ion()  
    fig, ax = plt.subplots()
    last_updated = 0

    while True:
        if os.path.exists(LOG_FILE):
            current_time = os.path.getmtime(LOG_FILE)
            if current_time != last_updated:
                last_updated = current_time
                logs = load_logs(LOG_FILE)

                # Reset chart
                ax.clear()

                levels = []
                totals = []

                for level, msgs in logs.items():
                    levels.append(level)
                    totals.append(sum(msgs.values()))

                ax.bar(levels, totals, color=['blue', 'orange', 'yellow', 'red'])
                ax.set_title("Log Level Distribution")
                ax.set_ylabel("Count")
                ax.set_xlabel("Log Level")

                plt.draw()
                plt.pause(0.1)

        time.sleep(WAIT_TIME)

# Start threads
if __name__ == "__main__":
    monitor_thread = threading.Thread(target=watch_logs)
    monitor_thread.daemon = True
    monitor_thread.start()

    plot_thread = threading.Thread(target=plot_logs)
    plot_thread.daemon = True
    plot_thread.start()

    print("Monitoring logs and graphing. Press Ctrl+C to stop\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped monitoring and graphing.")