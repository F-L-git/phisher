import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.progress import Progress
from typing import List, Set, Tuple
import logging
from time import sleep

logger = logging.getLogger(__name__)


class FindLinks:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _domain_to_url(domain: str, protocol: str = 'https') -> str:
        """Преобразует домен в URL с указанным протоколом."""
        if not domain.startswith(('http://', 'https://')):
            return f"{protocol}://{domain}"
        return domain

    def check_resources(self, domain: str, max_depth: int = 2, max_urls: int = 10) -> List[str]:
        """
        Собирает ссылки на изображения и иконки на главной странице и поддоменах,
        но не глубже max_depth и не более max_urls обработанных URL.

        Args:
            domain (str): Домен для проверки (например, example.com).
            max_depth (int): Максимальная глубина обхода поддоменов (0 – только главная).
            max_urls (int): Максимальное количество URL, которые будут обработаны.

        Returns:
            List[str]: Список уникальных ссылок на изображения и иконки.
        """
        available_links: Set[str] = set()
        start_url = self._domain_to_url(domain)

        # Очередь: каждый элемент — (url, глубина)
        queue: List[Tuple[str, int]] = [(start_url, 0)]
        processed = 0

        with Progress() as progress:
            # Внешний цикл по очереди, но с учётом лимитов
            idx = 0
            while idx < len(queue) and processed < max_urls:
                current_url, depth = queue[idx]
                idx += 1

                if depth > max_depth:
                    continue

                processed += 1
                logger.debug(f"Processing {current_url} (depth={depth})")

                try:
                    # Пробуем HTTPS, если не получилось – HTTP
                    response = None
                    for protocol in ('https', 'http'):
                        try:
                            url_to_get = self._domain_to_url(
                                current_url, protocol)
                            response = requests.get(url_to_get, timeout=10)
                            break
                        except requests.exceptions.RequestException:
                            continue
                    if response is None:
                        logger.warning(f"Could not reach {current_url}")
                        continue
                    response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Собираем изображения
                    images = soup.find_all('img', src=True)
                    icons = soup.find_all('link', rel='icon')
                    total_task = progress.add_task(
                        f"[blue]Scanning {current_url}...",
                        total=len(images) + len(icons)
                    )

                    for img in images:
                        src = img['src']
                        full = urljoin(current_url, src)
                        available_links.add(full)
                        progress.update(total_task, advance=1)

                    for icon in icons:
                        href = icon['href']
                        full = urljoin(current_url, href)
                        available_links.add(full)
                        progress.update(total_task, advance=1)

                    # Собираем поддомены для дальнейшего обхода, только если не достигли max_depth
                    if depth < max_depth:
                        subdomains = set()
                        for a in soup.find_all('a', href=True):
                            href = a['href']
                            parsed = urlparse(href)
                            # Если ссылка ведёт на поддомен того же домена
                            if parsed.netloc and parsed.netloc.endswith(domain) and parsed.netloc != domain:
                                subdomains.add(parsed.netloc)

                        for sub in subdomains:
                            # Определяем протокол из текущего URL
                            parsed_cur = urlparse(current_url)
                            scheme = parsed_cur.scheme if parsed_cur.scheme else 'https'
                            sub_url = f"{scheme}://{sub}"
                            # Проверяем, нет ли уже в очереди (с любой глубиной)
                            if not any(u == sub_url for u, _ in queue):
                                queue.append((sub_url, depth + 1))

                    progress.update(total_task, total=100, completed=100)

                except Exception as e:
                    logger.error(f"Error processing {current_url}: {e}")
                    continue

        return list(available_links)
