
import copy
from use_cases.InputMatrix import InputMatrix
from use_cases.OutputMatrix import OutputMatrix
from use_cases.assignment_strategies.AssignmentStrategyInterface import AssignmentStrategyInterface


class BipartiteAssignment(AssignmentStrategyInterface):
    
    def sort(self, reference_matrix: InputMatrix) -> OutputMatrix:

        # make a copy of input to do operations on
        matrix = copy.deepcopy(reference_matrix)

        
        

        return super().sort(matrix)