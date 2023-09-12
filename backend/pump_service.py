import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class PumpService:


    def __init__(self, test: str):
        self.a = test
        logger.debug(f'asda')

    def run_it(self, ):
        logger.info(f'a: {self.a}')


if __name__ == '__main__':
    a = PumpService('a')
    a.run_it()
