# simple automata validator
## how it works:
with Bruteforce, the algorithm generates different words from the specified alphabet and compares the results with a defined equivalent FA function.
Algorithm will return a list that contains not matched results.
the algorithm input is a JSON file that must in `schema.config.json` file schema

## simple example:
in file `example.json` is FA module of question:

write a _DFA_ that accept language that contain odd number of zero and not contain odd number of zero with alphabet = {1,0}

## Todo:
1. [ ] draw machine
2. [ ] support another type of machines
3. [ ] get natural language problem and convert it to a automata