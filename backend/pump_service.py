import logging
import smbus2 as smbus

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class PumpService:


    def __init__(self, test: str):
        self.a = test
        logger.debug(f'asda')

    def number_to_bytes(self, number):
        if number < 0 or number > 65535:
            raise ValueError("Number must be between 0 and 65535 (16-bit range)")
        # Extract the two bytes using bitwise operations
        byte1 = (number >> 8) & 0xFF
        byte2 = number & 0xFF
        return [byte1, byte2]

    def run_pump(self, pump_number):
        send = [pump_number, *self.number_to_bytes(1000)]
        logger.debug(f'pump_number {send}')
        try:
            bus = smbus.SMBus(1)
            bus.write_block_data(0x04, send)
        except Exception as e:
            print(f"Error communicating with Arduino: {e}")


if __name__ == '__main__':
    a = PumpService('a')

    a.run_pump(1)
