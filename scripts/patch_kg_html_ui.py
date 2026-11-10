"""
patch_kg_html_ui.py
===================
Injects the Visual Layout Perspective selector and the 60 FPS animation
transition engine into output/visualizations/statutory_kg_full_web.html.
"""

import os
import sys

HTML_PATH = 'output/visualizations/statutory_kg_full_web.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. UI Control Section to Inject
LAYOUT_UI_HTML = """      <!-- Visual Layout Perspective Selector -->
      <div class="filter-section" style="background: rgba(255, 215, 0, 0.06); border: 1px solid rgba(255, 215, 0, 0.28); border-radius: 8px; padding: 10px; margin-bottom: 4px;">
        <div class="filter-label" style="color: #FFD700; font-weight: 700; display: flex; justify-content: space-between; align-items: center;">
          <span>Visual Layout Perspective</span>
          <span id="active-layout-badge" style="font-size: 10px; background: rgba(255,215,0,0.18); padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">Organic Web</span>
        </div>
        <select id="layout-select" class="filter-dropdown" style="margin-top: 6px; border-color: rgba(255, 215, 0, 0.4); font-weight: 600; color: #FFD700;">
          <option value="repulsion" selected>1. Force-Directed Organic Web (Spring Physics)</option>
          <option value="domain">2. National Domain Topic Constellations (10 Galaxies)</option>
          <option value="hierarchical">3. Vertical Preemption Hierarchy (Top-to-Bottom)</option>
          <option value="concentric">4. Concentric Planetary Orbits (RA 7160 Core)</option>
          <option value="radial">5. Polar / Radial Wedges (Centrality Fan)</option>
        </select>
        <div id="layout-desc" style="font-size: 11px; color: #94a3b8; line-height: 1.4; margin-top: 6px;">
          Spring physics simulation: connected laws cluster organically, high-degree hubs at center, peripheral laws in outer cosmic orbits.
        </div>
      </div>
"""

TARGET_LOC = '      <!-- 2-Law Path & Distance Finder -->'
if 'Visual Layout Perspective Selector' not in html:
    html = html.replace(TARGET_LOC, LAYOUT_UI_HTML + '\n' + TARGET_LOC)
    print("Injected Layout UI control panel.")
else:
    print("Layout UI control panel already present.")

# 2. JavaScript Animation Engine
ANIMATION_JS = """
    // ==========================================
    // Multi-Layout Perspective Transition Engine
    // ==========================================
    let currentLayout = 'repulsion';
    let isAnimatingLayout = false;
    let animStartTime = null;
    const ANIM_DURATION = 900; // 900ms smooth transition

    const LAYOUT_DESCRIPTIONS = {
      'repulsion': 'Spring physics simulation: connected laws cluster organically, high-degree hubs at center, peripheral laws in outer cosmic orbits.',
      'domain': '10 Macro-Domain Galaxies based on national topic models: laws cluster into their respective subject matter solar systems with inter-domain bridge arcs.',
      'hierarchical': 'Vertical Preemption Architecture (Lex Superior): Top = Constitution & Codes, Middle = Republic Acts & Decrees, Bottom = Davao City Local Ordinances.',
      'concentric': 'Planetary Radar Orbits centered on RA 7160 (Local Government Code): core sun radiates through primary national anchors, framework ordinances, to peripheral laws.',
      'radial': 'Multi-polar Centrality Fan: Macro domains arranged angularly, radial distance represents degree centrality and institutional prominence.'
    };

    const LAYOUT_BADGES = {
      'repulsion': 'Organic Web',
      'domain': '10 Galaxies',
      'hierarchical': 'Preemption Hierarchy',
      'concentric': 'Planetary Orbits',
      'radial': 'Polar Fan'
    };

    function transitionToLayout(targetLayout) {
      if (currentLayout === targetLayout && !isAnimatingLayout) return;
      currentLayout = targetLayout;

      const badge = document.getElementById('active-layout-badge');
      if (badge) badge.innerText = LAYOUT_BADGES[targetLayout] || targetLayout;
      const desc = document.getElementById('layout-desc');
      if (desc) desc.innerText = LAYOUT_DESCRIPTIONS[targetLayout] || '';

      for (let i = 0; i < NODES.length; i++) {
        const n = NODES[i];
        n.startX = n.x;
        n.startY = n.y;

        if (targetLayout === 'repulsion') {
          n.targetX = n.xr !== undefined ? n.xr : n.x;
          n.targetY = n.yr !== undefined ? n.yr : n.y;
        } else if (targetLayout === 'domain') {
          n.targetX = n.xd !== undefined ? n.xd : n.x;
          n.targetY = n.yd !== undefined ? n.yd : n.y;
        } else if (targetLayout === 'hierarchical') {
          n.targetX = n.xh !== undefined ? n.xh : n.x;
          n.targetY = n.yh !== undefined ? n.yh : n.y;
        } else if (targetLayout === 'concentric') {
          n.targetX = n.xc !== undefined ? n.xc : n.x;
          n.targetY = n.yc !== undefined ? n.yc : n.y;
        } else if (targetLayout === 'radial') {
          n.targetX = n.xw !== undefined ? n.xw : n.x;
          n.targetY = n.yw !== undefined ? n.yw : n.y;
        }
      }

      animStartTime = performance.now();
      isAnimatingLayout = true;
      requestAnimationFrame(stepLayoutAnimation);
    }

    function easeOutCubic(t) {
      return 1 - Math.pow(1 - t, 3);
    }

    function stepLayoutAnimation(timestamp) {
      if (!isAnimatingLayout) return;
      const elapsed = timestamp - animStartTime;
      const t = Math.min(1.0, elapsed / ANIM_DURATION);
      const easeT = easeOutCubic(t);

      for (let i = 0; i < NODES.length; i++) {
        const n = NODES[i];
        n.x = n.startX + (n.targetX - n.startX) * easeT;
        n.y = n.startY + (n.targetY - n.startY) * easeT;
      }

      render();

      if (t < 1.0) {
        requestAnimationFrame(stepLayoutAnimation);
      } else {
        isAnimatingLayout = false;
        for (let i = 0; i < NODES.length; i++) {
          const n = NODES[i];
          n.x = n.targetX;
          n.y = n.targetY;
        }
        render();
      }
    }

    const layoutSelectEl = document.getElementById('layout-select');
    if (layoutSelectEl) {
      layoutSelectEl.addEventListener('change', (e) => {
        transitionToLayout(e.target.value);
      });
    }
"""

TARGET_JS_LOC = '    render();\n  </script>'
if 'Multi-Layout Perspective Transition Engine' not in html:
    html = html.replace(TARGET_JS_LOC, ANIMATION_JS + '\n    render();\n  </script>')
    print("Injected Multi-Layout Animation Engine into script.")
else:
    print("Multi-Layout Animation Engine already present.")

# Update recenter button to handle hierarchical layout smoothly
html = html.replace(
    "zoom = 0.25;\n      panX = width / 2;\n      panY = height / 2;\n      selectedNode = null;\n      render();",
    "zoom = (currentLayout === 'hierarchical' || currentLayout === 'domain') ? 0.18 : 0.25;\n      panX = width / 2;\n      panY = height / 2;\n      selectedNode = null;\n      render();"
)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"SUCCESS: Patched {HTML_PATH} successfully!")

