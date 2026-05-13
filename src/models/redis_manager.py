"""Gerenciamento de conexão com Redis."""

from __future__ import annotations

import redis


class RedisManager:
    def __init__(
        self,
        host: str,
        port: int,
        db: int = 0,
        password: str | None = None,
        decode_responses: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self._client: redis.Redis | None = None

    def connect(self) -> redis.Redis:
        client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=self.decode_responses,
        )
        client.ping()
        self._client = client
        return client

    def ensure_connected(self) -> redis.Redis:
        if self._client is None:
            return self.connect()
        return self._client

    def test_connection(self) -> tuple[bool, str]:
        try:
            self.ensure_connected().ping()
            return True, f"Conexão Redis OK em: {self.host}:{self.port}/{self.db}"
        except Exception as exc:
            return False, f"Falha no Redis: {exc}"
