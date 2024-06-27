
from use_cases.InputMatrix import InputMatrix
from use_cases.OutputMatrix import OutputMatrix
from use_cases.assignment_strategies.AssignmentStrategyInterface import AssignmentStrategyInterface

from ortools.sat.python import cp_model

# Use thing from here
# https://developers.google.com/optimization/assignment/assignment_cp



class CPSATAssignment(AssignmentStrategyInterface):


    def sort(self, matrix: InputMatrix, reviewer_load: int) -> OutputMatrix:
        
        # Model
        model = cp_model.CpModel()

        num_reviewers = len(matrix.reviewers)
        num_applicants = len(matrix.applicants)

        ## variables
        round_1 = {}
        round_2 = {}
        round_3 = {}
        for reviewer in range(num_reviewers):
            for applicant in range(num_applicants):
                round_1[reviewer, applicant] = model.new_bool_var(f"x[{reviewer},{applicant}]")
                round_2[reviewer, applicant] = model.new_bool_var(f"x[{reviewer},{applicant}]")
                round_3[reviewer, applicant] = model.new_bool_var(f"x[{reviewer},{applicant}]")

        ## Constraints
        # Each applicant gets 1 reviewer per round
        for applicant in range(num_applicants):
            model.add_exactly_one(round_1[reviewer, applicant] for reviewer in range(num_reviewers))
            model.add_exactly_one(round_2[reviewer, applicant] for reviewer in range(num_reviewers))
            model.add_exactly_one(round_3[reviewer, applicant] for reviewer in range(num_reviewers))




        raise NotImplementedError