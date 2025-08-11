"""Chroma client configuration with backward compatibility.

Newer versions of chromadb have migrated away from legacy Settings keys like
`chroma_db_impl`, `persist_directory`, etc. Supplying those now raises the
ValueError about a deprecated configuration. We centralize creation here and
fall back to the legacy style only if the new PersistentClient API is not
available (older chromadb versions).
"""

from __future__ import annotations

from typing import Any

import chromadb

try:  # Newer chromadb (>=0.4.* / post‑migration)
        from chromadb import PersistentClient  # type: ignore
        _HAS_PERSISTENT = True
except Exception:  # pragma: no cover - older version
        PersistentClient = None  # type: ignore
        _HAS_PERSISTENT = False

try:
        # Older Settings still exists; import lazily for fallback.
        from chromadb.config import Settings  # type: ignore
except Exception:  # pragma: no cover
        Settings = None  # type: ignore

DEFAULT_DB_DIR = "db"


def get_chroma_client(persist_directory: str = DEFAULT_DB_DIR, *, anonymized_telemetry: bool = False):
        """Return an appropriate Chroma client for current library version.

        1. Prefer new PersistentClient(path=...).
        2. Fallback to legacy chromadb.Client(Settings(...)).
        """
        if _HAS_PERSISTENT and PersistentClient is not None:
                return PersistentClient(path=persist_directory, settings=chromadb.Settings(anonymized_telemetry=anonymized_telemetry))
        # Legacy path
        if Settings is None:
                # As a last resort just build a default client (may not persist)
                return chromadb.Client()
        return chromadb.Client(
                Settings(
                        chroma_db_impl="duckdb+parquet",
                        persist_directory=persist_directory,
                        anonymized_telemetry=anonymized_telemetry,
                )
        )


# For legacy imports elsewhere expecting CHROMA_SETTINGS we expose a minimal
# object; LangChain will ignore unknown attrs when passing a concrete client.
class _LegacySettingsShim:
        anonymized_telemetry = False


CHROMA_SETTINGS = _LegacySettingsShim()  # backward compatibility export

__all__ = ["get_chroma_client", "CHROMA_SETTINGS", "DEFAULT_DB_DIR"]
