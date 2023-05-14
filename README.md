# reeq

aka. **Re**dis **E**vent **Q**ueue

An extremely simple, minimalistic library for handling events published to Redis.

## Limitations
Reeq currently uses [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/), where messages are delivered following _at-most-once_ semantics. That is, messages will get lost while your subscriber is offline, which is not an optimal behavior for the use cases that reeq is targeting. Instead, we might want to switch to [Redis Streams](https://redis.io/docs/data-types/streams-tutorial/) with _consumer groups_ instead, which provide persistent messages.

## Comparison
You might ask how reeq compares to tools such as [rq](https://python-rq.org/) or [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html). Reeq is way more lightweight, a bit more "low-level", but also way less capable. Reeq essentially only provides an event bus on top of Redis, while the aforementioned tools cover serialization, scheduling, task chaining, message retrial and a lot more. Another difference is the fact that job / task queues like rq or Celery usually impose "uni-directional" message flow, from your application to the workers, while reeq is built for use cases that require bi-directional communication between two "coequal" programs.

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

## License

MIT
