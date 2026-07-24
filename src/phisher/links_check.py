import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.progress import Progress


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
    
    # Function finds all links to images and icons present on the page and its subdomains.
    # Returns a list of image links and a list of icon links.
    def check_resources(self, domain: str) -> list:
        available_links = set()

        url = self._domain_to_url(domain)
        # Queue for traversing links on pages
        queue = [url]
        with Progress() as progress:
            for current_url in queue:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Search for images and icons links
                images = soup.find_all('img', src=True)
                icons = soup.find_all('link', rel='icon')
                total_task = progress.add_task(f"[blue]Search for links for {current_url}...", total=len(images)+len(icons))

                # Search for images
                for image in images:
                    src = image['src']
                    full_src = urljoin(current_url, src)
                    available_links.add(full_src)
                    progress.update(total_task, advance=1)
                
                # Search for icons
                for icon in icons:
                    href = icon['href']
                    full_href = urljoin(current_url, href)
                    available_links.add(full_href)
                    progress.update(total_task, advance=1)
                     

                # Add links with subdomains to the queue
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
                    if subdomain_url not in queue:  # Add the link to the queue if it's not there already
                        queue.append(subdomain_url)
                progress.update(total_task, total=100, completed=100)
        return list(available_links)


# Example for debug
if __name__ == "__main__":
    domain = "bspb.ru"  # company domain
    links = FindLinks().check_resources(domain)
    print(links)