from io import TextIOWrapper
from use_cases.InputMatrix import InputMatrix
from use_cases.ParseFileInterface import ParseFileInterface
import openpyxl


class ParseFile(ParseFileInterface):
    default_sheetname = "input sheet"

    def parse_file(self, file: TextIOWrapper) -> InputMatrix:
        # Open xlsx file as workbook, then get the correctly named sheet or the first sheet
        workbook = openpyxl.load_workbook(file, read_only=True, data_only=True)
        worksheet = None
        for ws in workbook.worksheets:
            if (ws.title == self.default_sheetname):
                worksheet = ws
                break
        if (worksheet == None):
            worksheet = workbook.worksheets[0]
        # create input matrix
        inputmatrix = InputMatrix()
        # Get reviewer names
        for cell in worksheet.rows[0]:
            pass

        # Get applicant names
        for cell in worksheet.columns[0]:
            pass

        raise NotImplementedError