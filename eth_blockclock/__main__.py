from PIL import Image, ImageDraw, ImageFont
from time import sleep

from IT8951 import constants
from IT8951.display import AutoEPDDisplay

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

V_COM = -2.37


class App():

    def main(self):
        logger.info('Initializing EPD...')

        display = AutoEPDDisplay(vcom=V_COM, flip=True)
        logger.info(f'VCOM set to {display.epd.get_vcom()}')

        # 1448 x 1072
        logger.info('rendering texts...')
        display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

        self._place_text(display.frame_buf, 'Rapid', fontsize=80, x_offset=-543, y_offset=-402)
        self._place_text(display.frame_buf, 'Fast', fontsize=80, x_offset=-181, y_offset=-402)
        self._place_text(display.frame_buf, 'Standard', fontsize=80, x_offset=181, y_offset=-402)
        self._place_text(display.frame_buf, 'Slow', fontsize=80, x_offset=543, y_offset=-402)

        self._place_text(display.frame_buf, '29', fontsize=160, x_offset=-543, y_offset=-134, fill='#000')
        self._place_text(display.frame_buf, '23', fontsize=160, x_offset=-181, y_offset=-134, fill='#444')
        self._place_text(display.frame_buf, '21', fontsize=160, x_offset=181, y_offset=-134, fill='#888')
        self._place_text(display.frame_buf, '21', fontsize=160, x_offset=543, y_offset=-134, fill='#bbb')

        self._place_text(display.frame_buf, 'Block Number:', fontsize=80, x_offset=-268, y_offset=268)
        self._place_text(display.frame_buf, '12578633', fontsize=120, x_offset=300, y_offset=268)

        display.draw_full(constants.DisplayModes.GC16)

    # this function is just a helper for the others
    def _place_text(self, img, text, fontsize=80, x_offset=0, y_offset=0, fill='#000'):
        """
        Put some centered text at a location on the image.
        """
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontsize)

        img_width, img_height = img.size
        text_width, _ = font.getsize(text)
        text_height = fontsize

        draw_x = (img_width - text_width)//2 + x_offset
        draw_y = (img_height - text_height)//2 + y_offset

        draw.text((draw_x, draw_y), text, font=font, fill=fill)


if __name__ == '__main__':

    import sys

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)-8s %(message)s',
        level=logging.INFO,
        stream=sys.stdout,
    )

    App().main()
