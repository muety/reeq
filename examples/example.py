import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)

from reeq import reeq


@reeq.listener('foo.bar.*')
def handle1(event: str, payload: Dict[str, Any]):
    logging.info(f'[1] Got event "{event}" with payload:\n{payload}')


@reeq.listener('foo.bar.baz')
def handle1(event: str, payload: Dict[str, Any]):
    logging.info(f'[1] Got event "{event}" with payload:\n{payload}')


if __name__ == '__main__':
    reeq.init('redis://localhost')
    reeq.publish('foo.bar.baz', '{"value": 1}')
    input()
