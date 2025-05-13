from __future__ import annotations

from collections import OrderedDict
from typing import Generic, TypeVar
from typing import OrderedDict as TOrderedDict

K = TypeVar("K")
V = TypeVar("V")


class Cache2Q(Generic[K, V]):
    def __init__(
        self,
        size: int,
        recent_ratio: float = 0.25,
        recent_evict_ratio: float = 0.5,
        frequent_ratio: float = 0.25,
    ):
        if size <= 0:
            raise ValueError("invalid size")

        self._recent: TOrderedDict[K, V] = OrderedDict()
        self._recent_max_size = int(size * recent_ratio)

        self._recent_evict: TOrderedDict[K, V] = OrderedDict()
        self._recent_evict_max_size = int(size * recent_evict_ratio)

        self._frequent: TOrderedDict[K, V] = OrderedDict()
        self._frequent_max_size = int(size * frequent_ratio)

    def get(self, key: K) -> V | None:
        if key in self._frequent:
            self._frequent.move_to_end(key)
            return self._frequent[key]

        if key in self._recent_evict:
            value = self._recent_evict[key]
            del self._recent_evict[key]
            self._set_frequent(key, value)
            return value

        return self._recent.get(key)

    def set(self, key: K, value: V) -> None:
        if key in self._frequent:
            self._frequent[key] = value
            self._frequent.move_to_end(key)
            return

        if key in self._recent_evict:
            del self._recent_evict[key]
            self._set_frequent(key, value)
            return

        self._set_recent(key, value)

    def remove(self, key: K) -> None:
        if key in self._frequent:
            del self._frequent[key]
        elif key in self._recent_evict:
            del self._recent_evict[key]
        elif key in self._recent:
            del self._recent[key]

    def clear(self) -> None:
        self._recent.clear()
        self._recent_evict.clear()
        self._frequent.clear()

    def _set_frequent(self, key: K, value: V) -> None:
        if len(self._frequent) >= self._frequent_max_size:
            _ = self._frequent.popitem(last=False)
        self._frequent[key] = value

    def _set_recent(self, key: K, value: V) -> None:
        if key in self._recent:
            self._recent[key] = value
            return

        if len(self._recent) >= self._recent_max_size:
            evict_k, evict_v = self._recent.popitem(last=False)
            self._set_recent_evict(evict_k, evict_v)
        self._recent[key] = value

    def _set_recent_evict(self, key: K, value: V) -> None:
        if len(self._recent_evict) >= self._recent_evict_max_size:
            _ = self._recent_evict.popitem(last=False)
        self._recent_evict[key] = value
