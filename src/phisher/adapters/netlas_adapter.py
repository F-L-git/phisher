from phisher.core.interfaces import SearchEngine, WhoisProvider
from netlas import Netlas
import json
import time
from typing import List, Dict, Any
from phisher.config.config_loader import load_config

class NetlasAdapter(SearchEngine, WhoisProvider):
    def __init__(self, api_key: str):
        self.conn = Netlas(api_key=api_key)
        self.config = load_config()
        self.sleep_interval = self.config.get(
            'netlas', {}).get('sleep_between_requests', 1)

    def _parse_jsons(self, json_string: str) -> List[Dict[str, Any]]:
        json_string = '[' + json_string.replace('}{', '},{') + ']'
        return json.loads(json_string)

    def count(self, datatype: str, query: str) -> int:
        result = self.conn.count(datatype=datatype, query=query)
        time.sleep(self.sleep_interval)
        return result.get('count', 0)

    def download(self, datatype: str, query: str, fields: str, size: int) -> List[Dict[str, Any]]:
        if size == 0:
            return []
        iterator = self.conn.download(
            datatype=datatype, query=query, fields=fields, size=size)
        full_bytes = b"".join(iterator)
        data = self._parse_jsons(full_bytes.decode("utf-8"))
        time.sleep(self.sleep_interval)
        return data

    def get_whois(self, domain: str) -> List[Dict[str, Any]]:
        count = self.count("whois-domain", domain)
        if count == 0:
            return []
        return self.download("whois-domain", domain, "", count)
