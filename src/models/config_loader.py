"""Leitura dos arquivos de configuração (.ini)."""

from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path


class ConfigLoader:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def load_sqlite_config(self) -> dict:
        parser = ConfigParser()
        parser.read(self.project_root / "config" / "sqlite.ini", encoding="utf-8")
        relative_path = parser.get("sqlite", "db_path")
        full_path = self.project_root / relative_path
        return {
            "db_path": str(full_path),
            "source_file": str(self.project_root / "config" / "sqlite.ini"),
        }

    def load_mongodb_config(self) -> dict:
        parser = ConfigParser()
        parser.read(self.project_root / "config" / "mongodb.ini", encoding="utf-8")
        return {
            "uri": parser.get("mongodb", "uri"),
            "database": parser.get("mongodb", "database"),
            "use_mongomock_on_failure": parser.getboolean("mongodb", "use_mongomock_on_failure"),
            "source_file": str(self.project_root / "config" / "mongodb.ini"),
        }

    def load_redis_config(self) -> dict:
        parser = ConfigParser()
        parser.read(self.project_root / "config" / "redis.ini", encoding="utf-8")
        password = parser.get("redis", "password", fallback="")
        return {
            "host": parser.get("redis", "host", fallback="localhost"),
            "port": parser.getint("redis", "port", fallback=6379),
            "db": parser.getint("redis", "db", fallback=0),
            "password": password if password else None,
            "decode_responses": parser.getboolean("redis", "decode_responses", fallback=True),
            "key_prefix": parser.get("redis", "key_prefix", fallback="ecommerce"),
            "product_cache_ttl_seconds": parser.getint(
                "redis", "product_cache_ttl_seconds", fallback=3600
            ),
            "cart_ttl_seconds": parser.getint("redis", "cart_ttl_seconds", fallback=1800),
            "source_file": str(self.project_root / "config" / "redis.ini"),
        }
