import fileinput
import re
import sys
from typing import List

__version__ = '1.1.0'

RESULT_REGEX = re.compile(
    r'Found (?P<count>\d+) errors'
)
REPLACES = {
    ord('<'): '&lt;',
    ord('"'): '&quot;',
}


def process_lines(lines: List[str]) -> str:
    result = {'count': 0, 'total_files': 0}
    failures = {}
    output = ''

    for line in lines:
        if line.startswith('Found '):
            result = re.match(
                RESULT_REGEX,
                line
            ).groupdict()
            continue

        file_, line, type_, *msg = line.split(':')
        type_ = type_.strip()

        if type_ == 'error':
            failures.setdefault(file_, []).append((line, msg))

    output += f"""<?xml version="1.0" encoding="utf-8"?>
<testsuite errors="0" failures="{result['count']}" name="" skips="0" tests="{result['count']}" time="0.0">"""

    for test_case in failures:
        output += f"""
        <testcase name="{test_case}" time="0.0">"""
        for failure in failures[test_case]:
            msg = f'{test_case}:{failure[0]}: error: '
            msg += ':'.join(failure[1]).strip().translate(REPLACES)
            output += f"""
            <failure message="Mypy error on {test_case}:{failure[0]}" type="WARNING">{msg}</failure>"""
        output += """
    </testcase>"""

    output += """
</testsuite>"""

    return output


def main():
    print(
        process_lines(
            list(fileinput.input())
        )
    )
