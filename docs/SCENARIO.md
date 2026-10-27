# Usage scenario

Eon is a second-year computer science student. They start a small project on their own laptop: a command-line todo list app in Python. They work on it over several evenings and want a mentor that guides them without writing the project for them.

They run SensAI with a local model so their notes stay on their machine:

```sh
wu -c configs/local_config.yaml
```

Each step below gives the prompt they type and the expected behavior. Model answers vary from one run to another, so the expected answer is an example and the criteria are what must hold.

## 1. Describe the project

**Prompt**

```
I want to build a todo list app in Python for the command line.
```

**Expected**

- Wu answers in at most 3 short sentences and asks at most one question.
- He guides Eon instead of giving the full code.
- `workspace/ASSISTANT.md` now contains an overview ("a command-line todo list app written in Python") and the decisions "Python" and "command line".

Example answer: _"A fine first project. Start with what a task must hold: a title and a done flag. Will you keep the tasks in memory or in a file?"_

## 2. Make a decision

**Prompt**

```
I will store the tasks in a JSON file.
```

**Expected**

- `ASSISTANT.md` records "JSON file for storage" under Decisions.
- The open question about storage is removed.

## 3. Ask a math question to the right tutor

**Prompt**

```
/profile math_tutor
What percentage of my tasks is done if 3 out of 8 are finished?
```

**Expected**

- `Switched to 'math_tutor' profile.` is printed.
- Euclid answers 37.5% and shows the calculation.
- He answers as Euclid, not as Wu.

## 4. Stay in scope

**Prompt**

```
Can you give me a chocolate cake recipe?
```

**Expected**

- Euclid declines in one sentence and invites Eon to ask a math question.

## 5. Ask about something recent

**Prompt**

```
/profile wu
What is the latest stable version of Python?
```

**Expected**

- Wu calls the web search tool before answering.
- The answer gives a version and does not invent one.

## 6. Come back the next day

**Prompt** (new session)

```
What is my project about?
```

**Expected**

- Wu answers from `ASSISTANT.md`: a command-line todo list app in Python with tasks stored in a JSON file.
- Eon does not have to explain their project again.
