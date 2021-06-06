from PIL import Image, ImageDraw, ImageFont

from IT8951 import constants
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

        logger.info('clearing display...')
        display.clear()

        # clear image to white
        display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

        logger.info('writing full...')
        self._place_text(display.frame_buf, 'partial', x_offset=-200)
        display.draw_full(constants.DisplayModes.GC16)

        # TODO: should use 1bpp for partial text update
        logger.info('writing partial...')
        self._place_text(display.frame_buf, 'update', x_offset=+200)
        display.draw_partial(constants.DisplayModes.DU)

        logger.info('clearing display...')
        display.clear()

    # this function is just a helper for the others
    def _place_text(self, img, text, x_offset=0, y_offset=0):
        """
        Put some centered text at a location on the image.
        """
        fontsize = 80

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontsize)

        img_width, img_height = img.size
        text_width, _ = font.getsize(text)
        text_height = fontsize

        draw_x = (img_width - text_width)//2 + x_offset
        draw_y = (img_height - text_height)//2 + y_offset

        draw.text((draw_x, draw_y), text, font=font)


if __name__ == '__main__':

    import sys

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)-8s %(message)s',
        level=logging.INFO,
        stream=sys.stdout,
    )

    App().main()
