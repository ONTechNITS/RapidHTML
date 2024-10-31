import os
import json
from pathlib import Path

from pydantic import BaseModel

from rapidhtml.components import Table

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
    table = Table()

    table.columns = ["Name", "Age", "City", "Profession"]
    table.add_rows(*people)

    return table
