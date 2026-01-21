import subprocess
from typing import List, Optional


def _run_adb_cmd(args: List[str], device: Optional[str] = None) -> str:
    base = ["adb"]
    if device:
        base += ["-s", device]
    base += args
    res = subprocess.run(base, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"adb failed: {res.stdout}\n{res.stderr}")
    return res.stdout.strip()


def list_devices() -> List[str]:
    out = _run_adb_cmd(["devices"])
    lines = [l for l in out.splitlines() if l.strip() and not l.startswith("List of devices")]
    devs = [l.split()[0] for l in lines if "device" in l or len(l.split()) >= 2]
    return devs


def get_first_device() -> Optional[str]:
    devs = list_devices()
    return devs[0] if devs else None


def get_wifi_state(device: Optional[str] = None) -> Optional[bool]:
    """Return True if wifi_on == 1, False if 0, else None."""
    out = _run_adb_cmd(["shell", "settings", "get", "global", "wifi_on"], device)
    out = out.strip()
    if out == "1":
        return True
    if out == "0":
        return False
    return None


def toggle_wifi(device: Optional[str] = None, enable: bool = True) -> None:
    cmd = "enable" if enable else "disable"
    _run_adb_cmd(["shell", "svc", "wifi", cmd], device)


def open_wifi_settings(device: Optional[str] = None) -> None:
    _run_adb_cmd(["shell", "am", "start", "-a", "android.settings.WIFI_SETTINGS"], device)
