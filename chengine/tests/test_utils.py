import csv
from io import TextIOWrapper
import os
from typing import Optional
from pydantic import BaseModel

BASE_TEST_DIR = "./chengine/tests/positions/"

class Test(BaseModel):
    name: str
    fen: str
    moves: list[str]
    
    # Chat GPT, was wrong, missed out * on args
    @classmethod
    def from_args(cls, *args) -> 'Test': 
        fields = list(cls.__annotations__.keys())
        return cls(**dict(zip(fields, args)))
    
TestSuite = dict[str, list[Test]]
        
# Chat GPT
def read_csv(file_path):
    data = []
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        
        # Read the data rows
        for row in reader:
            data.append(row)
    
    return data

def parse_csv(file: TextIOWrapper) -> list[Test]:
    data = list(csv.reader(file, delimiter=','))
    tests = []
    for datum in data:
        datum[2] = datum[2].split("|") # Separate moves
        tests.append(Test.from_args(*datum))
    return tests


def read_tests(filename: Optional[str] = None, base_filepath=BASE_TEST_DIR) -> TestSuite:
    """
    @params filename: if defined, read tests from the filepath, otherwise read the entire directory
    @params base_filepath: default "./chengine/tests/positions/"
    @returns a dictionary of file name to tests
    """

    # Chat GPT
    tests = {}
    files = os.listdir(base_filepath) if not filename else [filename]

    for f in files:
        file_path = os.path.join(base_filepath, f)

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                tests[f] = parse_csv(file)

    return tests


