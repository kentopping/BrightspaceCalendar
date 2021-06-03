import os
from os import path


class DTO:
    def __init__(self):
        self.file = None

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
