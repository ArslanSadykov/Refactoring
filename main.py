import io
import os
import random


def readTasks():
    result = []
    tasks_directory = 'tasks'
    if not os.path.exists(tasks_directory):
        print(f"Error: {tasks_directory} does not exist.")
        return result

    totalTasks = len(os.listdir(tasks_directory))
    print(totalTasks)
    for i in range(1, totalTasks):
        result.append([])
        task_path = os.path.join(tasks_directory, str(i))
        if not os.path.exists(task_path):
            print(f"Error: {task_path} does not exist.")
            continue

        totalVariants = len(os.listdir(task_path))
        for k in range(1, totalVariants):
            file_path = os.path.join(task_path, f"{k}.tex")
            if not os.path.exists(file_path):
                print(f"Error: {file_path} does not exist.")
                continue

            result[i - 1].append(readFile(file_path))
    return result


def readStudents():
    students_file = "students.txt"
    if not os.path.exists(students_file):
        print(f"Error: {students_file} does not exist.")
        return []

    with io.open(students_file, encoding='utf-8') as file:
        result = file.readlines()
    return result


def generateVariants(tasks, total):
    counts = [len(i) for i in tasks]
    result = set()

    # Check if any task has no variants
    if any(count == 0 for count in counts):
        print("Error: Some tasks have no variants.")
        return []

    while len(result) < total:
        result.add(generateVariant(counts))
    return list(result)



def generateVariant(counts):
    return tuple(random.randint(1, count) for count in counts)


def readFile(name):
    if not os.path.exists(name):
        print(f"Error: {name} does not exist.")
        return ''

    with io.open(name, encoding='utf-8') as file:
        text = file.read()
    return text


def main():
    random.seed(1183)
    print("Reading templates...")
    head = readFile('templates/head.tex')
    q_start = readFile('templates/qStart.tex')
    q_start2 = readFile('templates/qStart2.tex')
    q_finish = readFile('templates/qFinish.tex')
    tail = readFile('templates/tail.tex')

    print("Reading tasks...")
    tasks = readTasks()

    print("Reading students...")
    students = readStudents()

    if not tasks or not students:
        print("Exiting due to errors in reading tasks or students.")
        return

    print("Generating variants...")
    variants = generateVariants(tasks, len(students))
    random.shuffle(variants)

    os.makedirs(os.path.dirname("latex/main.tex"), exist_ok=True)

    with io.open("latex/main.tex", "w", encoding='utf-8') as out:
        print("Making main.tex file...")
        out.write(head)
        for i in range(len(variants)):
            out.write(q_start + str(students[i]) + q_start2)
            for taskNumber, task in enumerate(tasks):
                out.write(task[variants[i][taskNumber] - 1])
            out.write(q_finish)
        out.write(tail)

    with io.open("latex/dump.tex", "w", encoding='utf-8') as out:
        print("Making dump.tex file...")
        out.write(head)
        for i, task in enumerate(tasks):
            out.write(q_start + str(i + 1) + q_start2)
            for k in range(len(task)):
                out.write(task[k])
            out.write(q_finish)
        out.write(tail)

    print("Done!")


if __name__ == "__main__":
    main()
