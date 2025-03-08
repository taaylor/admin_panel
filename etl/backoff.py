import functools
import logging
import random
import time
from typing import Callable, Tuple, Type


def backoff(
    exception: Tuple[Type[Exception], ...] = Exception,
    start_sleep_time: float = 0.1,
    factor: float = 2,
    border_sleep_time: float = 10,
    jitter: bool = True,
) -> Callable:
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    """

    def func_wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            t = start_sleep_time
            attempt = 1
            while attempt < 10:
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    logging.warning(
                        f"Возникло исключение на стороне сервиса: '{e}'. Попытка #{attempt}"
                    )
                except Exception as e:
                    logging.warning(f"Возникло исключение: '{e}'. Попытка #{attempt}")
                if jitter:
                    t += random.uniform(0, t * 0.1)
                attempt += 1
                time.sleep(t)
                t = min(t * factor, border_sleep_time)
            logging.error(
                "ETL перкратил свою работу, из-за превышения попыток подключения"
            )

        return inner

    return func_wrapper
