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
    #client.read_holding_registers(Register Address, Register to Read, Unit ID)
    #Register Address 0 @ 0x000, Read Humidity
    resp = client.read_holding_registers(0x000,1,1)
    registers = resp.registers[0:1]
    Decoder = BinaryPayloadDecoder.fromRegisters(registers, Endian.BIG, wordorder=Endian.LITTLE)
    encoding = '16bit_int'
    result = getattr(Decoder,f"decode_{encoding}")()
    result = result / 10
    
    #Register Address 1 @ 0x001, Read Temperature
    resp2 = client.read_holding_registers(0x001,1,1)
    registers2 = resp2.registers[0:1]
    Decoder2 = BinaryPayloadDecoder.fromRegisters(registers2, Endian.BIG, wordorder=Endian.LITTLE)
    encoding = '16bit_int'
    result2 = getattr(Decoder2,f"decode_{encoding}")()
    result2 = result2 / 10
    
    # print(result)
    # print(result2)
    print(str(result) + '\t' + str(result2))

    time.sleep(1)

#Closes the underlying socket connection
client.close()
