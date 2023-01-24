import logging

import backoff
import requests
from furl import furl


class Request:
    def __init__(
        self,
        base_url="localhost",
        port=8080,
        parameters=None,
        headers=None,
        path_segments=None,
    ):
        self.base_url = base_url
        if parameters is None:
            parameters = {}
        self.parameters = parameters
        if headers is None:
            headers = {}
        self.headers = headers
        if path_segments is None:
            path_segments = []
        self.path_segments = path_segments

    def __repr__(self):
        return f"<RestApi base_url={self.base_url}, \
                    parameters={self.parameters}, \
                    header={self.headers}, \
                    path_segments={self.path_segments}>"

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.RequestException, requests.exceptions.HTTPError),
        max_time=60,
        max_tries=3,
    )
    def get_response(self):
        url_base_obj = furl(self.base_url)
        url_base_obj.path.segments = self.path_segments
        url_base_obj.add(self.parameters)
        logging.debug(url_base_obj.url)
        response = requests.get(url_base_obj.url, headers=self.headers)
        response.raise_for_status()
        return response

    def get_response_bytes(self):
        response = self.get_response()
        return response.content

    def get_response_json(self):
        response = self.get_response()
        return response.json()

    def get_response_xml(self):
        response = self.get_response()
        return response.content

    def get_parameters(self):
        parameters = {
            "base_url": self.base_url,
            "parameters": self.parameters,
        }

        if bool(self.headers):
            parameters["headers"] = self.headers
        return parameters
