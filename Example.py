import time
import serial


HANDSHAKE = 0
MEASURE_REQUEST = 1


""" Make sure connection is established by sending and receiving bytes. """
def Handshake_Arduino (arduino):   
    # Chill out while everything gets set
    time.sleep(1)

    # Set a long timeout to complete handshake
    timeout = arduino.timeout
    arduino.timeout = 2

    # Read and discard everything that may be in the input buffer
    _ = arduino.read_all()

    # Send request to Arduino
    arduino.write(bytes([HANDSHAKE]))

    # Read in what Arduino sent
    handshake_message = arduino.read_until()

    # Print the handshake message, if desired
    print("Handshake message: " + handshake_message.decode())

    # Reset the timeout
    arduino.timeout = timeout


""" Ask Arduino for a measure. """
def Request_Measure(arduino):
    # Read and discard everything that may be in the input buffer
    _ = arduino.read_all()
    
    # Ask Arduino for data
    arduino.write(bytes([MEASURE_REQUEST]))

    # Read in the data
    raw = arduino.read_until()
    raw = raw.decode()
    
    R, G, B, RGB = raw.rstrip().split(",")

    measure = [int(R), int(G), int(B), int(RGB)]

    return measure 


"""""""""""""""""""""""""""""""""""""""""""""""""""""
""""                 MAIN                        """"
"""""""""""""""""""""""""""""""""""""""""""""""""""""

arduino = serial.Serial('COM7', baudrate=115200, timeout=1)

# Call the handshake function
Handshake_Arduino(arduino)
time.sleep(1)


# Request measure
for _ in range(100):
    measure = Request_Measure(arduino)
    
    
    
    print(measure)


arduino.close()
