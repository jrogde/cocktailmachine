import logging

import smbus2 as smbus

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class ArduinoService:
    i2c_addr_4 = 0x04
    i2c_addr_5 = 0x05
    i2c_addr_6 = 0x06

    def __init__(self):
        run = True
        ant = 0
        while run:
            ant = ant + 1
            try:
                self.bus = smbus.SMBus(1)
            except Exception as e:
                if ant > 9:
                    logging.error(f"Error creating communicating with Arduino: {e}")
                    run = False
            else:
                run = False

    def write_block_data(self, addr, data):
        run = True
        ant = 0
        while run:
            ant = ant + 1
            try:
                self.bus.write_block_data(addr, 0, data)
            except Exception as e:
                if ant > 9:
                    logging.error(f"Error communicating with Arduino: {e}")
                    run = False
            else:
                run = False


if __name__ == '__main__':
    a = ArduinoService()
    a.write_block_data(a.i2c_addr_6, "aa")
