import logging
from arduino_service import ArduinoService

logger = logging.getLogger(__name__)
logging.basicConfig(filename='cocktailmachine.log', encoding='utf-8', level=logging.DEBUG)


class PumpService:

    ml_p_ms = 0.0045
    pump_started = 65

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
        arduino_service = ArduinoService()
        time_bytes = self.number_to_bytes(self.calculate_ms(ml))
        arduino_service.write_block_data(arduino_service.i2c_addr_6, [self.pump_started, *time_bytes])

        if pump_number > 8:
            send = [pump_number - 8, *time_bytes]
            logger.debug(f'run_pump 5, {pump_number}: {send}')
            arduino_service.write_block_data(arduino_service.i2c_addr_5, send)
        else:
            send = [pump_number, *time_bytes]
            logger.debug(f'run_pump 4, {pump_number}: {send}')
            arduino_service.write_block_data(arduino_service.i2c_addr_4, send)



if __name__ == '__main__':
    a = PumpService()

    a.run_pump(1, 270)
