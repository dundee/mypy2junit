import fileinput
import re
import sys
from typing import List, Tuple

__version__ = '1.6.0'

RESULT_REGEX = re.compile(
    # errors -> error if found only one error
    r'Found (?P<count>\d+) errors?'
)
REPLACES = {
    ord('<'): '&lt;',
    ord('"'): '&quot;',
}


def process_lines(lines: List[str]) -> Tuple[str, bool]:
    result = {'count': '0', 'total_files': '0'}
    failures = []
    output = ''

    for line in lines:
        if line.startswith('Found '):
            match = re.match(
                RESULT_REGEX,
                line
            )
            if match:
                result = match.groupdict()
            continue

        # example: Success: no issues found in 9 source files
        if line.startswith('Success: no issues found in '):
            break

        file_, line, type_, *message = line.split(':')
        type_ = type_.strip()

        if type_ == 'error':
            failures.append((file_, line, type_, message))

    output += f"""<?xml version="1.0" encoding="utf-8"?>
<testsuite errors="0" failures="{result['count']}" name="" skips="0" tests="{result['count']}" time="0.0">"""

    for failure in failures:
        msg = f"{failure[0]}:{failure[1]}: {failure[2]}: "
        msg += ':'.join(failure[3]).strip().translate(REPLACES)
        output += f"""
    <testcase classname="{failure[0]}" name="{failure[0]}:{failure[1]}" time="0.0">
        <failure message="Mypy error on {failure[0]}:{failure[1]}" type="WARNING">{msg}</failure>
    </testcase>"""

    output += """
</testsuite>"""

    return output, int(result['count']) == 0


def main():
    output, status = process_lines(
        list(fileinput.input())
    )
    print(
        output
    )
    if not status:
        sys.exit(1)


if __name__ == "__main__":
    main()
