from controllers.Controller import Controller
from presenters.Presenter import Presenter
from ui.UI import UI
from use_cases.AssignReviewersUseCase import AssignReviewersUseCase
from use_cases.BetterParseFile import BetterParseFile
from use_cases.ParseFile import ParseFile
from use_cases.assignment_strategies.GreedyAssignment import GreedyAssignment
from use_cases.assignment_strategies.GreedyAssignmentSplit import GreedyAssignmentSplit


def main():
    # Initialise everything
    ui = UI()
    controller = Controller()
    #fileparser = ParseFile()
    fileparser = BetterParseFile()
    assign_usecase = AssignReviewersUseCase()
    greedy_assignment = GreedyAssignmentSplit()
    presenter = Presenter()

    ui.add_controller(controller)
    controller.add_parse_file_use_case(fileparser)
    controller.add_assign_reviewers_use_case(assign_usecase)
    assign_usecase.add_assignment_strategy(greedy_assignment)
    assign_usecase.add_presenter(presenter)
    presenter.add_UI(ui)
    

    # Start UI
    print("Starting program")
    ui.start()

if __name__ == "__main__":
    main()
