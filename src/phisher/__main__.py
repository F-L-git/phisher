# src/phisher/__main__.py
import os
import argparse
import logging
from phisher.config.config_loader import load_config
from phisher.adapters.netlas_adapter import NetlasAdapter
from phisher.adapters.dnstwist_adapter import DnstwistAdapter
from phisher.core.pipeline import Pipeline
from phisher.models.perimeter import Perimeter
from phisher.utils.inparse import read
import phisher.utils.cout as cout


def main():
    # Настройка логирования из конфига
    config = load_config()
    log_config = config.get('logging', {})
    logging.basicConfig(
        level=getattr(logging, log_config.get('level', 'INFO')),
        format=log_config.get(
            'format', "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--perimeter",
                        help="Path to perimeter JSON", required=True)
    parser.add_argument(
        "-a", "--apikey", help="Netlas API key", required=False)
    args = parser.parse_args()

    # Получаем API ключ
    api_key = args.apikey or os.environ.get(
        'NETLAS_API_KEY') or config.get('netlas', {}).get('api_key')
    if not api_key:
        logger.error(
            "No Netlas API key provided. Use -a, set NETLAS_API_KEY env or config")
        return

    # Загружаем сырые данные
    raw_data = read(args.perimeter)

    # Валидируем через Pydantic
    try:
        perimeter = Perimeter(**raw_data)
    except Exception as e:
        logger.error(f"Invalid perimeter file: {e}")
        return

    # Создаём адаптеры
    search_engine = NetlasAdapter(api_key)
    whois_provider = search_engine
    mutation_gen = DnstwistAdapter()

    # Инициализируем пайплайн и передаём сервисы
    pipeline = Pipeline()
    pipeline.set_services(search_engine, whois_provider, mutation_gen)

    # Передаём в пайплайн словарь с данными (perimeter.dict() или __dict__)
    # используем .dict() для pydantic v2
    wrong_domains = pipeline.run(perimeter.dict())

    # Печатаем результат
    cout.print_domains(wrong_domains)


if __name__ == "__main__":
    main()
