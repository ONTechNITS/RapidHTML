from typing import Mapping

from rapidhtml import tags as html_tags
from rapidhtml.bases import Renderable


class Table(Renderable):
    def __init__(self) -> None:
        self.__columns: list[str] = []
        self.__data: list[Mapping[str, int | float | str]] = []

    @property
    def columns(self) -> list[str]:
        return self.__columns

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
        # table_headers = html_tags.Thead(
        #     html_tags.Tr(*[
        #         html_tags.Th(column_name) for column_name in self.__columns
        #     ])
        # )

        # for row in self.__data:

        # table_rows = [
        #     Tr(
        #         Td(row.get(column_name, ""))
        #     )
        # ]

        table = html_tags.Table()
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
        
        table.add_tag(thead, tbody)

        return table.render()
