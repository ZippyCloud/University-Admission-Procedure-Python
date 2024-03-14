from statistics import mean

departments = {"Biotech": {}, "Chemistry": {}, "Engineering": {}, "Mathematics": {}, "Physics": {}}
applicants = {}


def load_applicants():
    file = open("applicants.txt", "r")
    for line in file:
        first_name, last_name, physics, chemistry, math, computer_science, se, choice1, choice2, choice3 = line.split()
        full_name = first_name + " " + last_name
        physics = int(physics)
        chemistry = int(chemistry)
        math = int(math)
        computer_science = int(computer_science)
        se = int(se)
        applicants[full_name] = {
            "Physics": physics,
            "Chemistry": chemistry,
            "Mathematics": math,
            "Computer science": computer_science,
            "Special exam": se,
            "First choice": choice1,
            "Second choice": choice2,
            "Third choice": choice3
        }
    file.close()


def get_applicants(department, choice):
    applied = {}
    for key, value in applicants.items():
        if applicants[key][choice] == department:
            applied[key] = value
    return applied


def get_sorted_applicants(department, choice):
    if department == "Physics":
        return dict(
            sorted(get_applicants(department, choice).items(),
                   key=lambda x: (-max(mean([x[1]["Physics"], x[1]["Mathematics"]]), x[1]["Special exam"]), x[0])))
    elif department == "Engineering":
        return dict(
            sorted(get_applicants(department, choice).items(),
                   key=lambda x: (-max(mean([x[1]["Computer science"], x[1]["Mathematics"]]), x[1]["Special exam"]), x[0]))
        )
    elif department == "Biotech":
        return dict(
            sorted(get_applicants(department, choice).items(),
                   key=lambda x: (-max(mean([x[1]["Chemistry"], x[1]["Physics"]]), x[1]["Special exam"]), x[0]))
        )
    else:
        return dict(
            sorted(get_applicants(department, choice).items(),
                   key=lambda x: (-max(x[1][department], x[1]["Special exam"]), x[0])))


load_applicants()
limit = int(input())
for rounds in ["First choice", "Second choice", "Third choice"]:
    for department in departments.keys():
        applied = get_sorted_applicants(department, rounds)
        iterator = iter(applied.items())
        for key, value in applied.items():
            if len(departments[department]) < limit:
                departments[department][key] = value
                applicants.pop(key)
            else:
                break

for department, applicant_list in departments.items():
    if department == "Physics":
        departments[department] = dict(
            sorted(applicant_list.items(), key=lambda x: (-max(mean([x[1]["Physics"], x[1]["Mathematics"]]), x[1]["Special exam"]), x[0]))
        )
    elif department == "Engineering":
        departments[department] = dict(
            sorted(applicant_list.items(), key=lambda x: (-max(mean([x[1]["Computer science"], x[1]["Mathematics"]]), x[1]["Special exam"]), x[0]))
        )
    elif department == "Biotech":
        departments[department] = dict(
            sorted(applicant_list.items(), key=lambda x: (-max(mean([x[1]["Chemistry"], x[1]["Physics"]]), x[1]["Special exam"]), x[0]))
        )
    else:
        departments[department] = dict(sorted(applicant_list.items(), key=lambda x: (-x[1][department], x[0])))


for department, applicant_list in departments.items():
    with open(f"{department.lower()}.txt", "w", encoding="utf-8") as file:
        for name, data in applicant_list.items():
            if department == "Physics":
                print(name, max(mean([data["Physics"], data["Mathematics"]]), data["Special exam"]), file=file)
            elif department == "Engineering":
                print(name, max(mean([data["Computer science"], data["Mathematics"]]), data["Special exam"]), file=file)
            elif department == "Biotech":
                print(name, max(mean([data["Chemistry"], data["Physics"]]), data["Special exam"]), file=file)
            else:
                print(name, data[department], file=file)
