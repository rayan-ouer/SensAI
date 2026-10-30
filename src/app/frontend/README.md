# SensAI frontend

React + TypeScript + Vite, styled with Tailwind CSS and shadcn/ui.

## Commands

```sh
npm install     # once
npm run dev     # http://localhost:5173
npm run lint
npm run build
```

## Where things are

The root only holds configuration (Vite, TypeScript, oxlint, shadcn) and `index.html`.
`public/logo.svg` is the SensAI logo (copied from the repository's `assets/`), used as favicon and on the welcome screen;
`public/avatar.svg` is the same logo without its shield, used as the assistant avatar.
All the code is in `src/`:

```
src/
  main.tsx              entry point, mounts App
  App.tsx               background + page, with the pulsing logo while the page loads

  pages/                one file per screen
    ChatPage.tsx
    MonitoringPage.tsx   local interaction trace and metrics dashboard

  components/
    chat/               the pieces of the chat screen (written for this project)
    spec/               the specification side panel (written for this project)
    layout/             background and page loader (written for this project)
    effects/            visual effects copied from React Bits
    ui/                 components added by the shadcn CLI (shadcn/ui)

  hooks/                state and logic shared by components
    useChat.ts          messages, status, sending, conversation restored after a reload
    useSpec.ts          specification content and update state
    useProfiles.ts      available profiles and the selected one
    useModels.ts        available models and the selected one

  services/             calls to the backend
    chatApi.ts          the only contact point with the API

  types/                types shared across the app
    chat.ts             Message, StreamEvent, Profile, ChatStatus

  lib/                  helpers added by the shadcn CLI

  styles/
    index.css           Tailwind entry, imports the theme
    shadcn-tailwind.css shadcn/ui theme
```

Files in `components/ui/`, `components/effects/`, `lib/` and `styles/shadcn-tailwind.css`
come from external libraries.
Each one starts with a comment giving its source. Add or update them with the CLI
(`npx shadcn@latest add <name>`) instead of editing them by hand.

## Connecting the API

Start the API first (`wu-api`, from the repository root), then `npm run dev`.
In development, Vite forwards `/api` to `http://127.0.0.1:8084`: set `SENSAI_API` to use another address,
or `VITE_API_URL` to call the API directly without the proxy.

`services/chatApi.ts` is the only file that talks to the API:

- `createConversation()` creates a conversation, the first time a message is sent
- `streamReply(conversationId, content, profile, model)` sends a message with the selected profile and model and yields the events of the reply,
  one JSON object per line: `content` and `thinking` chunks, a `question` with its options, then `done` and `spec`,
  or `error`
- `fetchMessages(conversationId)` returns the history shown after a page reload
- `fetchSpec()`, `fetchProfiles()` and `fetchModels()` return the specification, the profiles and the models with
  the default ones

If the API restarted and lost the conversation, the page creates a new one and sends the message again.
