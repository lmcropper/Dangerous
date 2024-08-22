import serial
import time

# Set up the serial connection
port = '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0'
baudrate = 115200

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Connected to {port} at {baudrate} baudrate.")
    
    # Example command to send (replace with your actual command)
    command = b'Your Command Here\r\n'

    # Send the command
    ser.write(command)
    print(f"Sent command: {command.decode('utf-8').strip()}")

except serial.SerialException as e:
    print(f"Error connecting to {port}: {e}")
finally:
    if ser.is_open:
        ser.close()
        print(f"Connection to {port} closed.")
