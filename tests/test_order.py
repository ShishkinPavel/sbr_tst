import json
import os
from datetime import datetime

import pytest

from app.log_merger import merge_files


def read_lines(file):
    while True:
        lines = file.readlines(100)
        if not lines:
            break
        for line in lines:
            yield json.loads(line)


def test_sorted_jsonl_file():
    merge_files(
        first="logs/log_a.jsonl",
        second="logs/log_b.jsonl",
        target="logs/merged_logs.jsonl",
    )

    prev_timestamp = None
    with open("logs/merged_logs.jsonl", "r", encoding="utf-8") as f:
        for log in read_lines(f):
            timestamp = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
            if prev_timestamp is not None and timestamp < prev_timestamp:
                pytest.fail("Logs are not sorted in ascending order by timestamp")
            prev_timestamp = timestamp
    os.remove("logs/merged_logs.jsonl")
