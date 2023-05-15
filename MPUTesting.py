import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import numpy as np

# Create the serial connection.
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Initialize lists to store the data.
accel_data = [[], [], []]
accel_magnitude = []  # This list will store acceleration magnitude
gyro_data = [[], [], []]
time_data = []

start_time = time.time()

# Create the plot for accelerometer data.
fig, axs = plt.subplots(2)
fig.suptitle('Accelerometer and Gyroscope Data')

# Create the plot for gyroscope data.
ax = fig.add_subplot(212, projection='3d')
ax.set_x([-2000, 2000])
ax.set_y([-2000, 2000])
ax.set_z([-2000, 2000])

# Set the duration for data display (in seconds).
display_duration = 50  # This can be adjusted

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

try:
    while True:
        if ser.in_waiting:
            data_str = ser.readline().decode('utf-8', 'ignore')
            parsed_data = parse_data(data_str)
            if parsed_data is None:  # Skip this iteration if parsing failed
                continue

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

            # If data lists are longer than display_duration, truncate them.
            if len(time_data) > display_duration:
                accel_data[0] = accel_data[0][-display_duration:]
                accel_data[1] = accel_data[1][-display_duration:]
                accel_data[2] = accel_data[2][-display_duration:]
                accel_magnitude = accel_magnitude[-display_duration:]
                gyro_data[0] = gyro_data[0][-display_duration:]
                gyro_data[1] = gyro_data[1][-display_duration:]
                gyro_data[2] = gyro_data[2][-display_duration:]
                time_data = time_data[-display_duration:]

            # Update the accelerometer plot.
            axs[0].clear()
            axs[0].plot(time_data, accel_magnitude, 'o-')  # plotting the magnitude of acceleration
            axs[0].set_ylabel('Acceleration Magnitude')

            # Update the gyroscope plot.
            ax.clear()
            ax.quiver(gyro_data[0], gyro_data[1], gyro_data[2], gyro_data[0], gyro_data[1], gyro_data[2])
            ax.set_xlabel('Gyro X')
            ax.set_ylabel('Gyro Y')
            ax.set_zlabel('Gyro Z')

            # Pause to allow the plots to update.
            plt.pause(0.01)

except KeyboardInterrupt:
    # Close the serial connection.
    ser.close()
