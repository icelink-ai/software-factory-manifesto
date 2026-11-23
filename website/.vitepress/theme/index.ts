import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import './style.css'

// Click any diagram to open it full screen; click again or press Escape to close.
function enableDiagramZoom() {
  if (typeof document === 'undefined') return
  document.addEventListener('click', (event) => {
    const target = event.target as HTMLElement
    if (target.closest('a')) return
    const diagram = target.closest('.mermaid') as HTMLElement | null
    if (!diagram || diagram.closest('.diagram-overlay')) return
    const overlay = document.createElement('div')
    overlay.className = 'diagram-overlay'
    overlay.setAttribute('role', 'dialog')
    overlay.setAttribute('aria-label', 'Diagram, full screen. Click or press Escape to close.')
    const inner = document.createElement('div')
    inner.className = 'diagram-overlay-inner mermaid'
    inner.innerHTML = diagram.innerHTML
    overlay.appendChild(inner)
    const close = () => {
      overlay.remove()
      document.removeEventListener('keydown', onKey)
    }
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && close()
    overlay.addEventListener('click', close)
    document.addEventListener('keydown', onKey)
    document.body.appendChild(overlay)
  })
}

export default {
  extends: DefaultTheme,
  enhanceApp() {
    enableDiagramZoom()
  },
} satisfies Theme
