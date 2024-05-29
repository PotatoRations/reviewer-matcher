
from io import TextIOWrapper


class ParseFileInterface():

    def parse_file(self, file: TextIOWrapper):
        raise NotImplementedError