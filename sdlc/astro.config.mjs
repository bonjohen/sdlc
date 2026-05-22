import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://sdlc.johnboen.com',
  base: '/',
  integrations: [sitemap()],
});
