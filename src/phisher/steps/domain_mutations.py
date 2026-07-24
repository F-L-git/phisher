from phisher.core.interfaces import SearchEngine, MutationGenerator
from typing import List


class DomainMutations:
    def __init__(self, search_engine: SearchEngine, mutation_gen: MutationGenerator):
        self.search_engine = search_engine
        self.mutation_gen = mutation_gen

    def _make_query(self, mutations: List[str], max_query_operands: int = 100) -> List[str]:
        # как было
        queries = []
        current_string = "a:* domain:("
        current_operands = 0
        for mutation in mutations:
            part = f"{mutation}"
            if current_operands >= max_query_operands:
                queries.append(current_string[:-4] + ") level:2")
                current_string = "domain:(" + part + " || "
                current_operands = 1
            else:
                current_string += part + " || "
                current_operands += 1
        if current_string:
            queries.append(current_string[:-4] + ") level:2")
        return queries

    def search(self, domains: List[str]) -> List[str]:
        results = []
        for domain in domains:
            mutations = self.mutation_gen.generate(domain)
            # max_query_operands можно брать из конфига
            queries = self._make_query(mutations)
            for query in queries:
                count = self.search_engine.count("domain", query)
                if count > 0:
                    data = self.search_engine.download(
                        "domain", query, "domain", count)
                    for item in data:
                        results.append(item['data']['domain'])
        return results
