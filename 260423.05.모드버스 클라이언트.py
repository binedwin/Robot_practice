from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("192.168.27.60", port = 502)
client.connect()

def get_sig(num):

    result = client.read_holding_registers(address = num, count = 1, slave = 1)
    print(f"서버에서 읽어온 값은 : {result.registers[0]}")
    client.close()

def set_sig(num1, num2):
    client.write_register(address=num1, value=num2, slave =1)


set_sig(2, 65535)
get_sig(3)