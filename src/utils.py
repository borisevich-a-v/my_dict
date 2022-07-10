import requests  # type: ignore


# TODO: improve it
def send_request(url: str) -> requests.Response:
    print(f"Sending request {url}")
    return requests.get(url)


