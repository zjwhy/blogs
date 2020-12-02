from .comworkbook import ComWorkBook

class WpsWorkBook(ComWorkBook):
    def __init__(self, workbook, launch_way, original_file, xlApp):
        super(WpsWorkBook, self).__init__(workbook, launch_way, original_file, xlApp)

    def execute_macro(self, macro):
        raise ValueError("目前不支持WPS运行宏，请使用Microsoft Office Excel")