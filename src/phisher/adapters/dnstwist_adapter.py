from phisher.core.interfaces import MutationGenerator
import dnstwist
import re
from typing import List


class DnstwistAdapter(MutationGenerator):
    def generate(self, domain: str) -> List[str]:
        # dnstwist.run может возвращать список, но в текущей версии он пишет в файл.
        # Обёртка: используем временный файл, но можно переделать на вывод в строку.
        # Для простоты оставим текущую логику, но вынесем временную папку в конфиг.
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            dnstwist.run(domain=domain, format="list", output=tmp.name)
            tmp.flush()
            with open(tmp.name, 'r') as f:
                mutations = f.readlines()
            os.unlink(tmp.name)
        if not mutations:
            return []
        # Обработка: добавляем звёздочки для wildcard-поиска
        result = []
        for i, line in enumerate(mutations):
            line = line.strip()
            if i == 0:
                result.append(line + '*')
            else:
                result.append(re.sub(r'\.[^.]*$', '.*', line))
        return result
