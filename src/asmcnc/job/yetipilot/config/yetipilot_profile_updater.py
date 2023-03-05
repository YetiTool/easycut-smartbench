import requests
import json

# TO DO: Change this to the correct URL
PROFILES_URL = "https://localhost:7293/Download"
PROFILES_PATH = "asmcnc/job/yetipilot/config/profiles.json"
DEV_MODE = True


def version_tuple(v):
    return tuple(map(int, (v.split("."))))


def get_profiles_version():
    # type: () -> float
    with open(PROFILES_PATH, "r") as f:
        return json.load(f)["Version"]


def check_for_new_profiles(profiles_version, easycut_version):
    # type: (float, str) -> bool
    try:
        response = requests.get(PROFILES_URL, verify=not DEV_MODE)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return False

    try:
        profiles_json = response.json()
        if profiles_json["Version"] != profiles_version and \
                version_tuple(easycut_version) >= version_tuple(profiles_json["Easycut Requirement"]):
            return True
    except:
        return False
    return False


def get_new_profiles():
    # type: () -> bool
    try:
        response = requests.get(PROFILES_URL, timeout=2, verify=not DEV_MODE)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return False

    with open(PROFILES_PATH, "w") as f:
        f.write(response.text)
    return True


def run(easycut_version):
    # type: (str) -> bool
    update_available = check_for_new_profiles(get_profiles_version(), easycut_version)
    download_successful = get_new_profiles() if update_available else None
    return download_successful


if __name__ == "__main__":
    print(run("1.0.0"))