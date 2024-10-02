from __future__ import annotations

from typing import Callable
from functools import partial, update_wrapper, lru_cache


class RecursionOperator[*Ds, C]:
    def __init__(self, f: Callable[[RecursionOperator[*Ds, C], *Ds], C]):
        self.f = f

    @lru_cache
    def recurse(self, *args: *Ds) -> C:
        return self.f(self, *args)

    def __call__(self, *args: *Ds) -> C:
        return self.recurse(*args)


def fix[*Ds, C](f: Callable[[RecursionOperator[*Ds, C], *Ds], C]) -> Callable[[*Ds], C]:
    return update_wrapper(partial(f, RecursionOperator(f)), f)
