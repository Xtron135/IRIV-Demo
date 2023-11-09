from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import time

client = ModbusSerialClient(port="/dev/ttyACM0",
                          method="rtu",
                          baudrate=9600,
                          stopbits=1,
                          bytesize=8,
                          parity='N',
                          timeout=1)

connection = client.connect()
if connection:
    print("Connected.")

while True:
    #Starting add, num of reg to read, slave unit.
    #Address 0, Read Humidit
    resp = client.read_holding_registers(0x000B,1,1)
    registers = resp.registers[0:1]
    Decoder = BinaryPayloadDecoder.fromRegisters(registers, Endian.BIG, wordorder=Endian.LITTLE)
    encoding = '16bit_int'
    result = getattr(Decoder,f"decode_{encoding}")()
    result = result / 10
    
    #Address 1, Read Temperature
    # resp2 = client.read_holding_registers(0x001,1,3)
    # registers2 = resp2.registers[0:1]
    # Decoder2 = BinaryPayloadDecoder.fromRegisters(registers2, Endian.Big, wordorder=Endian.Little)
    # encoding = '16bit_int'
    # result2 = getattr(Decoder2,f"decode_{encoding}")()
    # result2 = result2 / 10
    
    print(result)
    # print(result2)
    # print(str(result) + '\t' + str(result2))

    time.sleep(1)

#Closes the underlying socket connection
client.close()
