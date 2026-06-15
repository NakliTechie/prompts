---
description: Launch the project for a live demo — boot it with the shared demo-seed data (the same asset /walkthrough-nt and /guide-nt use), and generate + open an interactive showcase (what's built · features · dependencies · status) with a button into the running app. For demoing work-in-progress to customers or execs.
argument-hint: "[focus: seed | showcase | launch]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Edit", "Write", "Task"]
---

A presenter's launcher for live demos. When you need to show work-in-progress to a customer or a senior exec, `/demo-nt` does two things: boots the real app **seeded and ready** (no empty-state fumbling in front of the room), and builds + opens an **interactive showcase** — a one-glance "here's what we've built so far" (features · dependencies · status) with a button straight into the running app.

Where `/guide-nt` *documents* how to use features and `/ux-review-nt` *critiques* the cold newcomer path, `/demo-nt` is **presenter mode**: the app is running, seeded, and the story is on one page.

If the project has no runnable surface, say so. If the current directory isn't a git repo, ask which project — don't guess. `$ARGUMENTS` (optional): `seed`, `showcase`, or `launch` to run just that part.

## Phase 1 — The shared demo seed (the load-bearing asset)

The demo data is **one canonical asset — `demo/seed/`** — that `/walkthrough-nt`, `/guide-nt`, and `/demo-nt` all load. Locate it, or scaffold it: the data files + a small loader the app can call (the way Bahi loads a sample `.khata`, or LocalMind seeds IndexedDB + injects sample content).
- It's **committed and grows with the app**: every new feature extends the seed, so a demo never lands on an empty or half-built screen, and all three commands stay current automatically.
- If `/walkthrough-nt` or `/guide-nt` already injects seed data ad-hoc, **promote that into `demo/seed/`** so the three share one source instead of drifting apart. (`/ux-review-nt` is the deliberate exception — it wipes state to test the cold newcomer.)

## Phase 2 — Boot the app, seeded and ready

Start the app and get it demo-ready:
- **Production build, in a real browser** — this is a *live* demo on your machine, so run it where the audience will see it (a real GPU browser — **WebGPU works here**, unlike the headless capture commands).
- Load `demo/seed/`, and land on the **best opening screen** — the one that tells the story fastest, not a blank dashboard.
- **Confirm it's actually ready** — no console errors, data populated, the key flows click through. A demo that breaks in front of an exec is exactly the failure this command exists to prevent; rehearse the happy path once.

## Phase 3 — Build the showcase (`demo/showcase.html`)

An interactive, single self-contained page — the "trailer," not a full guide:
- **What's built** — the features/surfaces that actually exist (derive from routes / components / the README), grouped, each with a one-line *value* statement (what it does for the user, not how it's coded). Honestly mark **shipped vs in-progress** — it's a WIP demo, so set expectations rather than overclaim.
- **Stack / dependencies** — the real stack from the manifests, for the technical execs in the room.
- **Status** — a high-level progress read (feature counts, what shipped recently). **Curated, never a raw `plan/` dump** — `plan/` is private working notes (dead ends, strategy); pull only the public-safe signal.
- **Launch** — a prominent button/link into the **running app** from Phase 2, plus a link to the `/guide-nt` guide if one exists and the live/demo URL.
- **Polished and exec-ready** — clean, built from the app's own `:root` design tokens (like `/guide-nt`), no dev chrome. This is the first thing the room sees.

## Phase 4 — Present + open

Serve and open `demo/showcase.html`; confirm the **Launch** button reaches the seeded app. Print: what's seeded, the showcase path, and the live app URL — so you can pull it all up in one move when the meeting starts.

**Privacy:** the showcase is committed (`demo/`, so it evolves with the app), but **curated for the audience** — the built-and-coming story, not the internal kitchen. If the repo is public or the WIP is sensitive, keep `demo/showcase.html` local instead (gitignore it) — it's a one-line change.

End by naming the opening screen and noting the seed is now shared with `/walkthrough-nt` and `/guide-nt`.
