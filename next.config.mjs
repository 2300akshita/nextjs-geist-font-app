/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*', // Proxy to Backend
      },
      {
        source: '/course',
        destination: 'http://localhost:3000/course'
      }
    ]
  }
}

export default nextConfig;
