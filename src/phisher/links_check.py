import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.progress import Progress, console


class FindLinks:
    def __init__(self) -> None:
        pass

    # Function converts the provided DOMAIN into a URL for use in check_resources()
    @staticmethod
    def _domain_to_url(domain: str, protocol='https') -> str:
        if not domain.startswith('http://') and not domain.startswith('https://'):
            url = f"{protocol}://{domain}"
        else:
            url = domain
        return url


def check_resources(self, domain: str, max_depth: int = 2, max_urls: int = 10) -> List[str]:
    """
    Находит все ссылки на изображения и иконки на странице и её поддоменах,
    но не глубже max_depth и не более max_urls обработанных URL.
    """
    available_links = set()
    url = self._domain_to_url(domain)
    # Очередь хранит (url, depth)
    queue = [(url, 0)]
    processed = 0

    with Progress() as progress:
        # Внешний цикл с учётом глубины
        for current_url, depth in queue:
            if depth > max_depth or processed >= max_urls:
                continue
            processed += 1
            try:
                response = requests.get(current_url, timeout=5)
            except Exception:
                console.log(f"[red]Failed to connect to {current_url}[/]")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')

            images = soup.find_all('img', src=True)
            icons = soup.find_all('link', rel='icon')
            total_task = progress.add_task(
                f"[blue]Search for links for {current_url}...", total=len(images)+len(icons))

            for image in images:
                src = image['src']
                full_src = urljoin(current_url, src)
                available_links.add(full_src)
                progress.update(total_task, advance=1)

            for icon in icons:
                href = icon['href']
                full_href = urljoin(current_url, href)
                available_links.add(full_href)
                progress.update(total_task, advance=1)

            # Собираем поддомены, но только если не достигли max_depth
            if depth < max_depth:
                subdomains = set()
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    parsed_link = urlparse(href)
                    if parsed_link.netloc.endswith(domain) and parsed_link.netloc != domain:
                        subdomains.add(parsed_link.netloc)
                for subdomain in subdomains:
                    parsed_url = urlparse(current_url)
                    subdomain_url = f"{parsed_url.scheme}://{subdomain}"
                    # Проверяем, нет ли уже в очереди (с любой глубиной)
                    if not any(u == subdomain_url for u, _ in queue):
                        queue.append((subdomain_url, depth + 1))
            progress.update(total_task, total=100, completed=100)

    return list(available_links)


# Example for debug
if __name__ == "__main__":
    domain = "bspb.ru"  # company domain
    links = FindLinks().check_resources(domain)
    print(links)
