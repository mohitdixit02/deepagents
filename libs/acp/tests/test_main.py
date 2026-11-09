from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest


def test_import_main_module() -> None:
    from deepagents_acp import __main__  # noqa: F401


def test_import_server_module() -> None:
    """Verify deepagents_acp.server imports cleanly without raising ImportError."""
    from deepagents_acp import server  # noqa: F401


def test_server_and_utils_fallback_without_acp_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify fallback helper functions work when acp does not expose them."""
    import acp
    from acp.schema import AudioContentBlock, ImageContentBlock, TextContentBlock

    for attr in ("audio_block", "image_block", "text_block"):
        monkeypatch.delattr(acp, attr, raising=False)

    import deepagents_acp.server
    import deepagents_acp.utils

    importlib.reload(deepagents_acp.utils)
    importlib.reload(deepagents_acp.server)

    tb = deepagents_acp.server.text_block("test message")
    assert isinstance(tb, TextContentBlock)
    assert tb.text == "test message"

    ib = deepagents_acp.server.image_block("data123", "image/png", uri="http://example.com/img.png")
    assert isinstance(ib, ImageContentBlock)
    assert ib.data == "data123"
    assert ib.mime_type == "image/png"
    assert ib.uri == "http://example.com/img.png"

    ab = deepagents_acp.server.audio_block("audiodata", "audio/mp3")
    assert isinstance(ab, AudioContentBlock)
    assert ab.data == "audiodata"
    assert ab.mime_type == "audio/mp3"

    # Restore modules
    monkeypatch.undo()
    importlib.reload(deepagents_acp.utils)
    importlib.reload(deepagents_acp.server)
