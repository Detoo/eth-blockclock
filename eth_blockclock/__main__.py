from IT8951.display import AutoEPDDisplay

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

V_COM = -2.37


class App():

    def main(self):
        logger.info('Initializing EPD...')

        display = AutoEPDDisplay(vcom=V_COM)
        logger.info(f'VCOM set to {display.epd.get_vcom()}')


if __name__ == '__main__':

    import sys

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)-8s %(message)s',
        level=logging.INFO,
        stream=sys.stdout,
    )

    App().main()
