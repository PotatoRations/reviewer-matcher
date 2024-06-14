
from ui.UIInterface import UIInterface
from use_cases.OutputMatrix import OutputMatrix


class PresenterInterface:
    def __init__(self) -> None:
        pass

    def add_UI(self, ui: UIInterface):
        raise NotImplementedError
    
    def present_output(self, output_matrix: OutputMatrix):
        raise NotImplementedError