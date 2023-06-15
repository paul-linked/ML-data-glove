import csv
import time
import serial
import random
import numpy as np


SERIAL_PORT = '/dev/ttyUSB0'

accel_data = [[], [], []]
accel_magnitude = []  # This list will store acceleration magnitude
gyro_data = [[], [], []]
time_data = []

start_time = time.time()

# Set the duration for data display (in seconds).
display_duration = 50  # This can be adjusted

def connect_to_esp(display_error):
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, 9600)
        ser.flush()
    except serial.SerialException as e:
        print(e)
        display_error("Failed to connect to ESP. Is it connected to the computer?")
        exit(1)

def parse_data(data_str):
    # Parse the data from the serial port.
    print(f"Raw data: {data_str}")  # Debug line
    data = data_str.strip().split(', ')
    try:
        accel_x = float(data[0].split(': ')[1]) 
        accel_y = float(data[1].split(': ')[1]) 
        accel_z = float(data[2].split(': ')[1])  
        gyro_x = float(data[3].split(': ')[1])
        gyro_y = float(data[4].split(': ')[1])
        gyro_z = float(data[5].split(': ')[1])
    except IndexError:
        print(f"Failed to parse data: {data}")
        return None  # Return None or some default values if parsing failed

    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z
    

def read_sensor_data():
    # Add code here to read sensor data from the ESP and return it as a dictionary
    # Example: {'hall_1': 0.0, 'hall_2': 0.0, 'hall_3': 0.0, 'hall_4': 0.0, 'hall_5': 0.0, 'mpu_x': 0.0, 'mpu_y': 0.0, 'mpu_z': 0.0}
    if ser.in_waiting:
            data_str = ser.readline().decode('utf-8', 'ignore')
            parsed_data = parse_data(data_str)
            if parsed_data is None:  # Skip this iteration if parsing failed
                pass

            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = parsed_data

            # Append the data.
            accel_data[0].append(accel_x)
            accel_data[1].append(accel_y)
            accel_data[2].append(accel_z)
            accel_magnitude.append(np.sqrt(accel_x**2 + accel_y**2 + accel_z**2))  # append magnitude to list
            gyro_data[0].append(gyro_x)
            gyro_data[1].append(gyro_y)
            gyro_data[2].append(gyro_z)
            time_data.append(time.time() - start_time)

            if len(time_data) > display_duration:
                accel_data[0] = accel_data[0][-display_duration:]
                accel_data[1] = accel_data[1][-display_duration:]
                accel_data[2] = accel_data[2][-display_duration:]
                accel_magnitude = accel_magnitude[-display_duration:]
                gyro_data[0] = gyro_data[0][-display_duration:]
                gyro_data[1] = gyro_data[1][-display_duration:]
                gyro_data[2] = gyro_data[2][-display_duration:]
                time_data = time_data[-display_duration:]
            
            return {'mpu_x': accel_x, 'mpu_y': accel_y, 'mpu_z': accel_z, 'gyro_x': gyro_x, 'gyro_y': gyro_y, 'gyro_z': gyro_z}
    else:
        return None
    

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
            MPUSensor_data = read_sensor_data() # Read sensor data from the ESP

            if MPUSensor_data is not None:
                button_state2 = random.choice([0, 1])
                sensor_data = sensor_data if sensor_data else {}  
                self.message_queue.put(("update_graph", (MPUSensor_data,), (button_state2,)))
                sensor_data['values'] = MPUSensor_data
                sensor_data['letter'] = letter
                save_data_to_csv(filename, sensor_data)

        else:
            MPUReading = {'mpu_x': random.randint(-1000, 1000), 'mpu_y': random.randint(-1000, 1000), 'mpu_z': random.randint(-1000, 1000), 'gyro_x': random.randint(-1000, 1000), 'gyro_y': random.randint(-1000, 1000), 'gyro_z': random.randint(-1000, 1000)}
            button_state1 = random.choice([0, 1])
            self.message_queue.put(("update_graph", (MPUReading,), (button_state1,)))
            time.sleep(1)

        time.sleep(0.01)  # Adjust the delay based on your requirements

# def update_graph(self, button_value):
#     self.message_queue.put(("update_graph", (button_value,)))


