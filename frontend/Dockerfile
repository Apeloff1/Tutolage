# ============================================================================
# CodeDock Frontend Dockerfile (Expo)
# ============================================================================

# Stage 1: Dependencies
FROM node:20-alpine as deps

WORKDIR /app

# Copy package files
COPY package.json yarn.lock* package-lock.json* ./

# Install dependencies
RUN if [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    else npm install; fi

# Stage 2: Development
FROM node:20-alpine as development

WORKDIR /app

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Expose Expo ports
EXPOSE 3000 8081 19000 19001 19002

# Start Expo
CMD ["npx", "expo", "start", "--web", "--port", "3000"]

# Stage 3: Web Build
FROM node:20-alpine as builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build for web
RUN npx expo export --platform web

# Stage 4: Production (Nginx for web)
FROM nginx:alpine as production

# Copy built web files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf 2>/dev/null || true

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
