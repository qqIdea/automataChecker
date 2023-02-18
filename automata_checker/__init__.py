from json import load
from os import PathLike
from typing import Union, Callable
import random
from jsonschema import validate


def dfa_validator(file: Union[str, bytes, PathLike[str], PathLike[bytes], int],
                  equalFunc: Callable[[str], bool], repetition: int, minLen: int = 1, maxLen: int = 50):
    """a Bruteforce algorithm
    Notes:
        Json file must be in schema
    Args:
        file: json file path or something simular
        equalFunc: a function that result is same as FA
        repetition: how many times FA & function must check
        minLen: minimum length of test case word
        maxLen: maximum length of test case word
    Returns:
        a list of words that they didn't get some result
     """
    def do_dfa(word: str) -> bool:
        nonlocal cashed_indexed_name
        nonlocal jsonData
        currentState = jsonData['initial state']
        for i in word:
            newState = jsonData['stats'][cashed_indexed_name[currentState]]['actions'].get(i)
            if newState is not None:
                currentState = newState
        result = jsonData['stats'][cashed_indexed_name[currentState]].get('accept')
        return False if result is None else result

    def equality_check():
        word = random_word_gen(jsonData['alphabets'], minLen, maxLen)
        if equalFunc(word) != do_dfa(word):
            return word

    def indexing_by_name(data: dict) -> dict[str, int]:
        nameIndex = {}
        index = 0
        for item in data['stats']:
            nameIndex.update({item['name']: index})
            index += 1
        return nameIndex

    def random_word_gen(alphabetsList: list[str], start: int, stop: int):
        """Return random string from alphabets in random length in range [start, stop], including both end points.
            """
        return ''.join(random.choices(population=alphabetsList, k=random.randint(start, stop)))

    schema = {
        'type': 'object',
        "properties": {
            'stats': {"type": "array", "items": {
                'type': 'object',
                "properties": {
                    "name": {"type": "string"},
                    'accept': {"type": "boolean"},
                    'actions': {'type': 'object',
                                'properties': {"additionalProperties": True}},
                    "additionalProperties": False
                }, 'required': ['name', 'actions']
            }},
            'alphabets': {"type": "array", "items": {'type': "string", "maxLength": 1}},
            'initial state': {'type': 'string'},
            "additionalProperties": False
        },
        'required': ['stats', 'alphabets', 'initial state']
    }

    with open(file, mode='r') as file:
        jsonData = load(file)
    validate(jsonData, schema=schema)
    cashed_indexed_name = indexing_by_name(jsonData)
    badWords = [equality_check() for i in range(repetition)]
    return [x for x in badWords if x is not None]
