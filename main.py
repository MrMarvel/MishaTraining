import os
from datetime import datetime, timedelta
from tkinter import *
import numpy as np
from sys import platform
from playsound import playsound


def math_problem_generator(a: int):
    all_b = np.arange(1, 10)
    np.random.shuffle(all_b)
    for i in all_b:
        yield i


def log_out_procedure():
    playsound("resources/mario_death.mp3", block=False)
    if platform == "darwin":
        os.system("tell application \"System Events\" to log out")
    elif platform == "win32":
        os.system("rundll32.exe user32.dll, LockWorkStation")


class Logger:
    def __init__(self, log: Text):
        self._log = log

    def log(self, msg: str):
        self._log.configure(state='normal')
        self._log.insert(1.0, ''.join([msg, '\n']))
        self._log.configure(state='disabled')


class App:
    pass


if __name__ == '__main__':
    # MODEL SETUP
    root = Tk()

    time_left = StringVar(value="Времени осталось:")
    time_left_label = Label(textvariable=time_left)

    entry_frame = Frame(root)

    e = Entry(entry_frame, width=50)

    question = StringVar(value="Сколько будет {}?")
    question_text = Label(entry_frame, textvariable=question)

    result_log = Text(root, state=DISABLED)

    # Logger
    logger = Logger(result_log)

    # Misha Learning Programm
    wage = [1, 2, 2, 3, 4,
            5, 6, 18, 18, 1]

    sum_wage = sum(wage)

    p = [i / sum_wage for i in wage]

    a = np.random.choice(np.arange(1, 11), p=p)

    all_b = np.arange(1, 11)
    np.random.shuffle(all_b)
    # First iteration
    question_number = 1
    b = int(all_b[question_number - 1])
    question.set(f"Сколько будет {a} x {b} = ?")

    # Click Handler
    def send_result(event=None):
        global question_number
        global b
        if question_number > len(all_b):
            return
        result = e.get()
        if len(result) < 1:
            return
        e.delete(0, END)
        try:
            result = int(result)
        except ValueError:
            logger.log("Неправильный формат ввода: не число!")
            playsound("resources/roblox_negative.mp3", block=False)
            return

        if result == a * b:
            logger.log(f"{a} x {b} = {a * b} OK\n")
            question_number += 1
            if question_number >= len(all_b):
                # Вопросы закончились
                question.set("Молодец!")
                root.after(3000, lambda: root.destroy())
                return
            b = all_b[question_number - 1]
            question.set(f"Сколько будет {a} x {b} = ?")
        else:
            logger.log(f"{a} x {b} не будет равно {result}! ОШИБКА\n")
            playsound("resources/roblox_negative.mp3", block=False)

    def update_clock():
        now = datetime.now()
        delta: timedelta = max_time - now
        formatted_delta = delta + datetime(year=2000, month=1, day=1)

        if formatted_delta.second == 0 and formatted_delta.minute in (5, 4, 3, 2, 1):
            playsound("resources/notification.mp3", block=False)
        if formatted_delta.minute == 0 and formatted_delta.second in (45, 30, 15):
            playsound("resources/notification.mp3", block=False)
        if now > max_time:
            logger.log("ВРЕМЯ КОНЧИЛОСЬ!")
            root.after(3000, lambda: root.destroy())
            log_out_procedure()
            return
        time_left.set(formatted_delta.strftime("Времени осталось: %M:%S"))
        root.after(1000, update_clock)


    # Time init
    started_time = datetime.now()
    max_time = started_time + timedelta(minutes=0, seconds=10)
    clock_phase = 1
    update_clock()

    # Handling
    send_result_button = Button(entry_frame, text="ОК", width=4, command=lambda: send_result())
    e.bind("<Return>", send_result)

    # Constraints
    time_left_label.pack(side=TOP)
    entry_frame.pack(fill=X, expand=False, pady=1)
    send_result_button.pack(side=RIGHT)
    e.pack(side=RIGHT, padx=5)
    question_text.pack(side=LEFT, fill=NONE, padx=5)
    result_log.pack(fill=BOTH)

    # Get attention of user
    playsound("resources/ding.mp3", block=False)

    # Run app
    root.mainloop()
