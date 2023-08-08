#%%
# Import Tkinter module and os module
import tkinter as tk
import time
import datetime
import os
import threading 
import platform


# Create a parent class for the script runner
class ScriptRunner:
    def __init__(self, rest_time:int, next_execution_time:int):
        self.stop_flag = [False]
        self.thread = None
        self.rest_time = rest_time
        self.next_execution_time = next_execution_time 

    def beep(self):
        print("beep")

    def running(self):
        while True:
            if not self.stop_flag[0]:
                print(f"{datetime.datetime.now()} -- Process ran")
                [self.beep() for _ in range(2)] 
                # Use rest time from variable
                time.sleep(self.rest_time.get())
            if not self.stop_flag[0]:
                self.beep()
                # Use next execution time from variable
                time.sleep(self.next_execution_time.get())
            if self.stop_flag[0]:
                print("Thread stopped by flag")
                print('Execution Stopped')
                return

    def run_script(self):
        self.stop_flag[0] = False 
        self.thread = threading.Thread(target=self.running) # Create a new thread with the running method as target
        self.thread.start()

    def stop_script(self):
        self.stop_flag[0] = True


class WindowsScriptRunner(ScriptRunner):
    def beep(self):
    
        import winsound
        winsound.Beep(440, 500)

class MacScriptRunner(ScriptRunner):
    def beep(self):

        os.system("say beep")

class LinuxScriptRunner(ScriptRunner):
    def beep(self):

        os.system("beep -l300 -f750")


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Script Runner")
        rest_time = tk.IntVar(master=self.root)
        next_execution_time = tk.IntVar(master=self.root)

        os_name = platform.system()
        if os_name == "Windows":
            self.script_runner = WindowsScriptRunner(rest_time=rest_time, next_execution_time=next_execution_time)
        elif os_name == "Darwin":
            self.script_runner = MacScriptRunner(rest_time=rest_time, next_execution_time=next_execution_time)
        elif os_name == "Linux":
            self.script_runner = LinuxScriptRunner(rest_time=rest_time, next_execution_time=next_execution_time)
        else:
            self.script_runner = ScriptRunner(rest_time=rest_time, next_execution_time=next_execution_time)

        
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

       
        self.run_button = tk.Button(self.root, text="Run", command=self.script_runner.run_script)

        
        self.stop_button = tk.Button(self.root, text="Stop", command=self.script_runner.stop_script)

        
        self.run_button.pack()
        self.stop_button.pack()

        # Create labels and entries for rest time and next execution time
        rest_label = tk.Label(self.root, text="Rest time (seconds):")
        rest_label.pack()
        rest_entry = tk.Entry(self.root, textvariable=rest_time)
        rest_entry.pack()

        next_label = tk.Label(self.root, text="Next execution time (seconds):")
        next_label.pack()
        next_entry = tk.Entry(self.root, textvariable=next_execution_time)
        next_entry.pack()

    
        self.flag_label = tk.Label(self.root, text="🏳️", font=("Arial", 24))

        
        self.flag_label.pack()

        # Set default values for rest time and next execution time
        rest_time.set(30)
        next_execution_time.set(1200)

    def update_flag(self):
        
        if self.script_runner.stop_flag[0]:
            
            self.flag_label.config(text="🚩", fg="red")
        else:
            
            self.flag_label.config(text="🏳️", fg="green")
        
        self.root.after(100, self.update_flag)

    def start(self):
        
        self.update_flag()
        
        self.root.mainloop()

# Create an instance of GUI and start it
gui = GUI()
gui.start()
