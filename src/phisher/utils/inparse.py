import json
from os import path, abort


def read(file):
    if path.exists(file) is True:
        with open(file, 'r', encoding='utf-8') as fd:
            inf = json.load(fd)
        return inf
    else:
        print("read error: File does not exist")
        abort()


class Inparse:
    def __init__(self):
        self.domains = list()
        self.topdomains = list()
        self.brandnames = list()
        self.whois = dict()
        self.keywords = list()
        self.imglinks = list()
        # Other points ...

    def parse(self, input_inf):
        for point in input_inf:
            match point:
                case "domains":
                    self.domains = input_inf["domains"]
                case "topdomains":
                    self.topdomains = input_inf["topdomains"]
                case "brandnames":
                    self.brandnames = input_inf["brandnames"]
                case "whois":
                    self.whois = input_inf["whois"]
                case "keywords":
                    self.keywords = input_inf["keywords"]
                case "imglinks":
                    self.imglinks = input_inf["imglinks"]
                # Other points ...


if __name__ == "__main__":
    file_name = input()
    input_file = read(file_name)
    perimetr = Inparse()
    perimetr.parse(input_file)
