from contextvars import ContextVar
from typing import Any

_store: ContextVar[dict] = ContextVar("request_context", default={})


class _RequestContext:
    def set(self, key: str, value: Any) -> None:
        ctx = _store.get({})
        _store.set({**ctx, key: value})

    def get(self, key: str, default: Any = None) -> Any:
        return _store.get({}).get(key, default)

    def clear(self) -> None:
        _store.set({})


request_context = _RequestContext()
