from typing import List, Dict, Any, Callable
from phisher.config.config_loader import load_config
from phisher.steps.domain_mutations import DomainMutations
from phisher.steps.subdomains import Subdomains
from phisher.steps.whoisreg import WhoisIdentification, WhoisIdentificationfrom phisher.core.interfaces import SearchEngine, WhoisProvider, MutationGenerator
import logging

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = load_config(config_path)
        self.steps = self.config.get('pipeline', {}).get('steps', [])
        self.context = {}  # будет хранить промежуточные данные

    def set_services(self, search_engine: SearchEngine, whois_provider: WhoisProvider, mutation_gen: MutationGenerator):
        self.search_engine = search_engine
        self.whois_provider = whois_provider
        self.mutation_gen = mutation_gen

    def run(self, perimeter: Dict[str, Any]) -> Dict[str, int]:
        # Инициализируем контекст с данными периметра
        self.context = {
            'perimeter': perimeter,
            'potential_phishing': [],
            'correct_domains': {},
            'wrong_domains': {}
        }
        for step_name in self.steps:
            step_func = getattr(self, f"_step_{step_name}", None)
            if step_func is None:
                logger.warning(f"Step {step_name} not implemented, skipping")
                continue
            logger.info(f"Running step: {step_name}")
            step_func()
        # После всех шагов возвращаем wrong_domains с критичностью
        return self.context['wrong_domains']

    def _step_domain_mutations(self):
        dm = DomainMutations(self.search_engine, self.mutation_gen)
        domains = self.context['perimeter']['domains']
        mutations = dm.search(domains)
        self.context['potential_phishing'].extend(mutations)

    def _step_subdomains(self):
        sd = Subdomains(self.search_engine)
        brandnames = self.context['perimeter']['brandnames']
        topdomains = self.context['perimeter']['topdomains']
        subdomains = sd.search(brandnames, topdomains)
        self.context['potential_phishing'].extend(subdomains)

    def _step_whois_check(self):
        whois = WhoisIdentification(self.whois_provider)
        potential = self.context['potential_phishing']
        whois_data = self.context['perimeter'].get('whois', {})
        correct, wrong = whois.search(potential, whois_data)
        self.context['correct_domains'].update(correct)
        self.context['wrong_domains'].update(wrong)

    def _step_double_check(self):
        whois = WhoisIdentification(self.whois_provider)
        wrong = self.context['wrong_domains']
        if not wrong:
            return
        true_links = self.context['perimeter'].get('imglinks', [])
        keywords = self.context['perimeter'].get('keywords', [])
        # Передаём конфигурацию для ограничения глубины и количества URL
        config = load_config()
        double_check_config = config.get('double_check', {})
        # Дополнительная проверка: можно передать параметры в метод domain_double_check
        # Модифицируем метод, чтобы он принимал max_depth, max_urls
        # Пока просто вызовем с параметрами по умолчанию из конфига
        wrong = whois.domain_double_check(true_links, keywords, wrong,
                                          max_depth=double_check_config.get(
                                              'max_depth', 1),
                                          max_urls=double_check_config.get('max_urls_per_domain', 5))
        self.context['wrong_domains'] = wrong
