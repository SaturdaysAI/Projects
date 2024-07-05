/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export',
    distDir: 'dist',
    assetPrefix: './',
    reactStrictMode: true,
    webpack(config, { isServer }) {
        if (!isServer) {
          config.resolve = {
              ...config.resolve,
              fallback: {
                  net: false,
                  dns: false,
                  tls: false,
                  assert: false,
                  path: false,
                  fs: false,
                  events: false,
                  process: false
              }
          };
        }

        return config;
      }
};

export default nextConfig;
