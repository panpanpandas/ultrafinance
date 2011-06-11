''' ultraFinance lib '''
import logging
LOG = logging.getLogger(__name__)

import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)-5.5s [%(name)s] [%(threadName)s] %(message)s',
                    filename=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ultraFinance.log'),
                    filemode='w')
