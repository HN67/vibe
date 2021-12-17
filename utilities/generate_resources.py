"""Read a file denoting raw resource contents and produce an API schema.

Run with something like
`python utilities\\generate_resources.py < database\\raw.txt > database\\generated.txt`
"""

import dataclasses
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


@dataclasses.dataclass(frozen=True)
class Var:
    """A typed name."""

    name: str
    type: str


@dataclasses.dataclass(frozen=True)
class Resource:
    """A described resource."""

    name: str
    mark: str
    attrs: t.Sequence[Var]

    @property
    def others(self) -> t.Sequence[Var]:
        """Everything except first attr."""
        return self.attrs[1:]

    @property
    def key(self) -> Var:
        """First attr."""
        return self.attrs[0]

    @classmethod
    def from_tuple(cls, resource: t.Tuple[str, t.Sequence[str]]) -> "Resource":
        """Construct a Resource from raw form."""
        name, mark = resource[0].split(" ", maxsplit=1)
        attrs = [p.split(" ", maxsplit=1) for p in resource[1]]
        return cls(name, mark, [Var(*attr) for attr in attrs])


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
    Output: {{{key_name}: {key_type}}}

    Description: Delete a {name}
    URL: /api/{name}s/<{key_name}: {key_type}>
    Method: DELETE
    Input: None
    Output: {{{key_name}: {key_type}}}
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


def print_procedures(output: t.TextIO, resource: Resource) -> None:
    """Print CRUD stored procedures for a resource."""

    parameter_list = ", ".join(f"IN {attr.name} {attr.type}" for attr in resource.attrs)
    selection_list = ", ".join(f"{attr.name}" for attr in resource.attrs)
    update_string = (
        "    ON DUPLICATE KEY UPDATE\n            "
        + ", ".join(
            f"{resource.name}.{attr.name} = {attr.name}" for attr in resource.attrs
        )
        + "\n        "
    )

    text = f"""
CREATE OR REPLACE PROCEDURE get_{resource.name.lower()}s()
    READS SQL DATA
    BEGIN
        SELECT {resource.key.name}
        FROM {resource.name}
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_{resource.name.lower()}(IN {resource.key.name} {resource.key.type})
    READS SQL DATA
    BEGIN
        SELECT {selection_list}
        FROM {resource.name}
        WHERE {resource.name}.{resource.key.name} = {resource.key.name}
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_{resource.name.lower()}({parameter_list})
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO {resource.name} ({selection_list})
        VALUES ({selection_list})
        {update_string};
    END;
//

CREATE OR REPLACE PROCEDURE delete_{resource.name.lower()}(IN {resource.key.name} {resource.key.type})
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM {resource.name}
        WHERE {resource.name}.{resource.key.name} = {resource.key.name}
        ;
    END;
//    
"""
    if resource.mark.startswith("qualia"):
        name = resource.mark.split(",", maxsplit=1)[1]
        table = f"{name}Affects"
        this = Var(name=name.lower(), type="NVARCHAR(255)")
        other = Var(name="mood", type="NVARCHAR(255)")

        parameters = ", ".join(f"IN {attr.name} {attr.type}" for attr in [this, other])
        selections = ", ".join(f"{attr.name}" for attr in [this, other])
        update_portion = ", ".join(
            f"{table}.{attr.name} = {attr.name}" for attr in [this, other]
        )
        delete_portion = " AND ".join(
            f"{table}.{attr.name} = {attr.name}" for attr in [this, other]
        )

        extra = f"""
CREATE OR REPLACE PROCEDURE put_{this.name}affects({parameters})
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO {table} ({selections})
        VALUES ({selections})
        ON DUPLICATE KEY UPDATE
            {update_portion}
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_{this.name}affects({parameters})
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM {table}
        WHERE {delete_portion}
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_{this.name}affects_{other.name}(IN {other.name} {other.type})
    READS SQL DATA
    BEGIN
        SELECT {selections}
        FROM {table}
        WHERE {table}.{other.name} = {other.name}
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_{this.name}affects_{this.name}(IN {this.name} {this.type})
    READS SQL DATA
    BEGIN
        SELECT {selections}
        FROM {table}
        WHERE {table}.{this.name} = {this.name}
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_{this.name}affects_{this.name}_{other.name}({parameters})
    READS SQL DATA
    BEGIN
        SELECT {selections}
        FROM {table}
        WHERE {delete_portion}
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_{this.name}affects()
    READS SQL DATA
    BEGIN
        SELECT {selections}
        FROM {table}
        ;
    END;
//
"""
        # dont strip leading newline
        text += extra
    print(text[1:], file=output)


def main() -> None:
    """Main function."""

    MODE = "procedures"

    if MODE == "api":
        raw_resources = list(read_raw(sys.stdin))
        logger.info(raw_resources)
        for raw_resource in raw_resources:
            print_schema(sys.stdout, raw_resource)
    elif MODE == "procedures":
        resources = [Resource.from_tuple(raw) for raw in read_raw(sys.stdin)]
        logger.info(resources)
        for resource in resources:
            print_procedures(sys.stdout, resource)


if __name__ == "__main__":
    main()
