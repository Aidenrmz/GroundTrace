# Security Policy

GroundTrace is a local development tool for inspecting RAG traces. It is not designed to be exposed directly to the public internet.

## Supported Versions

| Version | Status |
| --- | --- |
| 0.1.x | Active support |

## Reporting A Vulnerability

Do not disclose security issues in a public issue. Report them privately to the project maintainers through your normal repository security channel.

Include:

- A clear description of the issue.
- Reproduction steps or a minimal proof of concept.
- Expected impact.
- Suggested mitigation if you have one.

The goal is to acknowledge reports quickly, validate the problem, agree on disclosure timing, and ship a fix.

## Security Model

- Default bind address: `127.0.0.1`.
- Intended use: local development or a trusted internal machine.
- Data captured: prompts, retrieved chunks, LLM responses, metadata, and attribution results.
- Default storage: in-memory session state plus browser `localStorage` cache for summaries/history.
- Authentication: not included for local-only usage.

## Operational Guidance

### Keep The Dashboard Local

```python
import groundtrace

groundtrace.serve(host="127.0.0.1", port=7756)
```

Avoid binding to all interfaces unless you add your own network restrictions and authentication:

```python
groundtrace.serve(host="0.0.0.0", port=7756)  # only behind explicit controls
```

### Protect API Keys

GroundTrace does not intentionally store provider API keys. Keep keys in environment variables or a credential manager and avoid placing them in prompts, metadata, or documents.

```python
import os

api_key = os.getenv("OPENAI_API_KEY")
```

### Treat Sessions As Sensitive

Traces can contain proprietary prompts, retrieved documents, and generated answers. Do not share exports or screenshots unless the underlying content is safe to disclose.

### Audit Dependencies

The package depends on common Python web and ML libraries such as FastAPI, Uvicorn, httpx, NumPy, and sentence-transformers. Use your standard dependency scanner:

```bash
pip install pip-audit
pip-audit
```

## Known Risk Areas

- Streaming parsers must stay bounded so malformed server-sent events cannot consume excessive memory.
- Embedding very large outputs can create CPU and RAM spikes before model truncation applies.
- Session retention is bounded, but very large prompts and chunks still increase process memory.
- WebSocket Origin checks are required because browser CORS rules do not protect WebSocket endpoints.
- Transport-level interception observes matching `httpx` traffic and must be kept conservative about which hosts are treated as LLM providers.

## Hardening Checklist

- Leave the server on localhost for day-to-day debugging.
- Use a private network, reverse proxy authentication, and TLS before sharing a dashboard.
- Clear sessions after investigating sensitive traces.
- Keep dependencies patched.
- Review custom interceptors before enabling them in shared environments.
