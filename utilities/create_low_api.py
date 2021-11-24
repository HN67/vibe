"""Read a file denoting raw resource contents and produce an API schema.

Run with something like
`python utilities\\create_low_api.py < database\\raw.txt > database\\generated.txt`
"""

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

    logger.info(resource)
    logger.info(resource[0].split(" "))
    name, api_type = resource[0].split(" ")
    attrs = [p.split(" ") for p in resource[1]]

    logger.info(attrs)
    logger.info(resource)

    key = attrs[0]
    key_name, key_type = key
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
Output: [{key_type}]

    Description: Get information on a {name}
    URL: /api/{name}s/<{key_name}: {key_type}>
    Method: GET
    Input: None
    Output: {{{output_list}}}

    Description: Create / update a {name}
    URL: /api/{name}s/<{key_name}: {key_type}>
    Method: PUT
    Input: {{{input_list}}}
    Output: {{{output_list}}}

    Description: Delete a {name}
    URL: /api/{name}s/<{key_name}: {key_type}>
    Method: DELETE
    Input: None
    Output: {{{output_list}}}
"""
    if api_type == "qualia":
        foreign_name = "mood"
        foreign_type = "string"
        extra = f"""
Description: Query connections of a {name}
URL: /api/{name}s_connections
Method: GET
Input: {{"{name}": Optional[{key_type}], "{foreign_name}": Optional[{foreign_type}]}}
Output: [{{"{name}": {key_type}, "{foreign_name}": {foreign_type}}}]

    Description: Create a connection with a {name}
    URL: /api/{name}s_connections
    Method: POST
    Input: {{"{name}": {key_type}, "{foreign_name}": {foreign_type}}}
    Output: {{"{name}": {key_type}, "{foreign_name}": {foreign_type}}}

    Description: Delete a connection with a {name}
    URL: /api/{name}s_connections
    Method: DELETE
    Input: {{"{name}": {key_type}, "{foreign_name}": {foreign_type}}}
    Output: {{"{name}": {key_type}, "{foreign_name}": {foreign_type}}}
"""
        # dont strip leading newline
        text += extra
    print(text[1:], file=output)


def main() -> None:
    """Main function."""
    resources = list(read_raw(sys.stdin))
    logger.info(resources)
    for resource in resources:
        print_schema(sys.stdout, resource)


if __name__ == "__main__":
    main()
