from PIL import Image, ImageDraw, ImageFont
from time import sleep

from IT8951 import constants
from IT8951.display import AutoEPDDisplay

from web3 import Web3
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

V_COM = -2.37
WEB3_POLL_INTERVAL = 1.0


class App():

    def __init__(self, web3: Web3, display):
        self.web3 = web3
        self.display = display

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http = requests.Session()
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)

    def main(self):
        logger.info('listening to new blocks...')
        new_block_filter = self.web3.eth.filter('latest')
        while True:
            block_hashes = list(new_block_filter.get_new_entries())
            if len(block_hashes) > 0:
                self.handle_block(block_hashes[-1])  # skip stale blocks because rendering might take longer
            sleep(WEB3_POLL_INTERVAL)

    def handle_block(self, block_hash):
        logger.info(f'got block: {Web3.toHex(block_hash)}')
        block_number = self.web3.eth.block_number
        logger.info(f'block number: {block_number}')
        self.render({
            'block_number': block_number,
            **self.fetch_gas_info(),
        })

    def fetch_gas_info(self):
        ret = self.http.get('https://www.gasnow.org/api/v3/gas/price').json()
        return {
            'rapid': int(float(ret['data']['rapid']) / 1e9),
            'fast': int(float(ret['data']['fast']) / 1e9),
            'standard': int(float(ret['data']['standard']) / 1e9),
            'slow': int(float(ret['data']['slow']) / 1e9),
        }

    def render(self, info):
        logger.info(f'rendering info: {info}')

        # 1448 x 1072
        self.display.frame_buf.paste(0xFF, box=(0, 0, self.display.width, self.display.height))

        self._place_text(self.display.frame_buf, 'Rapid', fontsize=120, x_offset=-543, y_offset=-402)
        self._place_text(self.display.frame_buf, 'Fast', fontsize=120, x_offset=-181, y_offset=-402)
        self._place_text(self.display.frame_buf, 'Standard', fontsize=120, x_offset=181, y_offset=-402)
        self._place_text(self.display.frame_buf, 'Slow', fontsize=120, x_offset=543, y_offset=-402)

        self._place_text(self.display.frame_buf, str(info['rapid']), fontsize=400, x_offset=-543, y_offset=-134, fill='#000')
        self._place_text(self.display.frame_buf, str(info['fast']), fontsize=400, x_offset=-181, y_offset=-134, fill='#444')
        self._place_text(self.display.frame_buf, str(info['standard']), fontsize=400, x_offset=181, y_offset=-134, fill='#888')
        self._place_text(self.display.frame_buf, str(info['slow']), fontsize=400, x_offset=543, y_offset=-134, fill='#bbb')

        self._place_text(self.display.frame_buf, 'Block Number', fontsize=120, x_offset=-362, y_offset=268)
        self._place_text(self.display.frame_buf, str(info['block_number']), fontsize=350, x_offset=300, y_offset=268)

        self.display.draw_full(constants.DisplayModes.GC16)

    # this function is just a helper for the others
    def _place_text(self, img, text, fontsize=80, x_offset=0, y_offset=0, fill='#000'):
        """
        Put some centered text at a location on the image.
        """
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('res/fonts/BmCinemaA16-9j2.ttf', fontsize)

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

    logger.info('Initializing EPD...')

    display = AutoEPDDisplay(vcom=V_COM, flip=True)
    logger.info(f'VCOM set to {display.epd.get_vcom()}')

    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/your-api-key'))
    App(web3=web3, display=display).main()
