import { withMermaid } from 'vitepress-plugin-mermaid'
import sidebar from './sidebar.json'

export default withMermaid({
  title: 'Software Factory Manifesto',
  description:
    'Best practices for a fully automated software factory where AI agents turn requests into merged, verified changes.',
  base: '/software-factory-manifesto/',
  srcDir: 'content',
  cleanUrls: true,
  lastUpdated: true,
  head: [['meta', { name: 'theme-color', content: '#7c3aed' }]],
  markdown: { lineNumbers: false },
  themeConfig: {
    nav: [
      { text: 'Follow a request', link: '/docs/00-journey/' },
      { text: 'Manifesto', link: '/manifesto' },
      { text: 'Rules', link: '/RULES' },
      { text: 'Start your factory', link: '/docs/09-adoption/build-order' },
    ],
    sidebar,
    outline: { level: [2, 3], label: 'On this page' },
    search: { provider: 'local' },
    socialLinks: [{ icon: 'github', link: 'https://github.com/icelink-ai/software-factory-manifesto' }],
    editLink: {
      pattern: 'https://github.com/icelink-ai/software-factory-manifesto/tree/main/',
      text: 'View the source on GitHub',
    },
    footer: {
      message: 'Licensed under CC BY 4.0.',
      copyright: 'Written for AI agents and the people who run them.',
    },
  },
  mermaid: { securityLevel: 'loose' },
})
