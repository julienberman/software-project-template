# AGENTS

This file defines mandatory operating rules for any coding agent working in this repository.


## Project Overview

[PROJECT OVERVIEW GOES HERE]

## Architecture

### Stack overview
- Frontend: Next.js App Router, TypeScript, Clerk, Shadcn, TanStack Query, Tailwind CSS
- Backend: FastAPI, Pydantic.
- Database: MongoDB database, Redis cache.
- Deployment: Railway

## Documentation

### Definitions 
- `docs/commands.md` - contains a detailed description of each command.
- `docs/style.md` - contains naming rules, file conventions, layering expectations, and code style requirements.
- `docs/decisions.md` - contains reverse chronological architecture decisions with date, rationale, and impact.
- `docs/directory_structure.md` - contains the canonical ascii file tree and purpose of each directory.

### Maintenance policy

Docs must be meticulously maintained. Any change that affects the structure, behavior, setup, boundaries, database configuration, or tests requires corresponding docs updates in the same work item. No stale docs are allowed.

For each task, explicitly evaluate doc impact and do one of the following:

1. Update relevant files in `docs/`.
2. State clearly that there is no doc impact and why.

When architecture or policy decisions change, record them in `docs/decisions.md`, which should be in reverse chronological order (newest at top).
