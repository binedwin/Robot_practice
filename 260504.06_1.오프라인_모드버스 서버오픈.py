from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging

#LOG 출력으로 오류 체크
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
##오류가 있으면 로그로 출력이 되요
##어떤 오류인지 확인할 수 있습니다.
'''
di = Discrete input (읽기 전용 0 | 1)
co = Coils (읽기, 쓰기 0 | 1)
in = input registers (읽기 | 0~65535)
hr = holding registers (읽기, 쓰기 | 0~65535)
'''

store_unint = ModbusSlaveContext(
  di = ModbusSequentialDataBlock(0, [0]*100),
  co = ModbusSequentialDataBlock(0, [0]*100),
  ir = ModbusSequentialDataBlock(0, [0]*100),
  hr = ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves={1: store_unint}, single=False)
StartTcpServer(context=context, address = ("127.0.0.1", 5020))