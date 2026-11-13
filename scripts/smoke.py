import httpx
from django.conf import settings
from django.db import connection


with connection.cursor() as cur:
    cur.execute("SELECT version()")
    print("DB OK:", cur.fetchone()[0][:30])
    cur.execute("SELECT name FROM pg_available_extensions WHERE name='vector'")
    print("pgvector available:", cur.fetchone() is not None)

from openai import OpenAI
r = OpenAI(base_url=settings.OLLAMA_BASE_URL + "/v1",  api_key="oolama").chat.completions.create(
    model = settings.OLLAMA_CHAT_MODEL,
    messages = [{'role': 'user', 'content': 'Replay with the word ok'}]
)
print('LLM OK', r.choices[0].message.content, "|", "tokens:", r.usage.total_tokens)

try:
    tags = httpx.get(settings.OLLAMA_BASE_URL + "/api/tags").json()
    print("Ollama models:", [m["name"] for m in tags['models']])
except Exceptions as e:
    print("Ollama not running (fine for now):", type(e).__name__)