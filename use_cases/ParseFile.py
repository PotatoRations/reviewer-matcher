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

        raw_data = list(worksheet.rows)

        # Get reviewer names
        num_reviewers = len(raw_data[0]) - 1
        for cell in raw_data[0][1:]:
            inputmatrix.reviewers.append(str(cell))

        # Get applicant names
        num_applicants = len(raw_data) - 1
        for row in raw_data:
            inputmatrix.applicants.append(row[0])

        # Get num values
        for i, row in enumerate(raw_data[1:num_applicants+1]):
            for j, cell in enumerate (row[1:num_reviewers+1]):
                inputmatrix.matrix[i][j] = cell

        print(inputmatrix.reviewers)
        print(inputmatrix.applicants)
        print(inputmatrix.matrix)

        return inputmatrix