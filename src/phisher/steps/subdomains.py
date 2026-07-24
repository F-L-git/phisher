from phisher.core.interfaces import SearchEngine
from typing import List


class Subdomains:
    def __init__(self, search_engine: SearchEngine):
        self.search_engine = search_engine

    def _make_query(self, name: str, legit_domains_exception: str, max_level: int) -> str:
        return f"domain:{name}.* level:[3 TO {max_level}] a:*" + legit_domains_exception

    def search(self, names: List[str], legit_topdomains: List[str], max_level: int = 4) -> List[str]:
        domains = []
        legit_domains_exception = "!domain:(" + " || ".join(
            [f"*.{domain}" for domain in legit_topdomains]) + ")"
        for name in names:
            query = self._make_query(name, legit_domains_exception, max_level)
            count = self.search_engine.count("domain", query)
            if count > 0:
                data = self.search_engine.download(
                    "domain", query, "domain", count)
                for item in data:
                    domains.append(item['data']['domain'])
        return domains
