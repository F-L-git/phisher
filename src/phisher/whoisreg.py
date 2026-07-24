import json
from time import sleep
from typing import Dict, List

from bs4 import BeautifulSoup
from netlas import Netlas
import requests
from rich import _console

from links_check import FindLinks
from keywords import Keywords
from rich.progress import Progress


def parse_jsons(json_string):
    json_string = "[" + json_string.replace("}{", "},{") + "]"
    return json.loads(json_string)


# Heuristics are needed to identify legitimate resources obtained.
class WhoisIdentification:
    def __init__(self, netlas_connection: Netlas) -> None:
        self.netlas_connection = netlas_connection

    def _check_registration_data(self, data: dict, whois_data: dict) -> bool:
        # Check if registrant organization matches any of the specified organization names
        if "registrant" in data and "organization" in data["registrant"]:
            for name in whois_data.get("organisation", []):
                if data["registrant"]["organization"] == name:
                    return True
        # Check if registrant phone matches any of the specified phone numbers
        if "registrant" in data and "phone" in data["registrant"]:
            for phone in whois_data.get("phone", []):
                if data["registrant"]["phone"] == phone:
                    return True
        # Check if registrant email matches any of the specified email addresses
        if "registrant" in data and "email" in data["registrant"]:
            for email in whois_data.get("email", []):
                if data["registrant"]["email"] == email:
                    return True
        return False

    @staticmethod
    def search(domain: str, keywords: List[str]) -> Dict[str, int]:
        """
        Пытается получить страницу сначала по HTTPS, при неудаче – по HTTP.
        Возвращает словарь {keyword: количество вхождений}.
        """
        result = {keyword: 0 for keyword in keywords}
        # Пробуем протоколы по порядку
        for protocol in ('https', 'http'):
            try:
                response = requests.get(f"{protocol}://{domain}", timeout=5)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                for keyword in keywords:
                    result[keyword] = text.lower().count(keyword.lower())
                # Если дошли сюда – успех, прерываем цикл
                break
            except Exception:
                # Если ошибка, пробуем следующий протокол
                continue
        # Если оба протокола не сработали, возвращаем нули
        return result

    # Evaluates pages of wrong domains for the occurrence of official images and keywords
    # Returns a dict() of invalid domains with a criticality score (1 - 3)

    @staticmethod
    def domain_double_check(true_links: List[str], keywords: List[str], wrong_domains: Dict[str, int]) -> Dict[str, int]:
        finder = FindLinks()
        for w_domain in list(wrong_domains.keys()):
            try:
                # Ограничиваем глубину и количество обрабатываемых URL
                suspicious_links = finder.check_resources(
                    w_domain, max_depth=1, max_urls=5)
                for link in suspicious_links:
                    if link in true_links:
                        wrong_domains[w_domain] += 1
                        break
            except Exception as e:
                _console.log(
                    f"[red]Error checking resources for {w_domain}: {e}[/]")

            occurrences = Keywords.search(w_domain, keywords)
            # Если хотя бы одно ключевое слово найдено – увеличиваем счётчик
            if any(count > 0 for count in occurrences.values()):
                wrong_domains[w_domain] += 1

        return wrong_domains


# Example for debugging
input_domains = ["bspb.ru", "www.bspb.ru",
                 "travel.bspb.ru", " margin.fx.bspb.ru"]
whoisreg = {
    "organisation": ['PJSC "Bank "Saint-Petersburg"'],
    "email": [],
    "phone": [],
}

if __name__ == "__main__":
    netlas_connection = Netlas(api_key="5wKN7tr6dULDSLntT8Gq4LPxIT4Jq05b")
    registrant = WhoisIdentification(netlas_connection)
    correct_domains, wrong_domains = registrant.search(
        domains=input_domains, whois_data=whoisreg
    )
    wrong_domains['bspb.ru'] = 1  # just for an example
    print(wrong_domains)

    real_links = FindLinks().check_resources('bspb.ru')
    wrong_domains = registrant.domain_double_check(
        true_links=real_links,
        keywords=["Банк", "Банк Санкт-Петербург", "БСПБ"],
        wrong_domains=wrong_domains
    )
    print(wrong_domains)
