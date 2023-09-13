import logging
import smbus2 as smbus

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class PumpService:
    ml_p_ms = 0.0045

    i2c_addr_4 = 0x04
    i2c_addr_5 = 0x05
    i2c_addr_6 = 0x06

    pump_started = 65
    pump_stopped = 66

    def number_to_bytes(self, number):
        if number < 0 or number > 65535:
            raise ValueError("Number must be between 0 and 65535 (16-bit range)")
        # Extract the two bytes using bitwise operations
        byte1 = (number >> 8) & 0xFF
        byte2 = number & 0xFF
        return [byte1, byte2]

    def calculate_ms(self, ml):
        return int(ml / self.ml_p_ms)

    def run_pump(self, pump_number, ml):
        try:
            time_bytes = self.number_to_bytes(self.calculate_ms(ml))
            bus = smbus.SMBus(1)
            bus.write_block_data(self.i2c_addr_6, 0, [self.pump_started, *time_bytes])
            if pump_number > 8:
                send = [pump_number - 8, *time_bytes]
                logger.debug(f'run_pump 5, {pump_number}: {send}')
                bus.write_block_data(self.i2c_addr_5, 0, send)
            else:
                send = [pump_number, *time_bytes]
                logger.debug(f'run_pump 4, {pump_number}: {send}')
                bus.write_block_data(self.i2c_addr_4, 0, send)
            bus.write_block_data(self.i2c_addr_6, 0, [self.pump_stopped, *time_bytes])
        except Exception as e:
            print(f"Error communicating with Arduino: {e}")


if __name__ == '__main__':
    a = PumpService()

    a.run_pump(1, 270)
