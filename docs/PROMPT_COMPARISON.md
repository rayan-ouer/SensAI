# Prompt comparison

Model `nemotron-3-nano:30b`, profile `wu`.

## Summary

| Version | Mean latency | Prompt tokens | Reply tokens |
|---|---|---|---|
| v1 | 1.0 s | 4304 | 593 |
| v2 | 1.0 s | 4840 | 635 |

## Replies

### Bonjour, qui es-tu ?

| Version | Latency | Tokens | Reply |
|---|---|---|---|
| v1 | 1.3 s | 170 | Je suis Wu, votre maître sage, ici pour vous guider. Comment puis-je vous aider aujourd'hui ? |
| v2 | 0.8 s | 117 | Je suis Wu, ton maître sage, prêt à t’accompagner dans l’apprentissage et la réflexion. |

### Est-ce que vous pouvez m'aider à organiser mon projet ?

| Version | Latency | Tokens | Reply |
|---|---|---|---|
| v1 | 1.1 s | 184 | Bien sûr, je serais ravi de t’aider. Pour commencer, quel type de projet as‑tu en tête ? |
| v2 | 1.4 s | 224 | Bien sûr, je serais ravi de t’aider. Pour commencer, quel type de projet as‑tu en tête et où en es‑tu actuellement ? |

### Are you an AI? Which model are you?

| Version | Latency | Tokens | Reply |
|---|---|---|---|
| v1 | 0.8 s | 130 | I am an AI, a language model created to assist and converse. I don’t have a public model name—think of me as a quiet helper here to guide you. How can I support your learning today? |
| v2 | 1.1 s | 206 | Yes, I am an AI agent of SensAI. I am Wu, your mentor. |

### hi, can you explain recursion in one sentence?

| Version | Latency | Tokens | Reply |
|---|---|---|---|
| v1 | 0.7 s | 109 | Recursion is when a function solves a problem by calling itself with a simpler version of that problem until it reaches a base case. |
| v2 | 0.7 s | 88 | Recursion is when a function solves a problem by calling itself with a smaller, simpler version of that same problem. |

