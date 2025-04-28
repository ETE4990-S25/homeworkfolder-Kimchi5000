import re

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