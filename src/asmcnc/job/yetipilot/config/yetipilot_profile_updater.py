import requests
import json

# TO DO: Change this to the correct URL
PROFILES_URL = "https://localhost:7293/Download"
PROFILES_PATH = "profiles.json"
DEV_MODE = True


def get_profiles_version():
    # type: () -> float
    with open(PROFILES_PATH, "r") as f:
        return json.load(f)["Version"]


def check_for_new_profiles(profiles_version):
    # type: (float) -> bool
    try:
        response = requests.get(PROFILES_URL, verify=not DEV_MODE)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return False

    profiles_json = response.json()
    if profiles_json["Version"] != profiles_version:
        return True
    return False


def get_new_profiles():
    # type: () -> bool
    try:
        response = requests.get(PROFILES_URL, verify=not DEV_MODE)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return False

    with open(PROFILES_PATH, "w") as f:
        f.write(response.text)
    return True


def run():
    # type: () -> bool
    update_available = check_for_new_profiles(get_profiles_version())
    download_successful = get_new_profiles() if update_available else None
    return download_successful