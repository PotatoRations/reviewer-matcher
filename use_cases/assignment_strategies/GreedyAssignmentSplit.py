
import copy
import math
from use_cases.InputMatrix import InputMatrix
from use_cases.OutputMatrix import OutputMatrix
from use_cases.assignment_strategies.AssignmentStrategyInterface import AssignmentStrategyInterface
import pprint

"""
This one doesn't seem to work
"""
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
        reviewer_availabilities = []
        for _ in input_matrix.reviewers:
            reviewer_assignments.append([])   
            reviewer_availabilities.append([reviewer_load // 3, reviewer_load // 3, reviewer_load // 3])

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
                best_reviewer = self._get_best_reviewer(input_matrix, applicant, reviewer_assignments, reviewer_availabilities, round)
                # if no free reviewers found
                if best_reviewer < 0:
                    best_reviewer = self._resolve_conflict(input_matrix, applicant, reviewer_assignments, reviewer_availabilities)
                    assert best_reviewer >= 0   # sanity check, maybe throw error later, alternatively could just skip if not found
                
                # assign applicant and reviewer
                reviewer_assignments[best_reviewer].append(applicant)
                applicant_assignments[applicant].append(best_reviewer)
                # tick down reviewer availability:
                self._reduce_availability(best_reviewer, reviewer_availabilities, round)

            # tick over any unused availabilities to next round
            for i in range(0, len(input_matrix.reviewers)):
                self._carry_over_availability(i, reviewer_availabilities, round)
        
        # setup and return output matrix
        # TODO: reviewer_assignments shouldn't be needed for OutputMatrix, maybe refactor this out later
        output = OutputMatrix(None, applicant_assignments, input_matrix.reviewers, input_matrix.applicants)
        return output

    """
    Reduces availability of reviewer at round by 1
    """
    def _reduce_availability(self, reviewer: int, reviewer_availability: list, round: int):
        # subtract an availability
        reviewer_availability[reviewer][round] -= 1

        # reformat availability list (one extra assignment is worth 2 assignments in the next category)
        # thus getting an extra first reviewer assignment will take up 2 secondary reviewer positions
        # move negatives from 0th spot to 1st spot
        if reviewer_availability[reviewer][0] < 0:
            self._carry_over_availability(reviewer, reviewer_availability, 0)
        # move negatives from 1st spot to 2nd spot
        if reviewer_availability[reviewer][1] < 0:
            self._carry_over_availability(reviewer, reviewer_availability, 1)
        # negatives in 2nd spot are not removed, used to calculate reviewer load when resolving conflicts
        return
    
    """
    Carries over availability from this round to the next round
    """
    def _carry_over_availability(self, reviewer: int, reviewer_availability: list, round: int):
        if round >= self.reviewers_per_applicant - 1 or round < 0:
            return
        reviewer_availability[reviewer][round+1] += 2*reviewer_availability[reviewer][round]
        reviewer_availability[reviewer][round] = 0
        return

    """
    Returns the index of the reviewer that has the highest compatability with the applicant
    Returns -1 in case that no non-conflicting reviewers are found
    """
    def _get_best_reviewer(self, matrix: InputMatrix, applicant_index: int, reviewer_assignments: list, reviewer_availabilities: list, round: int) -> int:
        max_compat = 0      # set this to 0 to rule out conflict (-1)
        max_index = -1
        for i in range(0, len(matrix.reviewers)):
            # bypass reviewer if this tier is already full 
            if reviewer_availabilities[i][round] <= 0:
                continue

            # bypass reviewer if this reviewer is already reviewing our applicant
            if applicant_index in reviewer_assignments[i]:
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
    def _resolve_conflict(self, unchangedmatrix: InputMatrix, app_index: int, reviewer_assignments, reviewer_availabilities):
        
        # scores representing the workload of each assignment
        # first reviewer is worth 4, second reviewer is worth 2, reader is worth 1
        scores = (4, 2, 1)

        # Go through unchanged matrix and find best reviewer with the fewest assigned applicants over limit
        best_reviewer = -1
        best_free = -math.inf
        best_score = -0.5

        for i in range(0, len(unchangedmatrix.reviewers)):
            # rule out conflict (-1)
            if unchangedmatrix.matrix[i][app_index] < 0:
                continue

            # bypass reviewer if this reviewer is already reviewing our applicant
            if app_index in reviewer_assignments[i]:
                continue

            # calculate load on reviewer according to remaining slots
            spaces_free = 0
            for j, element in enumerate(reviewer_availabilities[i]):
                spaces_free += element*scores[j]
            
            # check if load is lesser than best so far
            if spaces_free > best_free:
                # change
                best_reviewer = i
                best_free = spaces_free
                best_score = unchangedmatrix.matrix[i][app_index]
            # also check if load is equal to best, then change only if score is better
            elif (spaces_free == best_free) and (unchangedmatrix.matrix[i][app_index] > best_score):
                best_reviewer = i
                best_free = spaces_free
                best_score = unchangedmatrix.matrix[i][app_index]

        return best_reviewer