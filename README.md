# Software Project Template

This repository is a full-stack template with a minimal working scaffold:
- Next.js frontend (`frontend/`)
- FastAPI backend (`backend/`)
- Postgres database

## Quickstart

1. Click `Use this template` on Github.
2. Clone your new repository.
3. Run the rename script from the repository root:

```bash
./init_template.sh your-project-slug
```

3. Copy environment variables:

```bash
cp .env.example .env
rm .env.example
```

4. Set additional environment variables in `.env`

5. Write `README.md`

6. Write `AGENTS.md`

## The `init_template.sh` script

Throughout this template, the tokens `software-project-template` and `software_project_template` are used as stand-ins for the actual project name. In addition, the `README.md` and `AGENTS.md` files include information _about the template repository_, and should be replaced with information about the actual project. The `init_template.sh` script:
- Replaces `software-project-template` and `software_project_template` in all project files (except generated and binary files) with the slug you pass.
- Replaces `README.md` and `AGENTS.md` with blank files.

## Local Development

The following command manage the services for local development:
- `docker compose up` -> launches the docker containers from the images of each service specified in `compose.yml`
    -`--build` -> forces docker to recreate the images of each service
    -`--watch` -> tells docker to launch the containers with the `develop.watch` rules specified in `compose.yml`
    -`-d` -> tells docker containers to launch the containers in "detached" mode, which gives back the terminal
- `docker compose ps` -> see running containers
- `docker compose exec <SERVICE_NAME> bash` -> Open a shell inside a running service container
- `docker compose down` -> tears down all running docker containers

## Production

Here are instructions for deploying the app on Railway:

1) Create new project from Railway dashboard.

2) Click `GitHub Repository`

3) Create services for frontend, backend, and postgres

4) Set frontend environment variables:
```
BACKEND_URL=https://${{backend.RAILWAY_PRIVATE_DOMAIN}}:${{backend.BACKEND_PORT}}
FRONTEND_HOSTNAME=0.0.0.0
FRONTEND_PORT=3000
```

5) Set backend environment variables:
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
BACKEND_HOSTNAME=0.0.0.0
BACKEND_PORT=8000

BLS_API_KEY=api_key_goes_here
```

6) In `settings` for both the `frontend` and `backend` Railway services, select `Add root directory` and add the `frontend/` and `backend/` directories respectively. Check `Wait for CI` and `Enable serverless`.

7) In the `frontend` service, click `Variables` > `6 variables added by Railway` and copy the `RAILWAY_SERVICE_ID`. Then, in `frontend/Dockerfile`, replace this line:
```
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    if [ -f pnpm-lock.yaml ]; then \
        corepack enable pnpm && pnpm install --frozen-lockfile; \
    else \
        echo "No lockfile found." && exit 1; \
    fi

```
with
```
RUN --mount=type=cache,target=/root/.local/share/pnpm/store,id=s/railway_service_id \
    if [ -f pnpm-lock.yaml ]; then \
        corepack enable pnpm && pnpm install --frozen-lockfile; \
    else \
        echo "No lockfile found." && exit 1; \
    fi
```

8) To access both the `frontend` and `backend` URLs, navigate to `settings` and click `Generate domain` under `Public networking`.

9) To create a custom domain... [TODO]

## More info about the Docker setup
The app is built using Dockerfiles. The Dockerfile is the recipe for a given service. It contains instructions for building an _image_ of that service from the code. When this image is run, it is called a _container_. In production, Railway runs each service from its dockerfile, and Railway provides the networking, environment variables, databases, etc. In development, `docker compose` orchestrates the networking, environment variables, databases, etc.

### Backend
- `Dockerfile` -> Contains the instructions for building the _production_ backend service. This is the template that Railway uses.
    - Starts from the official python 3.11 slim image
    - Installs `uv` in the container
    - Creates a `backend` directory in the container
    - Copies backend dependencies to the `backend` directory in the container
    - Copies source code to the `backend` directory in the container
    - Command to run the backend service at the hostname and port set in the `.env` file
- `Dockerfile.dev` -> Contains the isntructions for building the _development_ backed service. This is the template that compose.yml uses for the local network.
    - Same instructions as `Dockerfile`
    - Now, the command to run the backend service includes a `--reload` flag. This tells uvicorn to monitor the source code inside the container and reload if there are any changes.

### Frontend
- `Dockerfile` -> Contains the instructions for building the _production_ frontend service. This is the template that Railway uses.
    - Phase 1:
        - Starts from the latest official node.js image
        - Installs dependencies for the frontend service.
        - Caches these dependencies, so that if the source code changes, but `package.json` and `pnpm-lock.yaml` do not, Docker can reuse the dependency-install layer rather than reinstalling dependencies.
    - Phase 2:
        - Starts from the latest official node.js image
        - Copies installed depndencies from Phase 1 filesystem
        - Copies frontend source code
        - Executes `pnpm build`, which runs the build script in `package.json`. This _compiles_ the frontend source code, and creates an optimized production build under the `.next/` folder. This Dockerfile expects the option `output: standalone` to be set in `next.config.ts`. If it is, `.next/standalone` contains a minimaproduction version of the frontend service.
    - Phase 3:
        - Starts from the latest official node.js image
        - Copies public assets from Phase 2 filesystem
        - Copies standalone app from Phase 2 filesystem
        - Command to run the standalone server at the hostname and port set in the `.env` file
- `Dockerfile.dev` -> Contains the instructions for building the _development_ frontend service. This is the template that `compose.yml` uses.
    - Starts from thelatest official node.js image
    - Installs dependencies for the frontend service
    - Caches these dependencies, so that if the source code changes, but `package.json` and `pnpm-lock.yaml` do not, Docker can reuse the dependency-install layer rather than reinstalling dependencies.
    - Copies frontend source code
    - Command to execute `pnpm dev` at the hostname and port set in the `.env` file, which runs the development script in `package.json`. This compiles the frontend source code in _development mode_, which monitors the source code inside the container and recompiles if there are any changes. 

### Docker compose
- Database
    - Starts a `postgres` container from its official image. Not built from source code.
    - Initializes the database name, user, and password
    - Stores data in a named docker volume. Ensures that tearing down the container does not delete the data in the database. Maps all data written to `var/lib/postgresql/data` into the volume called `database_data`. On Linux, this volume is stored in `/var/lib/docker/volumes`. On MacOS, it is stored somewhere in a Linux VM that Docker Desktop manages.
- Backend
    - Builds `backend` image from `./backend/Dockerfile.dev`. Notice that this is the _development_ version, which allows for hot-reload.
    - Waits for the database healthcheck before starting
    - Loads variables from `.env` into the `backend` container environment
    - Connects the port of the local machine (specified in `.env`) to the same port in the `backend` container. So if I visit `https://localhost:${PORT}`, Docker forwards that request into the `backend` container.
    - If the `--watch` flag is specified, add the following two functions:
        - `sync` -> When files under `./backend` change on the host, copy them to `/backend` in the container. This allows uvicorn to trigger a reload.
        - `rebuild` -> If `uv.lock` changes, rebuild and recreate the service
- Frontend
    - Builds `frontend` image from `./frontend/Dockerfile.dev`. Notice that this is the _development_ version, which allows for hot-reload.
    - Waits for `backend` to start before starting
    - Loads variables from `.env` into the `frontend` container environment
    - Connects the port of local machine (specified in `.env`) to the same port in the `frontend` container. So if I visit `https://localhost:${PORT}`, Docker forwards that request into the `frontend` container.
    - If the `--watch` flag is specified, add the following two functions:
        - `sync` -> When files under `./frontend` change on the host, copy them to `/frontend` in the container. This allows `pnpm dev` to trigger a reload.
        - `rebuild` -> If `pnpm-lock.yaml` changes, rebuild and recreate the service

### .dockerignore
This file specifies which files should be removed from the build context. E.g. `__pycache__/` will not be copied into the image if it is in the relevant `.dockerignore`.

