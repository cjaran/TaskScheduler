import os
import time


current_tasks = []
finished_tasks = []
paused_tasks = []

if os.name == 'nt':
    folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
else:
    folder = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


def information():
    print("""Welcome to task keeping,
To start a new task press N,
To pause a task press P,
To resume a task press R,
To view current tasks press V,
To view finished tasks press F,
TO view paused tasks press M,
To finish a task press C,
To quit the program press Q,
To get this help info press H,
Entering data without a choice will default to new task.""")


def add_new_task(task):
    current_tasks.append([task, time.strftime("%H:%M:%S")])


def show_tasks():
    if not current_tasks:
        print("No tasks")
    for task in current_tasks:
        print(f'Task: {task[0]} started at {task[1]}')

def resume_task():
    if not paused_tasks:
        print("No tasks are paused.")
        return
    i = 0
    for task in paused_tasks:
        print(i, task[0], ' total time take ', task[1])
        i += 1
    task_to_del = int(input('Enter number beside task to resume -->\n'))
    if task_to_del > len(paused_tasks):
        print("Invalid selection")
        resume_task()
    resume_time = time.strftime("%H:%M:%S")
    start_time = paused_tasks[task_to_del][1]
    start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(":"))))
    current_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(resume_time.split(":"))))
    resume_time_seconds = current_time_seconds - start_time_seconds
    resume_time_hours, remainder = divmod(resume_time_seconds, 3600)
    resume_time_minutes, resume_time_seconds = divmod(remainder, 60)
    total_time = f"{resume_time_hours:02}:{resume_time_minutes:02}:{resume_time_seconds:02}"
    current_tasks.append([paused_tasks[task_to_del][0], total_time])
    paused_tasks.pop(task_to_del)

def view_paused_tasks():
    if not paused_tasks:
        print("No paused tasks")
    for task in paused_tasks:
        print(f'Task: {task[0]} current time {task[1]}')

def pause_task():
    if not current_tasks:
        print("No tasks in progress.")
        return

    i = 0
    for task in current_tasks:
        print(i, task[0], ' started at ', task[1])
        i += 1
    task_to_del = int(input('Enter number beside task to pause -->\n'))
    if task_to_del > len(current_tasks):
        print("Invalid selection")
        finish_task()
    paused_time = time.strftime("%H:%M:%S")
    start_time = current_tasks[task_to_del][1]
    start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(":"))))
    current_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(paused_time.split(":"))))
    total_time_seconds = current_time_seconds - start_time_seconds
    total_time_hours, remainder = divmod(total_time_seconds, 3600)
    total_time_minutes, total_time_seconds = divmod(remainder, 60)
    total_time = f"{total_time_hours:02}:{total_time_minutes:02}:{total_time_seconds:02}"
    paused_tasks.append([current_tasks[task_to_del][0], total_time])
    current_tasks.pop(task_to_del)


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
    if not finished_tasks:
        print("No tasks finished")
    for task in finished_tasks:
        print(''.join(task))


def end_of_day():
    print(f'Saving to {folder}/TaskKeeping.txt')
    with open(folder + '/TaskKeeping.txt', 'w') as f:
        f.write('Finished tasks\n')
        for task in finished_tasks:
            f.write(' '.join(task) + '\n')
            #pass
        f.write('Unfinished tasks\n')
        for task in current_tasks:
            f.write(' '.join(task) + '\n')
            #pass


def load_previous_tasks():
    try:
        with open(folder + '/TaskKeeping.txt', 'r') as f:
            unfinished = False
            for line in f.readlines():
                line = line.strip()
                if "Finished" in line:
                    continue
                elif not unfinished:
                    finished_tasks.append([line, 'Yesterday'])
                elif "Unfinished" in line:
                    unfinished = True
                    continue
                elif unfinished:
                    current_tasks.append([line, 'Yesterday'])
    except FileNotFoundError:
        print("No tasks found")


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
            elif choice == "m":
                view_paused_tasks()
            elif choice == "p":
                pause_task()
            elif choice == "r":
                resume_task()
            elif choice == "l":
                pass
            elif choice == "q":
                print("Exiting program.")
                end_of_day()
                break
            else:
                add_new_task(choice)
    except KeyboardInterrupt:
        print("Exiting program.")
        end_of_day()
    except SystemExit:
        print("Exiting program.")
        end_of_day()


if __name__ == "__main__":
    main()
