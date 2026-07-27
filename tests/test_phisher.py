# tests/test_phisher.py
import pytest
from phisher import check_domain   # предполагаем, что есть такая функция

def test_check_domain_phishing():
    # Пример: домен, который считается фишинговым
    result = check_domain("phishing-site.com")
    assert result is True

def test_check_domain_safe():
    result = check_domain("google.com")
    assert result is False