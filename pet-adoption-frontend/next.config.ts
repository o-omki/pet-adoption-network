// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**', // wildcard to accept any host
      },
    ],
  },
};

module.exports = nextConfig;
