// next.config.js — Next.js config. Standalone output for slim Docker image on ECS Fargate. Ch 35 containerized deploy.
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  poweredByHeader: false,
  experimental: {
    serverComponentsExternalPackages: ['pg', 'stripe'],
  },
};

module.exports = nextConfig;
