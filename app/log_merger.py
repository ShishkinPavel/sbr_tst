import json
from datetime import datetime


# Define a function to read a chunk of lines from a file
def read_lines(file):
    while True:
        lines = file.readlines(100)
        if not lines:
            break
        for line in lines:
            yield line


def write_from_file(file, current_datetime, f_out):
    for line in read_lines(file):
        log = json.loads(line)
        if (
            current_datetime is None
            or datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
            < current_datetime
        ):
            current_line = line
            current_datetime = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
            f_out.write(current_line)


def merge_files(first: str, second: str, target: str):
    # Open both files in read mode
    with open(first, "r", encoding="utf-8") as f1, open(
        second, "r", encoding="utf-8"
    ) as f2, open(target, "w", encoding="utf-8") as f_out:

        # Define variables for tracking the current line and datetime
        current_datetime = None

        # Iterate through both files simultaneously
        for line1, line2 in zip(read_lines(f1), read_lines(f2)):
            # Convert each line to a dictionary
            log1 = json.loads(line1)
            log2 = json.loads(line2)

            # Determine which log has the earliest datetime
            if current_datetime is None or datetime.strptime(
                log1["timestamp"], "%Y-%m-%d %H:%M:%S"
            ) < datetime.strptime(log2["timestamp"], "%Y-%m-%d %H:%M:%S"):
                current_line = line1
                current_datetime = datetime.strptime(
                    log1["timestamp"], "%Y-%m-%d %H:%M:%S"
                )
            else:
                current_line = line2
                current_datetime = datetime.strptime(
                    log2["timestamp"], "%Y-%m-%d %H:%M:%S"
                )

            # Write the current line to the output file
            f_out.write(current_line)

        # Handle any remaining lines in the both files
        write_from_file(f1, current_datetime, f_out)
        write_from_file(f2, current_datetime, f_out)
