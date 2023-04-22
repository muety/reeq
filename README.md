# reeq

aka. **Re**dis **E**vent **Q**ueue

An extremely simple, minimalistic library for handling events published to Redis.

## Installation

```bash
pip install git+https://github.com/muety/reeq.git
```

## Usage

```python
from reeq import reeq


# listen for event wildcard
@reeq.listener('foo.bar.*')
def handle1(event: str, payload: Dict[str, Any]):
    logging.info(f'[1] Got event "{event}" with payload: {payload}')


# listen for specific event
@reeq.listener('foo.bar.baz')
def handle2(event: str, payload: Dict[str, Any]):
    logging.info(f'[2] Got event "{event}" with payload: {payload}')


if __name__ == '__main__':
    reeq.init('redis://localhost')

    # publish event
    reeq.publish('foo.bar.baz', '{"value": 1}')
```

## To Do

* [ ] Add `pyproject.toml`

## License

MIT