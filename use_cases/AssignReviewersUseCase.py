from presenters.PresenterInterface import PresenterInterface
from use_cases.AssignReviewersUseCaseInterface import AssignReviewersUseCaseInterface
from use_cases.assignment_strategies.AssignmentStrategyInterface import AssignmentStrategyInterface
from use_cases.InputMatrix import InputMatrix


"""
Thingy for assigning reviewers

input specification:
- N*M InputMatrix object with N reviewers and M applicants
- Values range from -1 to some int, representing higher compatability
- -1 means conflict, will never be paired

"""
class AssignReviewersUseCase(AssignReviewersUseCaseInterface):
    
    def __init__(self) -> None:
        super().__init__()
        self.strategy = None
        return

    def assign_reviewers(self, input: InputMatrix, reviewer_load: int):
        output = self.strategy.sort(input, reviewer_load)
        self.presenter.present_output(output, input)
        return
    
    def add_assignment_strategy(self, strategy: AssignmentStrategyInterface):
        self.strategy = strategy

    def add_presenter(self, presenter: PresenterInterface):
        self.presenter = presenter