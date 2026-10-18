
import pytest

import url_shortener as module
from url_shortener import LRUCache, URLShortener


@pytest.fixture
def shortener(tmp_path, monkeypatch):
    # Use a temporary database so tests do not change your real data.
    monkeypatch.setattr(
        module,
        "DB_PATH",
        tmp_path / "test_smarturl.db"
    )
    return URLShortener()


def test_lru_cache_returns_saved_value():
    cache = LRUCache(capacity=2)
    cache.put("a", "first")
    cache.put("b", "second")

    assert cache.get("a") == "first"


def test_lru_cache_removes_least_recently_used_item():
    cache = LRUCache(capacity=2)
    cache.put("a", "first")
    cache.put("b", "second")
    cache.get("a")
    cache.put("c", "third")

    assert cache.get("b") is None
    assert cache.get("a") == "first"
    assert cache.get("c") == "third"


def test_shorten_and_retrieve_url(shortener):
    original = "https://example.com"

    code = shortener.shorten_url(original)

    assert len(code) == 6
    assert shortener.get_original_url(code) == original


def test_unknown_code_returns_none(shortener):
    assert shortener.get_original_url("missing") is None


def test_click_statistics(shortener):
    code = shortener.shorten_url("https://example.com")

    shortener.record_click(code)
    shortener.record_click(code)

    stats = shortener.get_stats(code)

    assert stats["original_url"] == "https://example.com"
    assert stats["clicks"] == 2


def test_unknown_code_has_no_statistics(shortener):
    assert shortener.get_stats("missing") is None
