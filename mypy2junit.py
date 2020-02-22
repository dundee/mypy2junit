import fileinput
import re
import sys
from typing import List

__version__ = '1.2.0'

RESULT_REGEX = re.compile(
    r'Found (?P<count>\d+) errors'
)
REPLACES = {
    ord('<'): '&lt;',
    ord('"'): '&quot;',
}


def process_lines(lines: List[str]) -> str:
    result = {'count': 0, 'total_files': 0}
    failures = []
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
            failures.append((file_, line, type_, msg))

    output += f"""<?xml version="1.0" encoding="utf-8"?>
<testsuite errors="0" failures="{result['count']}" name="" skips="0" tests="{result['count']}" time="0.0">"""

    for failure in failures:
        msg = f"{failure[0]}:{failure[1]}: {failure[2]}: "
        msg += ':'.join(failure[3]).strip().translate(REPLACES)
        output += f"""
    <testcase name="{failure[0]}:{failure[1]}" time="0.0">
        <failure message="Mypy error on {failure[0]}:{failure[1]}" type="WARNING">{msg}</failure>
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


if __name__ == "__main__":
    main()
