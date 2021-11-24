"""Read a file denoting raw resource contents and produce an API schema."""

import itertools
import logging
import sys
import typing as t

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def read_raw(file: t.TextIO) -> t.Iterable[t.Tuple[str, t.Sequence[str]]]:
    """Parse the raw file."""
    for key, group in itertools.groupby(
        [l.strip() for l in file], lambda line: line != ""
    ):
        if key:
            lines = list(group)
            yield (lines[0], lines[1:])


def print_schema(output: t.TextIO, resource: t.Tuple[str, t.Sequence[str]]) -> None:
    """Print a schema for the resource."""

    name = resource[0]
    attrs = [p.split(" ") for p in resource[1]]

    logger.info(attrs)
    logger.info(resource)

    key = attrs[0]
    others = attrs[1:]

    output_list = (
        "\n        " + "\n        ".join(f'"{k}": {v},' for (k, v) in attrs) + "\n    "
    )
    input_list = (
        (
            "\n        "
            + "\n        ".join(f'"{k}": {v},' for (k, v) in others)
            + "\n    "
        )
        if others
        else ""
    )

    text = f"""
Description: Get list of {name}s
URL: /api/{name}s/
Method: GET
Input: None
Output: [string]

    Description: Get information on a {name}
    URL: /api/{name}s/<{key[0]}: string>
    Method: GET
    Input: None
    Output: {{{output_list}}}

    Description: Create / update a {name}
    URL: /api/{name}s/<{key[0]}: string>
    Method: PUT
    Input: {{{input_list}}}
    Output: {{{output_list}}}

    Description: Delete a {name}
    URL: /api/{name}s/<{key[0]}: string>
    Method: DELETE
    Input: None
    Output: {{{output_list}}}
"""
    print(text[1:], file=output)


def main() -> None:
    """Main function."""
    resources = list(read_raw(sys.stdin))
    logger.info(resources)
    for resource in resources:
        print_schema(sys.stdout, resource)


if __name__ == "__main__":
    main()
