from pathlib import Path
import json
from typing import Dict, Any, Optional


def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    p = Path(path) if path else Path(__file__).resolve().parents[2] / "config" / "dev_caps.json"
    with open(p, "r") as f:
        return json.load(f)
