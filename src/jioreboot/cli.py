import requests
import re
import sys
import json
import platformdirs
import pathlib

HOST = "192.168.29.1"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "sec-gpc": "1",
}
RE_TOKEN = re.compile(r"type=\"hidden\" +name=\"token\" +value=\"(?P<token>\w+)\">")
CONFIG_DIR = pathlib.Path(platformdirs.user_config_dir("jioreboot", ensure_exists=True))
CONFIG_PATH = CONFIG_DIR / "config.json"

cookies = {
    "recordModified": "1",
}


def _request_post(data: dict[str, str]) -> requests.Response:
    url = f"http://{HOST}/platform.cgi"
    return requests.post(
        url,
        cookies=cookies,
        headers={**HEADERS, "Origin": HOST, "Referer": url},
        data=data,
        verify=False,
    )


def load_config(path: pathlib.Path | str) -> dict[str, str]:
    with open(path, "r") as file:
        return json.load(file)


def get_token(html: str) -> str | None:
    token_match = RE_TOKEN.search(html)
    return token_match["token"] if token_match else None


def reboot(token: str) -> bool:
    print("INFO: Rebooting...")

    data = {
        "thispage": "factoryDefault.html",
        "token": token,
        "button.reboot.statusPage": "Reboot",
    }
    resp = _request_post(data)

    if resp.status_code != 200:
        print("ERROR: Reboot failed because of status code", resp.status_code)
        return False

    print(f"INFO: Requesting reboot successful.")
    print("INFO: It may take upwards of 90 seconds to complete.")
    return True


def login(username: str, password: str) -> requests.Response:
    print("INFO: Username ::", username);
    print("INFO: Password ::", password)
    print("INFO: Logging in...")

    data = {
        "thispage": "index.html",
        "users.username": username,
        "users.password": password,
        "button.login.users.dashboard": "Login",
    }

    resp = _request_post(data)

    cookie = resp.headers["Set-Cookie"].split("=")[1]
    cookies["TeamF1Login"] = cookie

    print(f"INFO: Login successful with {cookie=}.")
    return resp


def main():
    try:
        config = load_config(CONFIG_PATH)
    except FileNotFoundError:
        print(f"ERROR: Config file {CONFIG_PATH} not found")
        sys.exit(1)

    resp = login(config["username"], config["password"])
    if not resp.text:
        print("ERROR: Login failed because of empty response")
        sys.exit(1)

    token = get_token(resp.text)
    if not token:
        print("ERROR: Login failed because of missing token")
        sys.exit(1)

    reboot(token)


if __name__ == "__main__":
    main()
