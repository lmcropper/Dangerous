import serial
import time

# Configure the serial connection
port = '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0'
baudrate = 115200

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Connected to {port} at {baudrate} baud")

    time.sleep(3)
    # Send a command
    command = '100\n'  # Replace with your command
    #ser.write(command.encode())
    #print(f"Sent command: {command.decode().strip()}")

    # Optionally, read a response
    #response = ser.readline()
    #print(f"Received: {response.decode().strip()}")

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    if ser.is_open:
        ser.close()
        print("Serial connection closed.")


