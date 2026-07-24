from phisher.core.interfaces import WhoisProvider
from typing import Dict, List, Tuple
import logging
from phisher.utils.links_check import FindLinks
from phisher.utils.keywords import Keywords

logger = logging.getLogger(__name__)


class WhoisIdentification:
    def __init__(self, whois_provider: WhoisProvider):
        self.whois_provider = whois_provider

    def _check_registration_data(self, data: dict, whois_data: dict) -> bool:
        # как было
        if "registrant" in data and "organization" in data["registrant"]:
            for name in whois_data.get("organisation", []):
                if data["registrant"]["organization"] == name:
                    return True
        if "registrant" in data and "phone" in data["registrant"]:
            for phone in whois_data.get("phone", []):
                if data["registrant"]["phone"] == phone:
                    return True
        if "registrant" in data and "email" in data["registrant"]:
            for email in whois_data.get("email", []):
                if data["registrant"]["email"] == email:
                    return True
        return False

    def search(self, domains: List[str], whois_data: dict) -> Tuple[dict, dict]:
        correct_domains = {}
        wrong_domains = {}
        for domain in domains:
            whois_entries = self.whois_provider.get_whois(domain)
            if not whois_entries:
                # нет данных — считаем подозрительным
                wrong_domains[domain] = 1
                continue
            matched = False
            for entry in whois_entries:
                if self._check_registration_data(entry['data'], whois_data):
                    matched = True
                    break
            if matched:
                correct_domains[domain] = 0
            else:
                wrong_domains[domain] = 1
        return correct_domains, wrong_domains

    def domain_double_check(self, true_links: List[str], keywords: List[str],
                            wrong_domains: Dict[str, int],
                            max_depth: int = 1, max_urls: int = 5) -> Dict[str, int]:
        finder = FindLinks()
        for domain in list(wrong_domains.keys()):
            try:
                suspicious_links = finder.check_resources(
                    domain, max_depth=max_depth, max_urls=max_urls)
                for link in suspicious_links:
                    if link in true_links:
                        wrong_domains[domain] += 1
                        break
            except Exception as e:
                logger.error(f"Error checking resources for {domain}: {e}")
            occurrences = Keywords.search(domain, keywords)
            if any(count > 0 for count in occurrences.values()):
                wrong_domains[domain] += 1
        return wrong_domains
