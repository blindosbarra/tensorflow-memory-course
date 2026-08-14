"""One long-lived event loop for the whole GUI process.

Streamlit is synchronous: every interaction re-runs the script top to bottom.
The obvious way to call an async ADK runner from there is `asyncio.run(...)`
per click — and it is a trap. `asyncio.run` creates a *fresh* event loop and
closes it on return, while the objects we deliberately keep across
interactions (a `TutorSession`'s `InMemoryRunner`, and the `google.genai`
HTTP client it holds) bind to the loop that created them. The second question
in a conversation would then run against a closed loop.

So the GUI gets exactly one background thread running one event loop for the
process's lifetime, and `run_coro` submits work to it from Streamlit's
threads. The loop is a daemon: it must not keep the process alive after
Streamlit shuts down.

Not needed by the CLI — `scripts/generate_lesson_doc.py` does one run and
exits, where `asyncio.run` is exactly right.
"""

from __future__ import annotations

import asyncio
from collections.abc import Coroutine
import threading
from typing import Any, TypeVar

T = TypeVar("T")

_loop: asyncio.AbstractEventLoop | None = None
_lock = threading.Lock()


def _ensure_loop() -> asyncio.AbstractEventLoop:
    global _loop
    with _lock:
        if _loop is not None and not _loop.is_closed():
            return _loop
        loop = asyncio.new_event_loop()
        thread = threading.Thread(
            target=loop.run_forever, name="lesson-agent-loop", daemon=True
        )
        thread.start()
        _loop = loop
        return loop


def run_coro(coro: Coroutine[Any, Any, T], timeout: float | None = 600.0) -> T:
    """Run a coroutine on the shared loop and block until it returns.

    `timeout` defaults to ten minutes: the five-agent pipeline makes five
    sequential-ish LLM calls over a whole notebook, and a hung request should
    surface as an error in the GUI rather than a spinner that never stops.
    """

    loop = _ensure_loop()
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result(timeout=timeout)
