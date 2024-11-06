import pytest

from rapidhtml.components.table import Table


def test_table_columns():
    table = Table()
    assert table.columns == []

    table.columns = ["Name", "Age", "City"]
    assert table.columns == ["Name", "Age", "City"]

    table.add_row(["John", "25", "New York"])

    # You cannot change the columns while row data exists
    with pytest.raises(ValueError):
        table.columns = ["Name", "Age", "City", "Country"]

    table.clear_rows()

    # Now it should work again
    table.columns = ["Name", "Age", "City", "Country"]
    assert table.columns == ["Name", "Age", "City", "Country"]


def test_table_add_row():
    table = Table()
    table.columns = ["Name", "Age", "City"]

    table.add_row(["John", "25", "New York"])
    assert table.rows == [{"Name": "John", "Age": "25", "City": "New York"}]

    table.add_row(["Alice", "30", "London"])
    assert table.rows == [
        {"Name": "John", "Age": "25", "City": "New York"},
        {"Name": "Alice", "Age": "30", "City": "London"},
    ]


def test_table_add_rows():
    table = Table()
    table.columns = ["Name", "Age", "City"]

    table.add_rows(["John", "25", "New York"], ["Alice", "30", "London"])
    assert table.rows == [
        {"Name": "John", "Age": "25", "City": "New York"},
        {"Name": "Alice", "Age": "30", "City": "London"},
    ]


def test_table_clear_rows():
    table = Table()
    table.columns = ["Name", "Age", "City"]
    table.add_row(["John", "25", "New York"])

    table.clear_rows()
    assert table.rows == []


def test_table_render():
    table = Table()
    table.columns = ["Name", "Age", "City"]
    table.add_row(["John", "25", "New York"])
    table.add_row(["Alice", "30", "London"])

    expected_output = (
        "<table>"
        "<thead>"
        "<tr>"
        "<th>Name</th>"
        "<th>Age</th>"
        "<th>City</th>"
        "</tr>"
        "</thead>"
        "<tbody>"
        "<tr>"
        "<td>John</td>"
        "<td>25</td>"
        "<td>New York</td>"
        "</tr>"
        "<tr>"
        "<td>Alice</td>"
        "<td>30</td>"
        "<td>London</td>"
        "</tr>"
        "</tbody>"
        "</table>"
    )

    assert table.render() == expected_output
