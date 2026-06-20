# Copied from Next.js Dockerfile example at this link:
# https://github.com/kristiyan-velkov/docker-nextjs-sample/blob/3d7cd2d9ab13f19bbba780e095d99f6bdadc89d4/Dockerfile
# Modifications: 
#   - Changed "/app" to "/frontend" to better match local filesystem structure
#   - Added a few additional clarifying comments
#   - Added explicit handling for Railway builds
#   - Removed branching; retained pnpm only

# ============================================
# Stage 1: Dependencies Installation Stage
# ============================================

# IMPORTANT: Node.js Version Maintenance
# This Dockerfile uses Node.js 24.13.0-slim, which was the latest LTS version at the time of writing.
# To ensure security and compatibility, regularly update the NODE_VERSION ARG to the latest LTS version.
ARG NODE_VERSION=24.13.0-slim

# Define dependencies stage
FROM node:${NODE_VERSION} AS dependencies

# Set working directory
WORKDIR /frontend

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json pnpm-lock.yaml* ./

# Install project dependencies with frozen lockfile for reproducible builds
# NOTE: If using railway, must add id=... to the mount flag
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    if [ -f pnpm-lock.yaml ]; then \
        corepack enable pnpm && pnpm install --frozen-lockfile; \
    else \
        echo "No lockfile found." && exit 1; \
    fi

# ============================================
# Stage 2: Build Next.js application in standalone mode
# ============================================

# Define builder stage
FROM node:${NODE_VERSION} AS builder

# Set working directory
WORKDIR /frontend

# Copy project dependencies from dependencies stage filesystem
COPY --from=dependencies /frontend/node_modules ./node_modules

# Copy application source code
COPY . .

ENV NODE_ENV=production

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
# ENV NEXT_TELEMETRY_DISABLED=1

# Build Next.js application
# If you want to speed up Docker rebuilds, you can cache the build artifacts
# by adding: --mount=type=cache,target=/app/.next/cache
# This caches the .next/cache directory across builds, but it also prevents
# .next/cache/fetch-cache from being included in the final image, meaning
# cached fetch responses from the build won't be available at runtime.
RUN if [ -f pnpm-lock.yaml ]; then \
        corepack enable pnpm && pnpm build; \
    else \
        echo "No lockfile found." && exit 1; \
    fi


# ============================================
# Stage 3: Run Next.js application
# ============================================

# Define runner stage
FROM node:${NODE_VERSION} AS runner

# Set working directory
WORKDIR /frontend

# Set production environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the run time.
# ENV NEXT_TELEMETRY_DISABLED=1

# Copy production assets from builder stage filesystem
COPY --from=builder --chown=node:node /frontend/public ./public

# Set the correct permissions for prerender cache
RUN mkdir .next
RUN chown node:node .next

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=node:node /frontend/.next/standalone ./
COPY --from=builder --chown=node:node /frontend/.next/static ./.next/static

# If you want to persist the fetch cache generated during the build so that
# cached responses are available immediately on startup, uncomment this line:
# COPY --from=builder --chown=node:node /frontend/.next/cache ./.next/cache

# Switch to non-root user for security best practices
USER node

# Expose port 3000 to allow HTTP traffic
EXPOSE 3000

# Start Next.js standalone server
CMD ["node", "server.js"]

