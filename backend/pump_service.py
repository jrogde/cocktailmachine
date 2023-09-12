import logging
import smbus2 as smbus

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class PumpService:

    ml_p_ms = 0.0045


    def number_to_bytes(self, number):
        if number < 0 or number > 65535:
            raise ValueError("Number must be between 0 and 65535 (16-bit range)")
        # Extract the two bytes using bitwise operations
        byte1 = (number >> 8) & 0xFF
        byte2 = number & 0xFF
        return [byte1, byte2]

    def calculate_ms(self, ml):
        return int(ml/self.ml_p_ms)

    def run_pump(self, pump_number, ml):
        try:
            bus = smbus.SMBus(1)
            if pump_number > 8:
                send = [pump_number-8, *self.number_to_bytes(self.calculate_ms(ml))]
                logger.debug(f'run_pump 5, {pump_number}: {send}')
                bus.write_block_data(0x05, 0, send)
            else:
                send = [pump_number, *self.number_to_bytes(self.calculate_ms(ml))]
                logger.debug(f'run_pump 4, {pump_number}: {send}')
                bus.write_block_data(0x04, 0, send)
        except Exception as e:
            print(f"Error communicating with Arduino: {e}")


if __name__ == '__main__':
    a = PumpService()

    a.run_pump(1,270)
