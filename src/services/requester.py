import logging
import time

import requests
import urllib3
from requests.exceptions import RequestException, RetryError

from src.config import get_settings

urllib3.disable_warnings()

logger = logging.getLogger(__name__)
settings = get_settings()


class Requester:
    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()
        self.max_retries = settings.REQUESTS_RETRY_MAX
        self.retry_delay = settings.REQUESTS_RETRY_DELAY
        self.status_retry = [429, 500, 502, 503, 504]

    def __prepare_request(self, method: str, endpoint: str, **kwargs) -> requests.PreparedRequest:
        prepped = requests.Request(
            method=method,
            url=self.url + endpoint,
            **kwargs,
        ).prepare()

        logger.debug(
            "request",
            extra={"method": prepped.method, "url": prepped.url, "body": prepped.body},
        )

        return prepped

    def __should_retry(self, response: requests.Response) -> bool:
        try:
            json_data = response.json()
            if response.status_code in self.status_retry or int(json_data.get("status")) in self.status_retry:
                return True

        except ValueError:
            logger.error("Payload is not a json")

        return False

    def sleep_retry(self, attempt: int, response: requests.Response = None):
        wait_time = self.retry_delay * (2**attempt)

        extra = None
        if response:
            extra = {"status_code": response.status_code, "text": response.text}

        logger.warning(f"Waiting for {wait_time:.2f} seconds before retrying...", extra=extra)
        time.sleep(wait_time)

    def __submit_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        attempt = 0
        while attempt < self.max_retries:
            try:
                prepped = self.__prepare_request(method, endpoint, **kwargs)

                response = self.session.send(
                    prepped,
                    timeout=settings.REQUESTS_TIMEOUT,
                    allow_redirects=settings.REQUESTS_ALLOW_REDIRECTS,
                    verify=settings.REQUESTS_VERIFY,
                    stream=settings.REQUESTS_STREAM,
                )

                logger.debug(
                    "response",
                    extra={
                        "method": prepped.method,
                        "url": response.url,
                        "status_code": response.status_code,
                        "text": response.text,
                    },
                )

                if self.__should_retry(response):
                    attempt += 1
                    self.sleep_retry(attempt, response)
                    continue

                return response

            except RequestException as e:
                logger.error(f"Request failed: {e}")

                attempt += 1
                self.sleep_retry(attempt)

        raise RetryError("Max retries exceeded")

    def get(self, endpoint: str = "", **kwargs) -> requests.Response:
        return self.__submit_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str = "", **kwargs) -> requests.Response:
        return self.__submit_request("POST", endpoint, **kwargs)

    def put(self, endpoint: str = "", **kwargs) -> requests.Response:
        return self.__submit_request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str = "", **kwargs) -> requests.Response:
        return self.__submit_request("DELETE", endpoint, **kwargs)
