import logging

import requests


class Request:
    def __init__(
        self,
        base_url: str = "localhost",
        port: int = 8080,
        parameters: dict = {},
        headers: dict = {},
        path_segments: list = [],
    ):
        self.base_url = base_url
        self.parameters = parameters
        self.headers = headers
        self.path_segments = path_segments

    def __repr__(self) -> str:
        return f"<RestApi base_url={self.base_url}, \
                    parameters={self.parameters}, \
                    header={self.headers}, \
                    path_segments={self.path_segments}>"

    def get_response(self):
        from furl import furl

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
