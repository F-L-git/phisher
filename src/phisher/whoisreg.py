import json
from time import sleep

from netlas import Netlas

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

    # Returns two lists: correct and incorrect resources - according to the received registration data.

    def search(self, domains: list, whois_data: dict) -> tuple[dict, dict]:
        correct_domains = dict()  # domains that match the registration data
        wrong_domains = dict()  # domains that don't match the registration data
        with Progress() as progress:
            total_task = progress.add_task("[green]Check whois registrations...", total=len(domains))
            for domain in domains:
                count = self.netlas_connection.count(datatype="whois-domain", query=domain)["count"]
                if count != 0:
                    iterator = self.netlas_connection.download(
                        datatype="whois-domain", query=domain, size=count
                    )
                    bytes_data = b"".join(iterator)
                    results = parse_jsons(bytes_data.decode("utf-8"))
                    for result in results:
                        if self._check_registration_data(result["data"], whois_data):
                            correct_domains[result["data"]["domain"]] = 0
                        else:
                            if result["data"]["domain"] not in wrong_domains:
                                wrong_domains[result["data"]["domain"]] = 1
                progress.update(total_task, advance=1)
                sleep(1)
                
        return correct_domains, wrong_domains
    
    # Evaluates pages of wrong domains for the occurrence of official images and keywords
    # Returns a dict() of invalid domains with a criticality score (1 - 3)
    @staticmethod
    def domain_double_check(true_links: list, keywords: list, wrong_domains: dict) -> dict:
        for w_domain in wrong_domains:
            try:
                suspicious_links = FindLinks().check_resources(w_domain)
                for link in suspicious_links:
                    if link in true_links:
                        wrong_domains[w_domain] += 1
                        break
            except:
                print(f"Failed connection with {w_domain}")

            occurrences = Keywords.search(w_domain, keywords)
            for occur in occurrences:
                if occurrences[occur] > 0:
                    wrong_domains[w_domain] += 1
                    break
        return wrong_domains

# Example for debugging
input_domains = ["bspb.ru", "www.bspb.ru", "travel.bspb.ru"," margin.fx.bspb.ru"]
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
    wrong_domains['bspb.ru'] = 1 # just for an example
    print(wrong_domains)
    
    real_links = FindLinks().check_resources('bspb.ru')
    wrong_domains = registrant.domain_double_check(
        true_links=real_links,
        keywords=["Банк", "Банк Санкт-Петербург", "БСПБ"],
        wrong_domains=wrong_domains
    )
    print(wrong_domains)
    
