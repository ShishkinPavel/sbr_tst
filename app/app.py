import argparse

from log_merger import merge_files


def main():
    # Define the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file1", help="path to first log file")
    parser.add_argument("log_file2", help="path to second log file")
    parser.add_argument(
        "-o", "--output_file", help="path to output merged log file", required=True
    )
    args = parser.parse_args()

    # Merge the logs and write the result to the output file
    merge_files(args.log_file1, args.log_file2, args.output_file)


if __name__ == "__main__":
    main()
