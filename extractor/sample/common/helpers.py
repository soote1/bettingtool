import importlib
import json
from multiprocessing import get_logger

import requests
from bs4 import BeautifulSoup

class RequestsHelper:
    """
    Basic wrapper for requests library
    """
    def __init__(self, *args):
        self.logger = get_logger()

    def get(self, url):
        self.logger.info(f"performing GET request to {url}")
        return requests.get(url)

class HtmlParserHelper:
    def __init__(self, *args):
        self.logger = get_logger()
    
    def create_html_object(self, html_str, html_parser):
        self.logger.info(f"creating html object using {html_parser} parser")
        return BeautifulSoup(html_str, html_parser)