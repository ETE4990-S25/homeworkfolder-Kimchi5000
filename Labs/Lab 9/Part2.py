import re
import json


def read_the_log_file(filename):
    log_lines = [] 
    try:
        with open(filename, 'r') as file: 
            log_lines = file.readlines()  # Read all lines into the list
        print("file read successfully")
    except FileNotFoundError:
        print("file not found")

    return log_lines


def parse_log_lines(log_lines):
    # Define the regex pattern to match log entries
    regex_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (\w+) - (.*)'

    parsed_logs = [] 
    for line in log_lines:
        match = re.match(regex_pattern, line.strip())  # Match the line against the regex pattern
        if match:
            log_entry = {
                'timestamp': match.group(1),
                'log_name': match.group(2),
                'log_level': match.group(3),
                'message': match.group(4)
            }
            parsed_logs.append(log_entry)  # Add the parsed entry to the list
        else:
            print("Log entry does not match the expected format:", line)

    return parsed_logs


def count_log_levels(parsed_logs):
    log_level_count = {}

    for log in parsed_logs:
        level = log['log_level']
        message = log['message']

        if level not in log_level_count:
            log_level_count[level] = {}

        if message not in log_level_count[level]:
            log_level_count[level][message] = 0

        log_level_count[level][message] += 1

    return log_level_count

def save_to_json(log_counts, filename='log_counts.json'):
    with open(filename, 'w') as json_file:
        json.dump(log_counts, json_file, indent=4)

if __name__ == "__main__":
    log_file_name = 'example_log.log' 
    parsed_log_entries = read_the_log_file(log_file_name)  

    log_counts = count_log_levels(parsed_log_entries)

    save_to_json(log_counts)