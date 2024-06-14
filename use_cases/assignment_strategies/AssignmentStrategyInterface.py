from use_cases.InputMatrix import InputMatrix
from use_cases.OutputMatrix import OutputMatrix

"""
    Interface for the strategy used to assign reviewers to papers.
    Using a strategy design pattern here since my algorithm implementation is probably gonna be terrible
"""
class AssignmentStrategyInterface():

    def sort(self, matrix: InputMatrix, reviewer_load: int) -> OutputMatrix:
        raise NotImplementedError