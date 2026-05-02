# LLMCache — Semantic Cache for LLM Queries

A high-performance semantic caching library that reduces LLM API costs and latency by storing and reusing responses for similar queries. Works as a drop-in cache layer for any LLM-powered application.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit/)

## Quick Install

```bash
pip install LLMCache
```

## What is LLMCache?

ChatGPT and other large language models are powerful but expensive. As your application grows, LLM API costs can become substantial and response times can slow down under load.

LLMCache tackles this by building a **semantic cache** for LLM responses — instead of exact matching, it uses embedding algorithms to find *similar* previous queries and returns cached answers, dramatically cutting costs and latency.

## Quick Start

> Make sure Python version is **3.8.1 or higher**

### Install from source

```bash
git clone https://github.com/Rajshree1854/LLMCache.git
cd LLMCache
pip install -r requirements.txt
python setup.py install
```

### Exact match cache

```python
from LLMCache import cache
from LLMCache.adapter import openai

cache.init()
cache.set_openai_key()

# Identical questions will be served from cache after the first request
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': "what's github"}],
)
```

### Semantic (similar) search cache

```python
from LLMCache import cache
from LLMCache.adapter import openai
from LLMCache.embedding import Onnx
from LLMCache.manager import CacheBase, VectorBase, get_data_manager
from LLMCache.similarity_evaluation.distance import SearchDistanceEvaluation

onnx = Onnx()
data_manager = get_data_manager(CacheBase("sqlite"), VectorBase("faiss", dimension=onnx.dimension))
cache.init(
    embedding_func=onnx.to_embeddings,
    data_manager=data_manager,
    similarity_evaluation=SearchDistanceEvaluation(),
)
cache.set_openai_key()

# Semantically similar questions return cached responses
questions = [
    "what's github",
    "can you explain what GitHub is",
    "can you tell me more about GitHub",
    "what is the purpose of GitHub",
]
for question in questions:
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': question}],
    )
```

### Temperature control

```python
from LLMCache import cache
from LLMCache.manager import manager_factory
from LLMCache.embedding import Onnx
from LLMCache.processor.post import temperature_softmax
from LLMCache.similarity_evaluation.distance import SearchDistanceEvaluation
from LLMCache.adapter import openai

onnx = Onnx()
data_manager = manager_factory("sqlite,faiss", vector_params={"dimension": onnx.dimension})
cache.init(
    embedding_func=onnx.to_embeddings,
    data_manager=data_manager,
    similarity_evaluation=SearchDistanceEvaluation(),
    post_process_messages_func=temperature_softmax,
)

# temperature=0 → always use cache; temperature=2 → always bypass cache
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=1.0,
    messages=[{"role": "user", "content": "what's github"}],
)
```

## Benefits

- **Lower costs** — Cached responses don't hit the LLM API, reducing token usage and request counts.
- **Faster responses** — Cache hits are near-instant compared to LLM generation time.
- **Better scalability** — Handles higher query throughput without hitting rate limits.
- **Dev/test friendly** — Mock LLM responses locally without any API calls.

## How It Works

LLMCache converts queries into vector embeddings and stores them in a vector database. On a new query, it performs a similarity search — if a sufficiently similar query exists in cache, the cached response is returned directly without calling the LLM.

Performance is measured by three metrics:
- **Hit Ratio** — how often queries are served from cache
- **Latency** — time to retrieve a cached response
- **Recall** — proportion of cacheable queries actually served from cache

## Modules

- **LLM Adapter** — Unified interface supporting OpenAI, LangChain, Llama.cpp, Dolly, and more.
- **Embedding Generator** — Converts queries to embeddings. Supports ONNX, HuggingFace, Cohere, FastText, SentenceTransformers, and more.
- **Cache Storage** — Stores LLM responses. Supports SQLite, PostgreSQL, MySQL, DynamoDB, and more.
- **Vector Store** — Similarity search over embeddings. Supports FAISS, Milvus, Chroma, Qdrant, Weaviate, and more.
- **Cache Manager** — Controls storage + eviction (LRU, FIFO, LFU, RR). Supports in-memory and distributed (Redis/Memcached) caching.
- **Similarity Evaluator** — Determines if a cached result matches the new query using vector distance, exact match, or model-based scoring.

## License

[MIT](LICENSE)
