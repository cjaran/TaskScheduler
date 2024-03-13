import os
import time


current_tasks = []
finished_tasks = []


def information():
    print("""Welcome to task keeping,
To start a new task press N,
To view current tasks press V,
To view finished tasks press F,
To finish a task press C,
To quit the program press Q,
To get this help info press H""")


def add_new_task(task):
    current_tasks.append([task, time.strftime("%H:%M:%S")])


def show_tasks():
    for task in current_tasks:
        print(f'Task: {task[0]} started at {task[1]}')


def finish_task():
    if not current_tasks:
        print("No tasks in progress.")
        return

    i = 0
    for task in current_tasks:
        print(i, task[0], ' started at ', task[1])
        i += 1
    task_to_del = int(input('Enter number beside task to delete -->\n'))
    if task_to_del > len(current_tasks):
        print("Invalid selection")
        finish_task()
    finished_time = time.strftime("%H:%M:%S")
    start_time = current_tasks[task_to_del][1]
    start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(":"))))
    current_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(finished_time.split(":"))))
    total_time_seconds = current_time_seconds - start_time_seconds
    total_time_hours, remainder = divmod(total_time_seconds, 3600)
    total_time_minutes, total_time_seconds = divmod(remainder, 60)
    total_time = f"{total_time_hours:02}:{total_time_minutes:02}:{total_time_seconds:02}"
    finished_tasks.append([f'{current_tasks[task_to_del][0]} finished at {finished_time}, total time {total_time}'])
    current_tasks.pop(task_to_del)


def show_finished_tasks():
    for task in finished_tasks:
        print(''.join(task))


def end_of_day():
    if os.name == 'nt':
        folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    else:
        folder = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    print(f'Saving to {folder}/TaskKeeping.txt')
    with open(folder + '/TaskKeeping.txt', 'w') as f:
        f.write('Finished tasks\n')
        for task in finished_tasks:
            f.write(' '.join(task) + '\n')
        f.write('Unfinished tasks\n')
        for task in current_tasks:
            f.write(' '.join(task) + '\n')


def main():
    try:
        information()
        while True:
            choice = input("Please enter your choice -->\n").lower()
            if choice == "h":
                information()
            elif choice == "n":
                new_task = input("Enter new task -->\n")
                add_new_task(new_task)
            elif choice == "v":
                show_tasks()
            elif choice == "c":
                finish_task()
            elif choice == "f":
                show_finished_tasks()
            elif choice == "q":
                print("Exiting program.")
                end_of_day()
                break
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("Exiting program.")
        end_of_day()
    except SystemExit:
        print("Exiting program.")
        end_of_day()


if __name__ == "__main__":
    main()