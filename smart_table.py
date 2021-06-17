from dearpygui.core import *
from dearpygui.simple import *
import app

class SmartTable:
    # This is the smart table that will fill widgets for cells based on type
    def __init__(self, name: str, header: List[str] = None):
        self.name = name
        self.header = header
        self.row = 0
        self.column = 0

        if header is not None:
            self.add_header(self.header)

    def add_header(self, header: List[str]):
        with managed_columns(f"{self.name}_head", len(header)):
            for item in header:
                add_text(item)
            
        with managed_columns(f"{self.name}_body", len(header)):
            pass

    def add_row(self, row_content: List[Any]):
        with managed_columns(f"{self.name}_{self.row}", len(row_content)+1, before=f"{self.name}_body"):
            for item in row_content:
                if type(item) is str:
                    add_input_text(f"##{self.name}_{self.row}_{self.column}", default_value=item, width=-1,)
                if type(item) is int:
                    add_input_int(f"##{self.name}_{self.row}_{self.column}", default_value=item, width=-1, step=0)
                if type(item) is float:
                    add_input_float(f"##{self.name}_{self.row}_{self.column}", default_value=item, width=-1, step=0)
                self.column += 1
            add_button(f"Edit##{self.name}_{self.row}_{self.column}", width=-1, callback_data=self.row, callback=lambda sender, data:app.edit_button_callback(data))
        self.column = 0
        self.row += 1
        