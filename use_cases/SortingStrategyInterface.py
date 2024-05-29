import InputMatrix
import OutputMatrix

"""
    Interface for the strategy used to assign reviewers to papers.
    Using a strategy design pattern here since my algorithm implementation is probably gonna be terrible
"""
class SortingStrategyInterface():

    def sort(self, matrix: InputMatrix) -> OutputMatrix:
        raise NotImplementedError