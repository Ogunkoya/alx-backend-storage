#!/usr/bin/env python3
import requests
from typing import Callable
from functools import wraps
import redis

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Function as 
    Decortator for counting 
    """
    @wraps(method)
    def wrapper(url):  # sourcery skip: use-named-expression
        """ Wrapper for decorator """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        web_html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return web_html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Function to obtain the 
    HTML content of a  URL 
    """
    requst = requests.get(url)
    return requst.text