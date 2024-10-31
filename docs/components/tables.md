# Using Tables from RapidHTML

The `Table` class in the `rapidhtml.components.table` module allows you to easily create HTML tables with dynamic data. Here's how you can use it:

1. Import the `Table` class from the `rapidhtml.components.table` module:

   ```python
   from rapidhtml.components import Table
   ```

2. Create an instance of the `Table` class:

   ```python
   table = Table()
   ```

3. Set the columns of the table using the `columns` property:

   ```python
   table.columns = ["Column 1", "Column 2", "Column 3"]
   ```

4. Add rows to the table using the `add_row` or `add_rows` methods:

   ```python
   table.add_row(["Value 1", "Value 2", "Value 3"])
   table.add_rows(["Value 4", "Value 5", "Value 6"], ["Value 7", "Value 8", "Value 9"])
   ```

5. Render the table to HTML using the `render` method:

   ```python
   html = table.render()
   ```

   The `render` method returns a string containing the HTML representation of the table.

You can customize the appearance of the table by adding CSS classes or inline styles to the table and its elements.