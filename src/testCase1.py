import json
fileName = "../data/json.examples/testCase.1.json";
data = json.load(file(fileName, "r"));

import process

errors = {};

for i in data.keys():
    errors[i] = process.process(i, data[i]);

print errors;
