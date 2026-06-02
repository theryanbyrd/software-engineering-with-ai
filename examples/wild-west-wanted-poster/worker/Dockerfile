# Dockerfile — Multi-stage build for the wwwp SQS worker (Node 20, Alpine).
# Book chapter concept: "Shipping the worker as an immutable container" — same artifact in CI,
# staging, and ECS Fargate. sharp needs native libs (libvips), so we install them at build time
# and carry the runtime ones into the slim final image.

# ---- deps: install ALL deps (incl. dev) so we can compile TypeScript ----
FROM node:20-alpine AS deps
WORKDIR /app
# Build toolchain + libvips headers so `sharp` can build/verify its native bindings.
RUN apk add --no-cache python3 make g++ vips-dev
COPY package.json package-lock.json* ./
RUN npm ci || npm install

# ---- build: compile TS -> JS into dist/ ----
FROM node:20-alpine AS build
WORKDIR /app
RUN apk add --no-cache vips-dev
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# ---- prod-deps: production-only node_modules ----
FROM node:20-alpine AS prod-deps
WORKDIR /app
RUN apk add --no-cache python3 make g++ vips-dev
COPY package.json package-lock.json* ./
RUN (npm ci --omit=dev || npm install --omit=dev)

# ---- runtime: minimal image with only runtime libs ----
FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
# Runtime shared library for sharp (no -dev headers needed at runtime).
RUN apk add --no-cache vips
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./
# Run as the unprivileged node user baked into the base image.
USER node
CMD ["node", "dist/index.js"]
