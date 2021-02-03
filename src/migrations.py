import json
import data


with open('db/teachers.json', 'w') as f:
    json.dump(data.teachers, f)

with open('db/goals.json', 'w') as f:
    json.dump(data.goals, f)
