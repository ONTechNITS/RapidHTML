import os
import json
from pathlib import Path

from pydantic import BaseModel

from rapidhtml.tags import Table, Thead, Tr, Th, Tbody, Td

WORKING_DIR = Path(os.path.dirname(os.path.realpath(__file__)))


class Person(BaseModel):
    name: str
    age: int
    city: str
    profession: str


def load_database() -> list[Person]:
    db_loc = WORKING_DIR / "data.json"

    with db_loc.open() as fh:
        data = json.load(fh)

    return [Person.model_validate(person) for person in data]


def generate_html(*people: Person) -> Table:
    table_header = Thead(
        Tr(
            Th("Name"), Th("Age"), Th("City"), Th("Profession")
        )
    )

    table_rows = [
        Tr(
            Td(person.name), Td(person.age), Td(person.city), Td(person.profession)
        )
        for person in people
    ]
    table_body = Tbody(*table_rows)
    table = Table(table_header, table_body, class_="styled-table")

    return table
