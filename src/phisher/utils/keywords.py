import requests
from bs4 import BeautifulSoup


class Keywords:
    @staticmethod
    def search(domain: str, keywords: list) -> dict:
        result = {keyword: 0 for keyword in keywords}
        for protocol in ('https', 'http'):
            try:
                response = requests.get(f"{protocol}://{domain}", timeout=10)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                for keyword in keywords:
                    result[keyword] = text.lower().count(keyword.lower())
                break  # успех
            except requests.exceptions.RequestException:
                continue
        return result


# Example for debugging
if __name__ == "__main__":
    res = Keywords.search(domain="bspb.ru", keywords=[
                          "Банк", "Банк Санкт-Петербург", "БСПБ"])
    print(res)
