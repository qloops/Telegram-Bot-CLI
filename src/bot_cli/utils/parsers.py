import re
from typing import List


def parse_target_ids(raw_input: str, reverse: bool = False) -> List[int]:
    targets = []
    tokens = [token.strip() for token in raw_input.split(",") if token.strip()]

    for token in tokens:
        range_match = re.match(r"^(\d+)\s*-\s*(\d+)$", token)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            start_val, end_val = sorted((start, end))
            targets.extend(range(start_val, end_val + 1))
        else:
            try:
                targets.append(int(token))
            except ValueError:
                print(f"Skipped invalid ID: {token}")

    return sorted(set(targets), reverse=reverse)