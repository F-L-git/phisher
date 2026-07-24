import os
import yaml
from typing import Any, Dict


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Подстановка переменных окружения вида ${VAR}
    def resolve_env(value):
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            var = value[2:-1]
            return os.environ.get(var, "")
        return value

    def traverse(obj):
        if isinstance(obj, dict):
            return {k: traverse(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [traverse(v) for v in obj]
        else:
            return resolve_env(obj)

    return traverse(config)
