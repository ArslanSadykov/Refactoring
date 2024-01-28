from Helper.start.start import start
from Helper.split.split import split


def main():
    head, q_start, q_start2, q_finish, tail, variants, students, tasks = start()
    split(head, q_start, q_start2, q_finish, tail, variants, students, tasks)


if __name__ == "__main__":
    main()
