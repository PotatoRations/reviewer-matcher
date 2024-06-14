
import copy
import math
from use_cases.InputMatrix import InputMatrix
from use_cases.OutputMatrix import OutputMatrix
from use_cases.assignment_strategies.AssignmentStrategyInterface import AssignmentStrategyInterface


class GreedyAssignmentSplit(AssignmentStrategyInterface):
    # hard-coded for now, maybe find a different solution later
    reviewers_per_applicant = 3


    max_reviewer_load = 6

    def __init__(self):
        super().__init__()

    def sort(self, input_matrix: InputMatrix, reviewer_load: int) -> OutputMatrix:

        self.max_reviewer_load = reviewer_load

        # setup dict for the assigned applicants for each reviewer (ensures max applicants per reviewer)
        # reviewer_assignments = [[]] * len(input_matrix.reviewers) very stupid no good implementation due to pointers (all arrays point to same memory)
        reviewer_assignments = []
        for _ in input_matrix.reviewers:
            reviewer_assignments.append(([], [], []))   # tuple containing list of first, secondary, and reader roles assigned
        # setup list for the reviewers assigned for each applicant (ensures each applicant gets 3 reviewers)
        applicant_assignments = []
        for _ in input_matrix.applicants:
            applicant_assignments.append([])

        # iterate for enough rounds to give each applicant "reviewers_per_applicant" reviewers
        for round in range(0, self.reviewers_per_applicant):
            # reverse order between each round of picking
            order = None
            if round % 2:
                order = range(0, len(input_matrix.applicants))
            else:
                order = range(len(input_matrix.applicants)-1, -1, -1)

            # assign reviewers for each applicant   
            for applicant in order:
                # get highest compatability reviewer
                best_reviewer = self._get_best_reviewer(input_matrix, applicant, reviewer_assignments, round)
                # if no free reviewers found
                if best_reviewer < 0:
                    best_reviewer = self._resolve_conflict(input_matrix, applicant, reviewer_assignments)
                    assert best_reviewer >= 0   # sanity check, maybe throw error later, alternatively could just skip if not found
                
                # assign applicant and reviewer
                print("paired reviewer " + str(best_reviewer) + "with applicant " + str(applicant))
                reviewer_assignments[best_reviewer][round].append(applicant)
                applicant_assignments[applicant].append(best_reviewer)
        
        # setup and return output matrix
        # TODO: reviewer_assignments shouldn't be needed for OutputMatrix, maybe refactor this out later
        output = OutputMatrix(None, applicant_assignments, input_matrix.reviewers, input_matrix.applicants)
        return output

    """
    Returns the index of the reviewer that has the highest compatability with the applicant
    Returns -1 in case that no non-conflicting reviewers are found
    """
    def _get_best_reviewer(self, matrix: InputMatrix, applicant_index: int, reviewer_assigments: list[tuple[list, list, list]], round: int) -> int:
        max_compat = 0      # set this to 0 to rule out conflict (-1)
        max_index = -1
        for i in range(0, len(matrix.reviewers)):
            # bypass reviewer if this tier is already full (each tier is 1/3 of total)
            if len(reviewer_assigments[i][round]) >= math.ceil(self.max_reviewer_load / 3.0):
                continue
            # bypass reviewer if this reviewer is already reviewing our applicant
            if self._already_assigned(applicant_index, i, reviewer_assigments):
                continue
            # check compatability
            if (matrix.matrix[i][applicant_index] >= max_compat):
                max_compat = matrix.matrix[i][applicant_index]
                max_index = i
        return max_index
    
    """
    Handles case where we cannot find a free non-conflicting reviewer for the applicant
    In this case finds the highest compatable reviewer that has the lowest # of assignments over limit

    returns index of this reviewer
    """
    def _resolve_conflict(self, unchangedmatrix: InputMatrix, app_index: int, reviewer_assignments):
        
        # scores representing the workload of each assignment
        # first reviewer is worth 4, second reviewer is worth 2, reader is worth 1
        scores = (4, 2, 1)

        # Go through unchanged matrix and find best reviewer with the fewest assigned applicants over limit
        best_reviewer = -1
        lowest_load = math.inf
        best_score = 0

        for i in range(0, len(unchangedmatrix.reviewers)):
            # rule out conflict (-1)
            if unchangedmatrix.matrix[i][app_index] < 0:
                continue
            # rule out if this reviewer already has this applicant assigned
            if self._already_assigned(app_index, i, reviewer_assignments):
                continue

            # calculate load on reviewer
            load = 0
            for j, lst in enumerate(reviewer_assignments[i]):
                load += len(lst)*scores[j]
            
            # check if load is lesser than best so far
            if load < lowest_load:
                # change
                best_reviewer = i
                lowest_load = load
                best_score = unchangedmatrix.matrix[i][app_index]
            # also check if app_num is equal to best, then change only if score is better
            elif (load == lowest_load) and (unchangedmatrix.matrix[i][app_index] > best_score):
                best_reviewer = i
                lowest_load = load
                best_score = unchangedmatrix.matrix[i][app_index]

        return best_reviewer
    
    """
    Returns if this applicant was already assigned to this reviewer"""
    def _already_assigned(self, applicant: int, reviewer: int, reviewer_assignemnts: list):
        for lst in reviewer_assignemnts[reviewer]:
            if applicant in lst:
                return True
        return False