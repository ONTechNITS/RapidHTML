from typing import Callable, Mapping

from rapidhtml import tags as html_tags
from rapidhtml.callbacks import RapidHTMLCallback


class Table(html_tags.BaseTag):
    def __init__(self, callback: Callable | RapidHTMLCallback = None, **attrs) -> None:
        super().__init__("table", callback=callback, **attrs)

        self.__columns: list[str] = []
        self.__data: list[Mapping[str, int | float | str]] = []

    @property
    def columns(self) -> list[str]:
        return self.__columns

    @property
    def rows(self) -> list[Mapping[str, int | float | str]]:
        return self.__data

    @columns.setter
    def columns(self, columns: list[str]) -> None:
        if self.__data:
            raise ValueError(
                "Cannot set columns after data has been added. Call clear_rows() first."
            )
        self.__columns = columns

    def add_row(self, row: list[str]) -> None:
        padding = [""] * (len(self.__columns) - len(row))
        padded_row = row + padding

        current_row_data = {
            column_name: row_data
            for column_name, row_data in zip(self.__columns, padded_row)
        }
        self.__data.append(current_row_data)

    def add_rows(self, *rows: list[str]) -> None:
        for row in rows:
            self.add_row(row)

    def clear_rows(self) -> None:
        self.__data = []

    def render(self) -> str:
        thead = html_tags.Thead()
        tbody = html_tags.Tbody()

        header_row = html_tags.Tr()
        for column in self.columns:
            header_row.add_tag(html_tags.Th(column))

        thead.add_tag(header_row)

        for row in self.__data:
            current_row = html_tags.Tr()
            for column in self.__columns:
                current_row.add_tag(html_tags.Td(row.get(column, "")))
            tbody.add_tag(current_row)

        self.tags = [thead, tbody]

        return super().render()
