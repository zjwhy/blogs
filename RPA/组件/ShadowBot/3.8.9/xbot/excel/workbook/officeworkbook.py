from .comworkbook import ComWorkBook

class OfficeWorkBook(ComWorkBook):
    def __init__(self, workbook, launch_way, original_file, xlApp):
        super(OfficeWorkBook, self).__init__(workbook, launch_way, original_file, xlApp)

    def execute_macro(self, macro):
        self.xlApp.Application.Run(macro)