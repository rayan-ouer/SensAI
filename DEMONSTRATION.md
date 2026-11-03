# Démonstration

Chaque lien ouvre la vidéo de la fonctionnalité correspondante du catalogue.

## Memory & Context

### [M4] Artifact & State Document

Le panneau Specification se met à jour après la description du projet.

[03-specification.webm](demos/03-specification.webm)

## Tools

### [T1] MCP

Un serveur MCP externe, `mcp-server-time`, est lancé au démarrage. Wu appelle `get_current_time` pour l'heure à Paris.

[18-mcp-externe.webm](demos/18-mcp-externe.webm)

### [T2] Sandboxed Code Execution

Ada exécute `date` dans le sandbox et cite la date renvoyée.

[12-sandbox.webm](demos/12-sandbox.webm)

### [T3] Web Search

Iris répond à la question sur la dernière version stable de Python.

[06-recherche-web.webm](demos/06-recherche-web.webm)

### [T4] File Access within Permissions

Ada confirme le dossier de travail, puis lit `README.md`.

[13-fichiers.webm](demos/13-fichiers.webm)

### [T5] Structured Output

L’agent critic répond avec un objet JSON : `verdict`, `summary`, `issues`.

[19-structured-output.webm](demos/19-structured-output.webm)

## RAG

### [R2] Advanced RAG

Un JSON est refusé, une note Markdown est indexée, puis la réponse s’appuie sur le passage retrouvé.

[07-documents.webm](demos/07-documents.webm)

## Orchestration & Reasoning

### [A1] Reasoning Loops (ReAct)

Iris enchaîne trois recherches : le Nobel de physique 2025, puis le laboratoire du nom trouvé, puis le résultat récompensé.

[04-reponse.webm](demos/04-reponse.webm)

### [A2] Multi-Agent Orchestration

`wu -m agents/agent.yaml`. Le coordinateur délègue à l’agent `analyst`.

[11-multi-agent.webm](demos/11-multi-agent.webm)

### [A3] Human-in-the-Loop

Avant d’écrire un fichier, l’agent demande `[y/N]`. La réponse `n` annule l’écriture.

[14-approbation.webm](demos/14-approbation.webm)

### [A4] Prompt Versioning

Démarrage avec les prompts v4, puis avec v1.

[15-versions.webm](demos/15-versions.webm)

`wu-compare` envoie le même message aux versions v1 et v2 et affiche latence et score.

[16-comparaison.webm](demos/16-comparaison.webm)

### [A5] Persona

Bascule entre Wu, Euclid, Sensei, Ada, Mira et Iris.

[01-profils.webm](demos/01-profils.webm)

## Evaluation

### [EV1] Automated Eval & Hallucination Detection

Les scores du juge pour v1 et v2, dans la même prise que la comparaison de prompts.

[16-comparaison.webm](demos/16-comparaison.webm)

### [EV3] Logging & Monitoring Dashboard

Compteurs, courbes, puis une trace `search_web` et une trace `human_in_the_loop`.

[10-monitoring.webm](demos/10-monitoring.webm)

## UX & Lifecycle

### [X1] Web UI

Choix du modèle dans l’en-tête.

[02-modeles.webm](demos/02-modeles.webm)

Nouvelle conversation, puis une nouvelle saisie.

[09-nouvelle-conversation.webm](demos/09-nouvelle-conversation.webm)

### [X2] Branching — Resume & Interrupt

« Dis bonjour. » est réécrit en « Dis bonsoir en trois mots. », et la réponse repart de là.

[08-edition.webm](demos/08-edition.webm)

### [X4] Questions & Forms

Dans le navigateur, la question s’affiche avec un bouton par option.

[05-questions.webm](demos/05-questions.webm)

Dans le terminal, le même choix est un menu numéroté, avec « Other free-form answer ».

[17-questions-cli.webm](demos/17-questions-cli.webm)
