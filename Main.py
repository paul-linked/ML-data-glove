import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import time
import threading
from queue import Queue
import requests
from random import randint
from functools import partial

#import other files
import sensorDataCollection as SDC

class GloveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.recording_thread = None
        self.recording = False
        self.title("Glove Training Data Collection")
        self.geometry("1700x800")
        self.create_widgets()
        self.create_button_style()
        self.message_queue = Queue()
        self.after(100, self.process_queue)


    def process_queue(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            if message[0] == "update_recording_status":
                self.update_recording_status(*message[1])
            elif message[0] == "update_countdown":
                self.update_countdown(*message[1])
            elif message[0] == "update_current_letter":
                self.update_current_letter(*message[1])
            elif message[0] == "update_graph":
                self.update_graph(*message[1], *message[2])
            self.message_queue.task_done()
            
        self.after(100, self.process_queue)

    

    def create_button_style(self):
        style = ttk.Style()
        style.configure("Start.TButton", background="lime", foreground="black")
        style.configure("Stop.TButton", background="red", foreground="black")
        style.configure("Neutral.TButton")  


    def create_widgets(self):

        #colomn 0 ---------------------------------------------------------------------------------------------------------

        # Graphs <---------------------------------------------------------------
        # Frame for the graph #1
        graph_frame = ttk.Frame(self)
        graph_frame.grid(row=0, column=0, padx=10, pady=10)

        # Creating the 2D graph #1
        fig1 = Figure(figsize=(5, 4), dpi=100)
        self.ax1 = fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=0, column=0)

        # Frame for the graph #2
        graph_frame = ttk.Frame(self)
        graph_frame.grid(row=0, column=1, padx=10, pady=10)

        # Creating the 2D graph #2
        fig2 = Figure(figsize=(5, 4), dpi=100)
        self.ax2 = fig2.add_subplot(111)
        
        self.canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=0, column=0)

        #Frame for the graph #3
        graph_frame = ttk.Frame(self)
        graph_frame.grid(row=0, column=2, padx=10, pady=10)

        # Creating the 2D graph #3
        fig3 = Figure(figsize=(5, 4), dpi=100)
        self.ax3 = fig3.add_subplot(111, projection='3d')
        self.ax3.set_xlim([-2000, 2000])
        self.ax3.set_ylim([-2000, 2000])
        self.ax3.set_zlim([-2000, 2000])

        self.canvas2 = FigureCanvasTkAgg(fig3, master=graph_frame)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=0, column=0)
        # ---------------------------------------------------------------------->

        # Frame for the recording status
        recording_frame = ttk.Frame(self)
        recording_frame.grid(row=1, column=0, padx=10, pady=10)

        recording_label = ttk.Label(recording_frame, text="Recording Status:", font=("Helvetica", 14))
        recording_label.grid(row=0, column=0)

        self.recording_text = tk.StringVar()
        self.recording_text.set("Not Recording")

        self.recording_status_label = ttk.Label(recording_frame, textvariable=self.recording_text, font=("Helvetica", 14, "bold"))
        self.recording_status_label.grid(row=0, column=1)

        # Countdown Frame
        countdown_frame = ttk.Frame(self)
        countdown_frame.grid(row=2, column=0, padx=10, pady=10)

        countdown_label = ttk.Label(countdown_frame, text="Countdown:", font=("Helvetica", 14))
        countdown_label.grid(row=0, column=0)

        self.countdown_text = tk.StringVar()
        self.countdown_text.set("0")

        countdown_value_label = ttk.Label(countdown_frame, textvariable=self.countdown_text, font=("Helvetica", 14, "bold"))
        countdown_value_label.grid(row=0, column=1)

        # Button to start the automated gesture recording
        self.start_stop_button = ttk.Button(self, text="Start Automated Recording", command=self.toggle_automated_recording)
        self.start_stop_button.grid(row=3, column=0, pady=10)

        #Error message
        error_message_frame = ttk.Frame(self)
        error_message_frame.grid(row=4, column=0, pady=10, sticky=tk.N)

        self.error_message_label = tk.Label(error_message_frame, text = "Error:", font=("Helvetica", 10))
        self.error_message_label.grid(row=0, column=0)

        self.error_message_text = tk.StringVar()
        self.error_message_text.set("None :))")

        self.error_message_value_label = ttk.Label(error_message_frame, textvariable=self.error_message_text, font=("Helvetica", 10), foreground="green")
        self.error_message_value_label.grid(row=0, column=1)

        #column 1 ------------------------------------------------------------------------------------------------------

        # Frame for the gesture
        gesture_frame = ttk.Frame(self)
        gesture_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.N)

        gesture_label = ttk.Label(gesture_frame, text="Perform Gesture:", font=("Helvetica", 14))
        gesture_label.grid(row=0, column=0)

        self.gesture_text = tk.StringVar()
        self.gesture_text.set("None")

        gesture_value_label = ttk.Label(gesture_frame, textvariable=self.gesture_text, font=("Helvetica", 14, "bold"))
        gesture_value_label.grid(row=1, column=0)

        # Frame for the current letter
        current_letter_frame = ttk.Frame(self)
        current_letter_frame.grid(row=2, column=1, padx=10, pady=10, sticky=tk.N)

        current_letter_label = ttk.Label(current_letter_frame, text="Current Letter:", font=("Helvetica", 20))
        current_letter_label.grid(row=0, column=0)

        self.current_letter_text = tk.StringVar()
        self.current_letter_text.set("")

        current_letter_value_label = ttk.Label(current_letter_frame, textvariable=self.current_letter_text, font=("Helvetica", 30, "bold"), foreground="blue")
        current_letter_value_label.grid(row=0, column=1)

        # Toggle button for the do_gestures switch
        self.do_gestures = tk.BooleanVar()
        self.do_gestures.set(True)

        toggle_do_gestures_button = ttk.Checkbutton(self, text="Perform Gestures (uncheck for sentences)", variable=self.do_gestures)
        toggle_do_gestures_button.grid(row=3, column=1, padx=10, pady=10, sticky=tk.N)

        # Toggle button for test mode (without esp)
        self.test_mode = tk.BooleanVar()
        self.test_mode.set(False)

        toggle_test_mode_button = ttk.Checkbutton(self, text="Testing Mode (without ESP)", variable=self.test_mode)
        toggle_test_mode_button.grid(row=4, column=1, padx=10, pady=10, sticky=tk.N)

        #frame for buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=5, column=1, pady=(20, 0))

        # reset button
        self.error_occured = False
        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_recording, style="Reset.TButton")
        reset_button.grid(row=0, column=0, padx=(0, 5))

        # Save button
        self.save_button = ttk.Button(button_frame, text="Save", command=self.save_recording, style="Save.TButton")
        self.save_button.grid(row=0, column=1, padx=(5, 0))

        #column 2 ------------------------------------------------------------------------------------------------------------

        # Change recording timings & repetition values & num words <----------------------------------------
        recording_time_label = ttk.Label(self, text="Recording Time (seconds):")
        recording_time_label.grid(row=1, column=2, padx=10, pady=10, sticky='e')

        self.recording_time = tk.StringVar(value=3)
        recording_time_spinbox = ttk.Spinbox(self, from_=1, to=10, textvariable=self.recording_time, wrap=True, width=5)
        recording_time_spinbox.grid(row=1, column=3, sticky="w", padx=10, pady=10)

        rest_time_label = ttk.Label(self, text="Rest Time (seconds):")
        rest_time_label.grid(row=2, column=2, sticky="e", padx=10, pady=10)

        self.rest_time = tk.StringVar(value=3)
        rest_time_spinbox = ttk.Spinbox(self, from_=1, to=10, textvariable=self.rest_time, wrap=True, width=5)
        rest_time_spinbox.grid(row=2, column=3, sticky="w", padx=10, pady=10)

        repetitions_label = ttk.Label(self, text="Repetitions / # sentances:")
        repetitions_label.grid(row=3, column=2, padx=5, pady=5, sticky="e")

        self.repetitions_var = tk.StringVar()
        self.repetitions_spinbox = ttk.Spinbox(self, from_=1, to=10000, textvariable=self.repetitions_var, width=5)
        self.repetitions_spinbox.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        self.repetitions_var.set(3)  # Default value

        numWords_label = ttk.Label(self, text="Number of words per sentance:")
        numWords_label.grid(row=4, column=2, padx=5, pady=5, sticky="e")

        self.numWords_var = tk.StringVar()
        self.numWords_spinbox = ttk.Spinbox(self, from_=1, to=10, textvariable=self.numWords_var, width=5)
        self.numWords_spinbox.grid(row=4, column=3, padx=5, pady=5, sticky="w")
        self.numWords_var.set(4)  # Default value

        # ----------------------------------------> Change recording timings & repetition values & num words



    def update_countdown(self, countdown):
        self.countdown_text.set(str(countdown))

    def change_gesture(self):
        gestures = ["Gesture 1", "Gesture 2", "Gesture 3", "Gesture 4", "Gesture 5"]
        self.gesture_text.set(random.choice(gestures))

        # Add dummy data to graph (replace this with your actual sensor data)
        self.ax.clear()
        x = range(10)
        y = [random.randint(0, 10) for _ in range(10)]
        self.ax.plot(x, y)
        self.ax.figure.canvas.draw()


    def start_automated_recording(self, stop_recording, do_gestures):
        self.recording_text.set("Starting...")
        self.update_recording_status("Starting...", "black")
        time.sleep(1)
        self.automated_recording(stop_recording, do_gestures)


    def automated_recording(self, stop_recording, do_gestures):
        repetitions = int(self.repetitions_var.get())  # Get the repetitions value
        numWords = int(self.numWords_var.get()) # Get the number of words per sentence

        recording_time = float(self.recording_time.get()) # Get the recording & rest time values
        rest_time = int(self.rest_time.get())

        if do_gestures:
            gestures = ["Gesture 1", "Gesture 2", "Gesture 3", "Gesture 4", "Gesture 5"]

            for gesture in gestures:
                if stop_recording.is_set():
                    break
                self.gesture_text.set(gesture)

                for _ in range(repetitions):
                    if stop_recording.is_set():
                        break


                    # data collection part here

                    self.message_queue.put(("update_recording_status", ("Recording", "red")))
                    collect_data_thread = threading.Thread(target=partial(SDC.collect_data, self, gesture, "temp_data.csv", recording_time, self.test_mode.get(), self.display_error)) #start collecting data here
                    collect_data_thread.start() 
                    for i in range(int(recording_time) - 1, -1, -1):
                        if stop_recording.is_set():
                            break
                        self.message_queue.put(("update_countdown", (i,)))
                        time.sleep(1)
                    collect_data_thread.join() #stop capturing data here 



                    self.message_queue.put(("update_recording_status", ("Not Recording", "black")))
                    for i in range(rest_time - 1, -1, -1):
                        if stop_recording.is_set():
                            break
                        self.message_queue.put(("update_countdown", (i,)))
                        time.sleep(1)

                self.message_queue.put(("update_recording_status", ("Changing Gesture", "orange")))
                for i in range(rest_time - 1, -1, -1):
                    if stop_recording.is_set():
                        break
                    self.message_queue.put(("update_countdown", (i,)))
                    time.sleep(1)
        else:
            for _ in range(repetitions):
                if stop_recording.is_set():
                    break

                sentence = self.get_sentence(numWords)  # don't change this to be = 1. strictly 1< words
                self.gesture_text.set(sentence)
                self.message_queue.put(("update_current_letter", (sentence[0],)))
                self.message_queue.put(("update_recording_status", ("Not Recording", "black")))

                for i in range(5, -1, -1): # reading time before recording
                        if stop_recording.is_set():
                            break
                        self.message_queue.put(("update_countdown", (i,)))
                        time.sleep(1)
                

                for idx, letter in enumerate(sentence):
                    if stop_recording.is_set():
                        break

                    self.update_current_letter(letter)


                    # data collection part here
                    self.message_queue.put(("update_recording_status", ("Recording", "red")))
                    collect_data_thread = threading.Thread(target=partial(SDC.collect_data, self, letter, "temp_data.csv", recording_time, self.test_mode.get(), self.display_error)) #start collecting data here
                    collect_data_thread.start() 
                    for i in range(int(recording_time) - 1, -1, -1):
                        if stop_recording.is_set():
                            break
                        self.message_queue.put(("update_countdown", (i,)))
                        time.sleep(1)
                    collect_data_thread.join() #stop capturing data here 



                    self.message_queue.put(("update_recording_status", ("Not Recording", "black")))
                    for i in range(rest_time - 1, -1, -1):
                        if stop_recording.is_set():
                            break
                        if i == 2:
                            # Set the next letter when the countdown is 2
                            next_letter = sentence[idx + 1] if idx + 1 < len(sentence) else ""
                            self.message_queue.put(("update_current_letter", (next_letter,)))
                        self.message_queue.put(("update_countdown", (i,)))
                        time.sleep(1)

                if _ == repetitions - 1: # if last sentence
                    break

                self.message_queue.put(("update_recording_status", ("Changing Sentence", "orange")))
                for i in range(rest_time - 1, -1, -1):
                    if stop_recording.is_set():
                        break
                    self.message_queue.put(("update_countdown", (i,)))
                    time.sleep(1)

        self.message_queue.put(("update_recording_status", ("Recording Completed", "green")))

    def update_graph(self, button_value1, button_value2):
        #graph 1 print
        self.ax1.clear()
        self.ax1.set_ylim(0, 2)
        self.ax1.set_xlim(0, 2)
        self.ax1.plot([1, 1], [0, button_value1], color="blue", linewidth=2)
        self.ax1.set_title("Button Value")
        self.canvas1.draw()

        #graph 2 print
        self.axs[0].clear()
        self.axs[0].plot(time_data, accel_magnitude, 'o-')  # plotting the magnitude of acceleration
        self.axs[0].set_ylabel('Acceleration Magnitude')



    def get_sentence(self, word_count):
        call = requests.get('https://hipsum.co/api/?type=hipster-centric&sentences=1').json()[0]
        tokens = call.split(' ')

        for i in range(len(tokens)):
            if randint(0, 2) == 0:
                tokens[i] = tokens[i].capitalize()
            elif randint(0, 5) == 0:
                tokens[i] = tokens[i].upper()
            if i < len(tokens) - 1:
                tokens[i] += ' '

        symbols = '!"#$\',-./?@'

        for i in range(len(tokens)):
            if randint(0, 4) == 0:
                if i > 0:
                    tokens[i - 1] = tokens[i - 1][:-1]
                tokens.insert(i, symbols[randint(0, len(symbols) - 1)] + ' ')

        sentence = ''.join(tokens)
        sentence = ' '.join(sentence.split()[:word_count])
        sentence = sentence.replace(' ', '_')  # replace spaces with underscores

        return sentence
    
    def update_current_letter(self, letter):
        self.current_letter_text.set(letter)


    def toggle_do_gestures(self):
        self.do_gestures.set(not self.do_gestures.get())

    def update_recording_status(self, text, color):
        self.recording_text.set(text)
        self.recording_status_label.config(foreground=color)
        self.update()

    def toggle_automated_recording(self):
        if not self.recording:
            self.recording = True
            self.stop_recording = threading.Event()
            self.recording_thread = threading.Thread(target=self.automated_recording, args=(self.stop_recording, self.do_gestures.get()))
            self.recording_thread.start()
            self.start_stop_button.config(text="Stop Automated Recording", style="Stop.TButton")
        else:
            self.recording = False
            self.stop_recording.set()
            self.recording_thread.join()
            self.start_stop_button.config(text="Start Automated Recording", style="Start.TButton")


    def start_automated_recording_thread(self):
        recording_thread = threading.Thread(target=self.start_automated_recording)
        recording_thread.start()

    def reset_recording(self): #reset everything
        self.toggle_automated_recording
        self.start_stop_button.config(text="Start Automated Recording", style="Neutral.TButton")
        self.save_button.config(style="Neutral.TButton")
        self.message_queue.put(("update_recording_status", ("Not Recording", "black")))
        self.message_queue.put(("update_countdown", ("",)))
        self.message_queue.put(("update_current_letter", ("",)))
        self.gesture_text.set("")

        # Clear the graphs
        self.ax1.cla()
        self.ax2.cla()
        self.canvas1.draw()
        self.canvas2.draw()

        # Clear the temporary file
        open("temp_data.csv", 'w').close()

        error = self.error_occured
        if not error:
            self.error_message_text.set("None :))")
            self.error_message_value_label.config(foreground="green")

    def save_recording(self): #save current record to main data
        temp_filename = "temp_data.csv"
        main_filename = "data.csv"
        self.save_button.config(style="Start.TButton")

        with open(temp_filename, 'r') as temp_file, open(main_filename, 'a') as main_file:
            temp_file.readline()
            for line in temp_file:
                main_file.write(line)

        # Clear the temporary file
        open(temp_filename, 'w').close()

    def display_error(self, error_message):
        self.error_message_text.set(error_message)
        if error_message != "None :))":
            time.sleep(1)
            self.toggle_automated_recording
            self.error_message_value_label.config(foreground="red")
            self.error_occured = True
            self.reset_recording
            self.error_occured = False
        
        


if __name__ == "__main__":
    app = GloveApp()
    app.mainloop()

