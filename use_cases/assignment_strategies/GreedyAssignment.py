
import copy
import math
from use_cases.InputMatrix import InputMatrix
from use_cases.OutputMatrix import OutputMatrix
from use_cases.assignment_strategies.AssignmentStrategyInterface import AssignmentStrategyInterface


class GreedyAssignment(AssignmentStrategyInterface):
    # hard-coded for now, maybe find a different solution later
    reviewers_per_applicant = 3
    # todo: make this changeable from outside
    # TODO: also make it so limit of each category (divide by 3rds)

    # scoring system:
    # first reviewer: 4
    # second reviewer: 2
    # reader: 1
    max_reviewer_score = 4

    def __init__(self):
        super().__init__()

    def sort(self, input_matrix: InputMatrix, reviewer_load: int) -> OutputMatrix:

        self.max_reviewer_score = reviewer_load
        # make a copy of input to do operations on
        input_copy = copy.deepcopy(input_matrix)

        # setup dict for the assigned applicants for each reviewer (ensures max applicants per reviewer)
        # reviewer_assignments = [[]] * len(input_matrix.reviewers) very stupid no good implementation due to pointers (all arrays point to same memory)
        reviewer_assignments = []
        for _ in input_matrix.reviewers:
            reviewer_assignments.append([])
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
                best_reviewer = self._get_best_reviewer(input_copy, applicant)
                # if no free reviewers found
                if best_reviewer < 0:
                    best_reviewer = self._resolve_conflict(input_matrix, applicant, reviewer_assignments)
                    assert best_reviewer >= 0   # sanity check, maybe throw error later, alternatively could just skip if not found
                
                # assign applicant and reviewer
                print("paired reviewer " + str(best_reviewer) + "with applicant " + str(applicant))
                reviewer_assignments[best_reviewer].append(applicant)
                applicant_assignments[applicant].append(best_reviewer)
                
                # wipe pairing on input_copy
                input_copy.matrix[best_reviewer][applicant] = -1
                # check if reviewer has max applicants, if so, set all compat to -1
                if len(reviewer_assignments[best_reviewer]) >= self.max_reviewer_score:
                    for j in range(0, len(input_matrix.applicants)):
                        input_copy.matrix[best_reviewer][j] = -1
                print(reviewer_assignments[best_reviewer])
        
        # setup and return output matrix
        output = OutputMatrix(reviewer_assignments, applicant_assignments, input_matrix.reviewers, input_matrix.applicants)
        return output

    """
    Returns the index of the reviewer that has the highest compatability with the applicant
    Returns -1 in case that no non-conflicting reviewers are found
    """
    def _get_best_reviewer(self, matrix: InputMatrix, applicant_index: int) -> int:
        max_compat = 0      # set this to 0 to rule out conflict (-1)
        max_index = -1
        for i in range(0, len(matrix.reviewers)):
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
        
        # Go through unchanged matrix and find best reviewer with the fewest assigned applicants over limit
        best_reviewer = -1
        lowest_load = math.inf
        best_score = 0

        for i in range(0, len(unchangedmatrix.reviewers)):
            # rule out conflict (-1)
            if unchangedmatrix.matrix[i][app_index] < 0:
                continue
            # rule out if this reviewer already has this applicant assigned
            if app_index in reviewer_assignments[i]:
                continue
            # check if app_num is lesser than best
            if len(reviewer_assignments[i]) < lowest_load:
                best_reviewer = i
                lowest_load = len(reviewer_assignments[i])
                best_score = unchangedmatrix.matrix[i][app_index]
                # change
            # also check if app_num is equal to best, then change only if score is better
            elif (len(reviewer_assignments[i]) == lowest_load) and (unchangedmatrix.matrix[i][app_index] > best_score):
                best_reviewer = i
                lowest_load = len(reviewer_assignments[i])
                best_score = unchangedmatrix.matrix[i][app_index]

        return best_reviewer