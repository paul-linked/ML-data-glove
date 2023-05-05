import csv
import time
import serial
import random



SERIAL_PORT = '/dev/ttyUSB0'

def connect_to_esp(display_error):
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
        ser.flush()
    except serial.SerialException as e:
        print(e)
        display_error("Failed to connect to ESP. Is it connected to the computer?")
        exit(1)
    

def read_sensor_data():
    # Add code here to read sensor data from the ESP and return it as a dictionary
    # Example: {'hall_1': 0.0, 'hall_2': 0.0, 'hall_3': 0.0, 'hall_4': 0.0, 'hall_5': 0.0, 'mpu_x': 0.0, 'mpu_y': 0.0, 'mpu_z': 0.0}
    pass

def read_button_state():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if int(line) not in [0, 1]:
            return None
        button_state = int(line)
        return button_state
    else:
        return None

def save_data_to_csv(filename, data):
    fieldnames = list(data.keys())
    file_exists = False

    try:
        with open(filename, 'r', newline='') as csvfile:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

def collect_data(self, letter, filename, duration, test_mode, display_error):
    if not test_mode:
        connect_to_esp(display_error)
    

    start_time = time.time()

    while time.time() - start_time < duration:
        if not test_mode:
            button_state = read_button_state()

            if button_state is not None:
                sensor_data = read_sensor_data() # this line does not do antrhing now. probs cursed idk
                button_state2 = random.choice([0, 1])
                sensor_data = sensor_data if sensor_data else {}  
                self.message_queue.put(("update_graph", (button_state,), (button_state2,)))
                sensor_data['button'] = button_state
                sensor_data['letter'] = letter
                save_data_to_csv(filename, sensor_data)

        else:
            button_state1 = random.choice([0, 1])
            button_state2 = random.choice([0, 1])
            
            self.message_queue.put(("update_graph", (button_state1,), (button_state2,)))
            time.sleep(1)

        time.sleep(0.01)  # Adjust the delay based on your requirements

def update_graph(self, button_value):
    self.message_queue.put(("update_graph", (button_value,)))


