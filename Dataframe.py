import time
import serial
import pandas as pd


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

arduino = serial.Serial('COM5', baudrate=115200, timeout=1)

# Call the handshake function
Handshake_Arduino(arduino)
time.sleep(1)


#color = ['Cyan','Yellow','Purple','White','Brown','Pink','Orange','Black','Blue','Red','Green','Gray']

color = ['Blue','Purple','Pink','Green','Yellow','Red','Brown','Orange','White','Gray','Black']


lista_r = []
lista_g = []
lista_b = []
lista_rgb = []
lista_d = []
lista_color = []

N = 100


for d in range(len(color)):
    print('Measure for color',color[d])
    input('Press Enter to continue...')
    
    for i in range(N):
        measure = Request_Measure(arduino)
        
        lista_r.append(measure[0])
        lista_g.append(measure[1])
        lista_b.append(measure[2])
        lista_rgb.append(measure[3])
        
        lista_d.append(d)
        lista_color.append(color[d])
        
        print('measure:',i,', data=',measure, ', color=', color[d])
    

print('generating data frame...')

data = {'R':lista_r,'G':lista_g,'B':lista_b,'RGB':lista_rgb,'D':lista_d,'Color':lista_color}

df = pd.DataFrame(data)
df.to_csv('df_color.csv',index=False)

print('done.')


arduino.close()
