from io import TextIOWrapper
from controllers.ControllerInterface import ControllerInterface
from use_cases.AssignReviewersUseCaseInterface import AssignReviewersUseCaseInterface
from use_cases.ParseFileInterface import ParseFileInterface


class Controller(ControllerInterface):

    def add_assign_reviewers_use_case(self, assign_reviewers: AssignReviewersUseCaseInterface):
        self.assign_reviewers_use_case = assign_reviewers
        return
    
    def add_parse_file_use_case(self, parse_file: ParseFileInterface):
        self.parse_file = parse_file
        return

    def assign_reviewers(self, file: TextIOWrapper, reviewer_load: int):

        # get and parse file into input matrix
        input_matrix = self.parse_file.parse_file(file)

        # pass input matrix to use case
        self.assign_reviewers_use_case.assign_reviewers(input_matrix, reviewer_load)

        return