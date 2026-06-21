# Commands
Commands must be run from the repository root.


## Validation Policy

- Docker compose is the required execution path for validation commands.
- Launch containers before running diagnostic commands
- Run lint, typecheck, tests, and format checks through already running service containers.


## Launch
- `docker compose up --watch -d` -> start the database, backend, and frontend with sync functionality in detached mode
- `docker compose ps` -> see running containers
- `docker compose exec <SERVICE_NAME> bash` -> Open a shell inside a running service container
- `docker compose logs -f <SERVICE_NAME>` -> Open the logs of a service container
- `docker compose down` -> tear down all running docker containers


## Template Initialization

- `./init_template.sh <project-slug>` -> replace template slugs, stamp the initial decision date, and generate the project README


## Backend
- `docker compose exec backend uv run ruff check .` -> run backend lint checks
- `docker compose exec backend uv run ruff format --check .` run backend format checks
- `docker compose exec backend uv run mypy app` -> run backend type checks


## Frontend

- `docker compose exec frontend pnpm lint` -> run frontend lint checks
- `docker compose exec frontend pnpm format:check` -> run frontend format checks
- `docker compose exec frontend pnpm typecheck` -> run frontend type checks
