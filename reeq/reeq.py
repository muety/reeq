import json
import logging
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, Future
from threading import Thread
from typing import Any, List, Tuple, Callable, Set, Dict, Optional

import redis
from redis.client import PubSub
from redis.exceptions import ConnectionError as RedisConnectionError

ListenCallback = Callable[[str, Any], None]

logger = logging.getLogger('reeq')
logger.setLevel(logging.INFO)

valid_pattern = re.compile('^[\w\d]+(?:\\.[\w\d]+)*(?:\\.\\*)?$')


class Reeq:
    def __init__(self) -> None:
        super().__init__()
        self._redis: redis.Redis = None
        self._pubsub: PubSub = None
        self._executor: ThreadPoolExecutor = None
        self._listeners: List[Tuple[str, ListenCallback]] = []  # TODO: use more efficient data structure
        self._active_subscriptions: Set[str] = set()
        self._receiver: Optional[Thread] = None

    def init(self, redis_url: str, workers: int = os.cpu_count()):
        if self._pubsub is not None:
            return  # already initalized

        self._redis: redis.Redis = redis.from_url(redis_url, decode_responses=True)
        self._redis.ping()

        self._pubsub: PubSub = self._redis.pubsub()
        self._executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=workers)

        # start all subscriptions created before init()
        for listener in self._listeners:
            self._subscribe_channel(listener[0])

        self._start_receive()

    def publish(self, event: str, payload: Any) -> int:
        return self._redis.publish(event, payload)

    def listen(self, pattern: str, callback: ListenCallback):
        if not valid_pattern.match(pattern):
            raise Exception('invalid pattern')

        self._listeners.append((pattern, callback))

        if self._pubsub is not None:  # post init()
            self._subscribe_channel(pattern)

    def unlisten(self, callback: ListenCallback):
        self._listeners = [l for l in self._listeners if l[1] != callback]
        # TODO: unsubscribe from channels, if no more active listeners for prefix

    def listener(self, pattern: str):
        def inner(func):
            self.listen(pattern, func)
            return func

        return inner

    def _subscribe_channel(self, pattern: str):
        parts: List[str] = pattern.removesuffix('.*').split('.')
        if (prefix := parts[0]) not in self._active_subscriptions:
            subpattern: str = prefix if len(parts) == 1 else f'{prefix}.*'
            self._pubsub.psubscribe(subpattern)
            self._active_subscriptions.add(prefix)

    def _start_receive(self):
        def receiver():
            while True:
                try:
                    message: Dict[str, Any] = self._pubsub.get_message(ignore_subscribe_messages=True, timeout=5.)
                    if message is not None:
                        event_name: str = message['channel']
                        event_payload: Dict[str, Any] = json.loads(message['data'])
                        self._dispatch(event_name, event_payload)

                except RedisConnectionError as e:
                    logger.warning('got redis connection error, continuing ...')
                    time.sleep(1.)

                except Exception as e:
                    logging.exception(e)

        self._receiver = Thread(target=receiver, args=(), daemon=True)
        self._receiver.start()

    def _dispatch(self, event: str, payload: Any):
        for listener in self._listeners:
            pattern, callback = listener
            if event == pattern or (pattern[-1] == '*' and event.startswith(pattern[:-1])):
                future: Future[Any] = self._executor.submit(callback, event, payload)
                try:
                    future.result()  # TODO: allow to have multiple listeners process the same event simultaneously
                except Exception as e:
                    raise e


reeq = Reeq()
