import os
from os import path


# Data transfer object
class DTO:
    def __init__(self):
        self.file = None

    def read_txt(self, name):
        file = None
        array = []
        if path.exists(f"{name}"):
            file = open(f"{name}", "r")
        for f in file:
            f = f.rstrip("\n")
            array.append(f)
        file.close()
        return array

    def read_csv(self, name):
        if path.exists(f"{name}.csv"):
            file = open(f"{name}.csv", "r")
            self.file = file

    def delete_csv(self, array):
        for name in array:
            if path.exists(f"{name}.csv"):
                os.remove(f"{name}.csv")

    def get_file(self):
        return self.file
