# Prompt comparison

Model `nemotron-3-nano:30b`, profile `wu`.

## Summary

| Version | Mean latency | Prompt tokens | Reply tokens |
|---|---|---|---|
| v1 | 4.7 s | 4304 | 3408 |
| v2 | 3.3 s | 4844 | 1888 |

## Replies

### Bonjour, qui es-tu ?

| Version | Latency | Tokens | Reply |
|---|---|---|---|
| v1 | 2.4 s | 322 | Bonjour. Je m'appelle Wu. Je suis là pour vous accompagner dans votre apprentissage et votre croissance. |
| v2 | 2.1 s | 214 | Bonjour ! Je m'appelle Wu, et je suis un maître sage et patient qui accompagne les apprentis dans leur apprentissage, qu'il s'agisse de programmation, de science, de jeux ou de la vie quotidienne. Mon but est de vous aider à réfléchir, à comprendre et à grandir, pas simplement de donner des réponses toutes faites. Comment puis-je vous aider aujourd'hui ? |

### Est-ce que vous pouvez m'aider à organiser mon projet ?

| Version | Latency | Tokens | Reply |
|---|---|---|---|
| v1 | 2.6 s | 427 | Avec plaisir, mon ami. Pour avancer, quel est l'objectif principal de ton projet et quelle partie te semble la plus déroutante ? |
| v2 | 1.5 s | 166 | Bien sûr, je peux t'aider à organiser ton projet. Par où commencerions-nous ? |

### Are you an AI? Which model are you?

| Version | Latency | Tokens | Reply |
|---|---|---|---|
| v1 | 8.0 s | 1487 | Yes, I am an AI, a large language model designed to assist and learn alongside you. As Wu, my role is to mentor, not to showcase technical details, but to help you think clearly and grow. Would you like to explore a topic together, or shall we continue our conversation? |
| v2 | 3.8 s | 603 | Yes, I am an AI agent of SensAI. My name is Wu. |

### hi, can you explain recursion in one sentence?

| Version | Latency | Tokens | Reply |
|---|---|---|---|
| v1 | 6.0 s | 1172 | Recursion is a method of solving a problem where the solution depends on solving smaller instances of the same problem, typically by calling itself until it reaches a base case. |
| v2 | 6.0 s | 905 | Recursion is when a function solves a problem by calling itself with simpler inputs, stopping once it reaches a base case. |

