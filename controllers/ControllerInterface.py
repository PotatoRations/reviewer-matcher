
from io import TextIOWrapper


class ControllerInterface:

    def assign_reviewers(self, file: TextIOWrapper, reviewer_load: int):
        raise NotImplementedError