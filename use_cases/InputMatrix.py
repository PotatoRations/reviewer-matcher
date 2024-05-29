
class InputMatrix:

    # Initialise empty matrix
    def __init__(self) -> None:
        self.reviewers = []
        self.papers = []
        self.matrix = []

        # Not yet sure how to handle this, maybe with a flag in tuple?
        self.past_reviewers_pairs = []
        return

    def assign_value_by_name(self, reviewer: str, paper: str, value: int, past_reviewer: bool) -> bool:
        reviewer_index = self.reviewers.index(reviewer)
        paper_index = self.papers.index(paper)
        return self.assign_value_by_index(reviewer_index, paper_index, value, past_reviewer)
    
    def assign_value_by_index(self, reviewer_index: int, paper_index: int, value: int, past_reviewer: bool) -> bool:
        was_empty = True
        if self.matrix[reviewer_index][paper_index] != None:
            was_empty = False
        self.matrix[reviewer_index][paper_index] = (value, past_reviewer)
        return was_empty
