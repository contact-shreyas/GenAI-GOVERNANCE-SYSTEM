# Multi-stage build for optimized Next.js production and development
# Stage 1: Builder - install dependencies and build
FROM node:20-alpine AS builder

WORKDIR /app

# Enable Corepack for pnpm support
RUN corepack enable && corepack prepare pnpm@8.15.4 --activate

ENV NODE_ENV=development

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies using pnpm
RUN pnpm install --frozen-lockfile --ignore-scripts

# Copy source code
COPY . .

# Build Next.js application
RUN pnpm run build


# Stage 2: Runtime - minimal production image
FROM node:20-alpine AS runtime

WORKDIR /app

# Enable Corepack for pnpm
RUN corepack enable && corepack prepare pnpm@8.15.4 --activate

ENV NODE_ENV=production

# Copy package files and lockfile
COPY package.json pnpm-lock.yaml* ./

# Install only production dependencies
RUN pnpm install --prod --frozen-lockfile --ignore-scripts

# Copy built application from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY next.config.js ./

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 && \
    chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Run application
CMD ["pnpm", "start"]
