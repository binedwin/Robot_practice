from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging # LOG로 오류 체크

### 로그 보는거 필수아님
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
### 로그 끝

# 1 =세그먼트 값
# 2,3,4= LED 값
# 5= 상태값
aa = [1,2,3,4,5]

unit1 = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [0]),
    co = ModbusSequentialDataBlock(0, [0]),
    ir = ModbusSequentialDataBlock(0, [0]),
    hr = ModbusSequentialDataBlock(0, aa),
)

context = ModbusServerContext(slaves={1 : unit1}, single=False)
StartTcpServer(context, address = ("192.168.27.60", 502))