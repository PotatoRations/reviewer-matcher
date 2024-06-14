from use_cases.InputMatrix import InputMatrix

class AssignReviewersUseCaseInterface():

    def assign_reviewers(self, input: InputMatrix, reviewer_load: int):
        raise NotImplementedError