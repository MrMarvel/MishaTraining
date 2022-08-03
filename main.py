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
        import osascript
        os.system("/System/Library/CoreServices/Menu\\ Extras/user.menu/Contents/Resources/CGSession -suspend")
        # os.system("tell application \"System Events\" to log out")
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
    def __init__(self):
        self.all_b = None
        self.a: int = 0
        self.b: int = 0
        self.question_number: int = 0
        self.send_result_button: Button | None = None
        self.result_log: Text | None = None
        self.question_text: Label | None = None
        self.question: StringVar | None = None
        self.e: Entry | None = None
        self.entry_frame: Frame | None = None
        self.time_left_label: Label | None = None
        self.time_left: StringVar | None = None
        self.root: Tk | None = None
        self.model_setup()
        self.make_constraints()

    def model_setup(self):
        # MODEL SETUP
        self.root = Tk()

        self.time_left = StringVar(value="Времени осталось:")
        self.time_left_label = Label(textvariable=self.time_left)

        self.entry_frame = Frame(self.root)

        self.e = Entry(self.entry_frame, width=50)

        self.question = StringVar(value="Сколько будет {}?")
        self.question_text = Label(self.entry_frame, textvariable=self.question)

        self.result_log = Text(self.root, state=DISABLED)

        self.send_result_button = Button(self.entry_frame, text="ОК", width=4)

    def run(self):

        # Logger
        logger = Logger(self.result_log)

        # Misha Learning Programm
        wage = [1, 2, 2, 3, 4,
                5, 6, 18, 18, 1]

        sum_wage = sum(wage)

        p = [i / sum_wage for i in wage]

        self.a = np.random.choice(np.arange(1, 11), p=p)

        self.all_b = np.arange(1, 11)
        np.random.shuffle(self.all_b)
        # First iteration
        self.question_number = 1
        self.b = int(self.all_b[self.question_number - 1])
        self.question.set(f"Сколько будет {self.a} x {self.b} = ?")

        questions_are_resolved = False

        # Click Handler
        def send_result(event=None):
            if self.question_number > len(self.all_b):
                return
            result = self.e.get()
            if len(result) < 1:
                return
            self.e.delete(0, END)
            try:
                result = int(result)
            except ValueError:
                logger.log("Неправильный формат ввода: не число!")
                playsound("resources/roblox_negative.mp3", block=False)
                return

            if result == self.a * self.b:
                logger.log(f"{self.a} x {self.b} = {self.a * self.b} OK\n")
                self.question_number += 1
                if self.question_number >= len(self.all_b):
                    # Вопросы закончились
                    self.questions_are_resolved = True
                    self.question.set("Молодец!")
                    self.root.after(3000, lambda: self.root.destroy())
                    return
                self.b = self.all_b[self.question_number - 1]
                self.question.set(f"Сколько будет {self.a} x {self.b} = ?")
            else:
                logger.log(f"{self.a} x {self.b} не будет равно {result}! ОШИБКА\n")
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
                self.root.after(3000, lambda: self.root.destroy())
                self.root.after(1000, lambda: log_out_procedure())
                return
            self.time_left.set(formatted_delta.strftime("Времени осталось: %M:%S"))
            self.root.after(1000, update_clock)

        # Time init
        started_time = datetime.now()
        max_time = started_time + timedelta(minutes=0, seconds=10)
        clock_phase = 1
        update_clock()

        # Handling
        self.e.bind("<Return>", send_result)
        self.send_result_button.configure(command=lambda: send_result())

        # Get attention of user
        playsound("resources/ding.mp3", block=False)

        # Run app
        self.root.mainloop()

        return questions_are_resolved

    def make_constraints(self):  # Constraints
        self.time_left_label.pack(side=TOP)
        self.entry_frame.pack(fill=X, expand=False, pady=1)
        self.send_result_button.pack(side=RIGHT)
        self.e.pack(side=RIGHT, padx=5)
        self.question_text.pack(side=LEFT, fill=NONE, padx=5)
        self.result_log.pack(fill=BOTH)


if __name__ == '__main__':
    while not App().run():
        pass
