import redis
import json
import hashlib


class ExactCache:
    def __init__(self, host="localhost", port=6379, ttl=3600):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.ttl = ttl  # auto expire in 1 hour

    def _make_key(self, question: str) -> str:
        # Normalize question → lowercase + strip spaces
        normalized = question.strip().lower()
        # Hash it so long questions don't become huge keys
        return "exact:" + hashlib.md5(normalized.encode()).hexdigest()

    def get(self, question: str):
        key = self._make_key(question)
        cached = self.client.get(key)

        if cached:
            print("[ExactCache] HIT ")
            return json.loads(cached)

        print("[ExactCache] MISS ")
        return None

    def set(self, question: str, answer: str):
        key = self._make_key(question)
        self.client.setex(key, self.ttl, json.dumps(answer))
        print("[ExactCache] Saved to cache ")

    def delete(self, question: str):
        key = self._make_key(question)
        self.client.delete(key)

    def clear_all(self):
        # Delete all exact: keys
        for key in self.client.scan_iter("exact:*"):
            self.client.delete(key)
        print("[ExactCache] Cache cleared ")