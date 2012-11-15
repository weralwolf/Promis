import json
fp = open("../data/json.examples/testCase.1.json", "r")
content = "".join([i.strip(" \n") for i in fp.readlines()])
data = json.JSONDecoder().decode(content)

import process

errors = {};

for i in data.keys():
    errors[i] = process.process(i, data[i]);

print errors;
