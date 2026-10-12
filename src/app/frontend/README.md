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

```
main.tsx              entry point, mounts App
App.tsx               background + page, with the loader while the page loads
index.css             Tailwind and the shadcn/ui theme

pages/                one file per screen
  ChatPage.tsx

components/
  chat/               the pieces of the chat screen (written for this project)
  layout/             background and page loader (written for this project)
  effects/            visual effects copied from React Bits
  ui/                 components added by the shadcn CLI (shadcn/ui, Dot Matrix)

hooks/                state and logic shared by components
  useChat.ts          messages, status, sending

services/             calls to the backend
  chatApi.ts          the only contact point with the API (mocked for now)

types/                types shared across the app
  chat.ts             Message, Role, ChatStatus

lib/                  helpers added by the shadcn CLI
utils/                project helpers
```

Files in `components/ui/`, `components/effects/` and `lib/` come from external libraries.
Each one starts with a comment giving its source. Add or update them with the CLI
(`npx shadcn@latest add <name>`) instead of editing them by hand.

## Connecting the API

The page only depends on `streamReply(messages)` in `services/chatApi.ts`.
Replace its body with the real request; nothing else has to change.
