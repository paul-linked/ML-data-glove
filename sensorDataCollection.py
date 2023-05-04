import csv
import time
import serial


SERIAL_PORT = '/dev/ttyUSB0'

def connect_to_esp():
    global ser
    ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
    ser.flush()

def read_sensor_data():
    # Add code here to read sensor data from the ESP and return it as a dictionary
    # Example: {'hall_1': 0.0, 'hall_2': 0.0, 'hall_3': 0.0, 'hall_4': 0.0, 'hall_5': 0.0, 'mpu_x': 0.0, 'mpu_y': 0.0, 'mpu_z': 0.0}
    pass

def read_button_state():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
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

def collect_data(letter, filename, duration):
    connect_to_esp()

    start_time = time.time()

    while time.time() - start_time < duration:
        button_state = read_button_state()

        if button_state is not None:
            sensor_data = read_sensor_data()
            sensor_data = sensor_data if sensor_data else {}  
            sensor_data['button'] = button_state
            sensor_data['letter'] = letter
            save_data_to_csv(filename, sensor_data)

        time.sleep(0.01)  # Adjust the delay based on your requirements

