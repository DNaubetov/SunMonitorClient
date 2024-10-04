from decimal import Decimal
from pymodbus.client import ModbusTcpClient
from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian


class ModbusAPP:
    def __init__(self, connect, serial_number, slave, read_dict: dict):
        self.connect = connect
        self.serial_number = serial_number
        self.slave = slave
        self.registers_dict = read_dict
        self.decoders = BinaryPayloadDecoder.fromRegisters

    def __decode_registers(self, registers, count):
        res = self.decoders(registers, byteorder=Endian.BIG, wordorder=Endian.BIG if count < 10 else Endian.LITTLE)
        decode_bit = {1: res.decode_16bit_uint,
                      2: res.decode_32bit_uint,
                      4: res.decode_64bit_uint,
                      11: res.decode_16bit_int,
                      12: res.decode_32bit_int,
                      14: res.decode_64bit_int,
                      21: res.decode_16bit_float,
                      22: res.decode_32bit_float,
                      24: res.decode_64bit_float,
                      31: res.decode_string}
        return decode_bit[count]

    def read_registers(self, name: str):
        try:
            register: bool | dict = self.registers_dict.get(name, False)
            if register is False:
                return

            registers_functions = {3: self.connect.read_holding_registers, 4: self.connect.read_input_registers}

            register_function = registers_functions[register["function"]]
            data = register_function(address=register["address"],
                                     count=register["count"] % 10,
                                     slave=self.slave)

            decode = self.__decode_registers(data.registers, register["count"])

            if register.get('coefficient', False):
                return {'data': str(round(Decimal(str(decode())) * Decimal(register["coefficient"]), 2)),
                        'unit': register["unit"]}

            return {'data': str(decode())}
        except Exception as e:
            return e

    def read_all_registers(self):
        reg = {name: self.read_registers(name) for name in self.registers_dict.keys()}
        data = {'serial_number': self.serial_number, "inverter_registers_data": reg}
        return data
