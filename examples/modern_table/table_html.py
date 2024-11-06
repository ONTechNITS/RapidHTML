import os
import json
from pathlib import Path

from pydantic import BaseModel

from rapidhtml.components import Table as ComponenetTable

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


def generate_html(*people: Person) -> ComponenetTable:
    table = ComponenetTable(class_="styled-table")

    table.columns = ["Name", "Age", "City", "Profession"]
    
    for person in people:
        table.add_row([person.name, str(person.age), person.city, person.profession])

    return table
