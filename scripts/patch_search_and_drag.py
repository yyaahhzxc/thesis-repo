"""
patch_search_and_drag.py
========================
Updates output/visualizations/statutory_kg_full_web.html:
1. Replaces the plain single search bar with the updated Trace Connection style:
   - Type selector dropdown (All, RA, Ordinance, PD, BP, EO, CA, Act)
   - Live suggestions autocomplete dropdown showing law number, year, and title
   - Smooth camera zoom and focus on selection/enter
2. Prevents drag/pan on canvas from clicking away or clearing the currently highlighted law
   by tracking drag distance (5px threshold) and suppressing the synthetic click event on release.
"""

import re
import os
import sys

HTML_PATH = "output/visualizations/statutory_kg_full_web.html"

if not os.path.exists(HTML_PATH):
    print(f"Error: {HTML_PATH} not found.")
    sys.exit(1)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# -------------------------------------------------------------------------
# 1. Update the Search Bar HTML
# -------------------------------------------------------------------------
OLD_SEARCH_HTML = """      <div class="search-box">
        <input type="text" id="search-input" placeholder="Search individual law, keyword...">
      </div>"""

NEW_SEARCH_HTML = """      <!-- Single Law Quick Search (Trace Connection Style) -->
      <div class="filter-section" style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 10px;">
        <div class="filter-label" style="display: flex; justify-content: space-between; align-items: center;">
          <span>Quick Search Law</span>
          <span id="search-status-badge" style="font-size: 10px; color: #00F2FE; font-family: 'Fira Code', monospace; display: none;"></span>
        </div>
        <div class="law-selector-row" style="margin-top: 6px;">
          <select id="type-select-search" class="type-select">
            <option value="ALL" selected>All</option>
            <option value="RA">RA</option>
            <option value="ORD">Ordinance</option>
            <option value="PD">PD</option>
            <option value="BP">BP</option>
            <option value="EO">EO</option>
            <option value="CA">CA</option>
            <option value="ACT">Act</option>
          </select>
          <div class="num-input-wrapper">
            <input type="text" id="search-input" class="num-input" placeholder="Type number or keyword (e.g. 7160, 0309, tax)..." autocomplete="off">
            <div id="suggest-search" class="suggestions-list"></div>
          </div>
        </div>
      </div>"""

if OLD_SEARCH_HTML in html:
    html = html.replace(OLD_SEARCH_HTML, NEW_SEARCH_HTML)
    print("[1/3] Successfully replaced single search HTML with trace-style selector.")
elif "Quick Search Law" in html:
    print("[1/3] Quick Search Law HTML already present.")
else:
    print("Warning: Could not find exact OLD_SEARCH_HTML block.")

# -------------------------------------------------------------------------
# 2. Update Canvas Mouse Events to Prevent Drag Click-Away
# -------------------------------------------------------------------------
OLD_MOUSE_EVENTS = """    canvas.addEventListener('mousedown', (e) => {
      const m = getCanvasMousePos(e);
      isDragging = true;
      dragStartX = m.x - panX;
      dragStartY = m.y - panY;
      tooltip.style.display = 'none';
    });

    window.addEventListener('mousemove', (e) => {
      const m = getCanvasMousePos(e);
      if (isDragging) {
        panX = m.x - dragStartX;
        panY = m.y - dragStartY;
        tooltip.style.display = 'none';
        render();
        return;
      }

      // Check if mouse is within canvas bounds
      if (m.x < 0 || m.x > width || m.y < 0 || m.y > height) {
        tooltip.style.display = 'none';
        if (hoveredNode) {
          hoveredNode = null;
          render();
        }
        return;
      }

      const found = getNodeAtScreenPos(m.x, m.y);

      if (found !== hoveredNode) {
        hoveredNode = found;
        render();
      }

      if (hoveredNode) {
        const sx = toScreenX(hoveredNode.x);
        const sy = toScreenY(hoveredNode.y);
        const rect = canvas.getBoundingClientRect();
        tooltip.style.display = 'block';
        tooltip.style.left = `${sx + rect.left}px`;
        tooltip.style.top = `${sy + rect.top}px`;
        tooltip.innerHTML = `<span style="color:#00F2FE;">${hoveredNode.num || hoveredNode.id}</span> <span style="color:#94a3b8; font-size:10px;">(Degree: ${hoveredNode.deg})</span>`;
      } else {
        tooltip.style.display = 'none';
      }
    });

    window.addEventListener('mouseup', () => {
      isDragging = false;
    });

    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const m = getCanvasMousePos(e);
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
      const mouseWorldX = toWorldX(m.x);
      const mouseWorldY = toWorldY(m.y);

      zoom = Math.max(0.05, Math.min(4.5, zoom * zoomFactor));

      panX = m.x - mouseWorldX * zoom;
      panY = m.y - mouseWorldY * zoom;

      render();
    }, { passive: false });

    canvas.addEventListener('click', (e) => {
      const m = getCanvasMousePos(e);
      const found = getNodeAtScreenPos(m.x, m.y);
      if (found) {
        selectedNode = found;
        showInspector(selectedNode);
        render();
      } else {
        selectedNode = null;
        hideInspector();
        render();
      }}
    );"""

NEW_MOUSE_EVENTS = """    // Drag vs Click Tracking State (Prevents drag release from clicking away)
    let mouseDownScreenX = 0;
    let mouseDownScreenY = 0;
    let hasDragged = false;
    const DRAG_THRESHOLD = 5; // pixels

    canvas.addEventListener('mousedown', (e) => {
      const m = getCanvasMousePos(e);
      isDragging = true;
      hasDragged = false;
      mouseDownScreenX = m.x;
      mouseDownScreenY = m.y;
      dragStartX = m.x - panX;
      dragStartY = m.y - panY;
      tooltip.style.display = 'none';
    });

    window.addEventListener('mousemove', (e) => {
      const m = getCanvasMousePos(e);
      if (isDragging) {
        const dx = m.x - mouseDownScreenX;
        const dy = m.y - mouseDownScreenY;
        if (Math.hypot(dx, dy) > DRAG_THRESHOLD) {
          hasDragged = true;
        }
        panX = m.x - dragStartX;
        panY = m.y - dragStartY;
        tooltip.style.display = 'none';
        render();
        return;
      }

      // Check if mouse is within canvas bounds
      if (m.x < 0 || m.x > width || m.y < 0 || m.y > height) {
        tooltip.style.display = 'none';
        if (hoveredNode) {
          hoveredNode = null;
          render();
        }
        return;
      }

      const found = getNodeAtScreenPos(m.x, m.y);

      if (found !== hoveredNode) {
        hoveredNode = found;
        render();
      }

      if (hoveredNode) {
        const sx = toScreenX(hoveredNode.x);
        const sy = toScreenY(hoveredNode.y);
        const rect = canvas.getBoundingClientRect();
        tooltip.style.display = 'block';
        tooltip.style.left = `${sx + rect.left}px`;
        tooltip.style.top = `${sy + rect.top}px`;
        tooltip.innerHTML = `<span style="color:#00F2FE;">${hoveredNode.num || hoveredNode.id}</span> <span style="color:#94a3b8; font-size:10px;">(Degree: ${hoveredNode.deg})</span>`;
      } else {
        tooltip.style.display = 'none';
      }
    });

    window.addEventListener('mouseup', () => {
      isDragging = false;
    });

    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const m = getCanvasMousePos(e);
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
      const mouseWorldX = toWorldX(m.x);
      const mouseWorldY = toWorldY(m.y);

      zoom = Math.max(0.05, Math.min(4.5, zoom * zoomFactor));

      panX = m.x - mouseWorldX * zoom;
      panY = m.y - mouseWorldY * zoom;

      render();
    }, { passive: false });

    canvas.addEventListener('click', (e) => {
      // If user dragged/panned across canvas, suppress click to preserve highlighted law
      if (hasDragged) {
        hasDragged = false;
        return;
      }
      const m = getCanvasMousePos(e);
      const found = getNodeAtScreenPos(m.x, m.y);
      if (found) {
        selectedNode = found;
        showInspector(selectedNode);
        render();
      } else {
        selectedNode = null;
        hideInspector();
        render();
      }
    });"""

if OLD_MOUSE_EVENTS in html:
    html = html.replace(OLD_MOUSE_EVENTS, NEW_MOUSE_EVENTS)
    print("[2/3] Successfully updated canvas mouse events with drag-click suppression.")
elif "DRAG_THRESHOLD" in html:
    print("[2/3] Drag-click suppression already present.")
else:
    print("Warning: Could not find exact OLD_MOUSE_EVENTS block.")

# -------------------------------------------------------------------------
# 3. Update searchLaws, setupSuggestions & Quick Search Wiring
# -------------------------------------------------------------------------
OLD_SEARCH_JS = """    // Helper: Find law nodes by type and number query
    function searchLaws(type, query) {
      query = (query || '').toLowerCase().trim();
      return NODES.filter(n => {
        if (type !== 'ALL' && n.type !== type) return false;
        if (!query) return true;
        return (n.num && n.num.toLowerCase().includes(query)) ||
               (n.id && n.id.toLowerCase().includes(query));
      });
    }

    function setupSuggestions(inputId, typeSelectId, listId) {
      const input = document.getElementById(inputId);
      const typeSelect = document.getElementById(typeSelectId);
      const list = document.getElementById(listId);

      function update() {
        const q = input.value.trim();
        const type = typeSelect.value;
        const matches = searchLaws(type, q).slice(0, 8);

        if (matches.length === 0 || !q) {
          list.style.display = 'none';
          return;
        }

        list.innerHTML = matches.map(m => `
          <div class="suggestion-item" data-id="${m.id}">
            <span style="color:#00F2FE; font-weight:600;">${m.num || m.id}</span>
            <span style="color:#64748b; font-size:10px; margin-left:4px;">(${m.year})</span>
          </div>
        `).join('');
        list.style.display = 'block';

        list.querySelectorAll('.suggestion-item').forEach(item => {
          item.addEventListener('click', () => {
            const nid = item.getAttribute('data-id');
            const found = nodeMap.get(nid);
            if (found) {
              input.value = found.num || found.id;
              input.dataset.selectedId = found.id;
            }
            list.style.display = 'none';
          });
        });
      }

      input.addEventListener('input', update);
      input.addEventListener('focus', update);
      typeSelect.addEventListener('change', update);

      document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !list.contains(e.target)) {
          list.style.display = 'none';
        }
      });
    }

    setupSuggestions('path-input-a', 'type-select-a', 'suggest-a');
    setupSuggestions('path-input-b', 'type-select-b', 'suggest-b');"""

NEW_SEARCH_JS = """    // Helper: Find law nodes by type, number, or keyword query
    function searchLaws(type, query) {
      query = (query || '').toLowerCase().trim();
      if (!query) return [];
      const filtered = NODES.filter(n => {
        if (type !== 'ALL' && n.type !== type) return false;
        return (n.num && n.num.toLowerCase().includes(query)) ||
               (n.id && n.id.toLowerCase().includes(query)) ||
               (n.title && n.title.toLowerCase().includes(query));
      });

      // Rank exact num matches first, then prefix, then degree centrality
      filtered.sort((a, b) => {
        const aNum = (a.num || '').toLowerCase();
        const bNum = (b.num || '').toLowerCase();
        const aId = (a.id || '').toLowerCase();
        const bId = (b.id || '').toLowerCase();

        const aNumExact = aNum === query ? 3 : (aNum.startsWith(query) ? 2 : (aNum.includes(query) ? 1 : 0));
        const bNumExact = bNum === query ? 3 : (bNum.startsWith(query) ? 2 : (bNum.includes(query) ? 1 : 0));
        if (aNumExact !== bNumExact) return bNumExact - aNumExact;

        const aIdMatch = aId.includes(query) ? 1 : 0;
        const bIdMatch = bId.includes(query) ? 1 : 0;
        if (aIdMatch !== bIdMatch) return bIdMatch - aIdMatch;

        return (b.deg || 0) - (a.deg || 0);
      });

      return filtered;
    }

    function setupSuggestions(inputId, typeSelectId, listId, onSelectCallback) {
      const input = document.getElementById(inputId);
      const typeSelect = document.getElementById(typeSelectId);
      const list = document.getElementById(listId);
      if (!input || !typeSelect || !list) return;

      function update() {
        const q = input.value.trim();
        const type = typeSelect.value;
        const matches = searchLaws(type, q).slice(0, 10);

        if (matches.length === 0 || !q) {
          list.style.display = 'none';
          return;
        }

        list.innerHTML = matches.map(m => `
          <div class="suggestion-item" data-id="${m.id}" style="padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05); cursor:pointer;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="color:#00F2FE; font-weight:600;">${m.num || m.id}</span>
              <span style="color:#64748b; font-size:10px;">${m.year ? '(' + m.year + ')' : ''}</span>
            </div>
            ${m.title ? `<div style="color:#94a3b8; font-size:10px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:230px; margin-top:2px;">${m.title}</div>` : ''}
          </div>
        `).join('');
        list.style.display = 'block';

        list.querySelectorAll('.suggestion-item').forEach(item => {
          item.addEventListener('click', () => {
            const nid = item.getAttribute('data-id');
            const found = nodeMap.get(nid);
            if (found) {
              input.value = found.num || found.id;
              input.dataset.selectedId = found.id;
              if (onSelectCallback) onSelectCallback(found);
            }
            list.style.display = 'none';
          });
        });
      }

      input.addEventListener('input', update);
      input.addEventListener('focus', update);
      typeSelect.addEventListener('change', update);

      // Support Enter key to select top match
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const q = input.value.trim();
          const type = typeSelect.value;
          const matches = searchLaws(type, q);
          if (matches.length > 0) {
            const found = matches[0];
            input.value = found.num || found.id;
            input.dataset.selectedId = found.id;
            list.style.display = 'none';
            if (onSelectCallback) onSelectCallback(found);
          }
        } else if (e.key === 'Escape') {
          list.style.display = 'none';
        }
      });

      document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !list.contains(e.target)) {
          list.style.display = 'none';
        }
      });
    }

    setupSuggestions('path-input-a', 'type-select-a', 'suggest-a');
    setupSuggestions('path-input-b', 'type-select-b', 'suggest-b');

    // Quick Search Wiring with Camera Focus & Inspector Card Activation
    function focusAndSelectNode(node) {
      if (!node) return;
      selectedNode = node;
      zoom = 1.25;
      panX = width / 2 - node.x * zoom;
      panY = height / 2 - node.y * zoom;
      showInspector(node);
      render();

      const badge = document.getElementById('search-status-badge');
      if (badge) {
        badge.innerText = 'MATCHED';
        badge.style.display = 'inline-block';
      }
    }

    setupSuggestions('search-input', 'type-select-search', 'suggest-search', (found) => {
      focusAndSelectNode(found);
    });

    document.getElementById('search-input').addEventListener('input', (e) => {
      const q = e.target.value.trim();
      if (!q) {
        const badge = document.getElementById('search-status-badge');
        if (badge) badge.style.display = 'none';
        delete e.target.dataset.selectedId;
      }
    });"""

if OLD_SEARCH_JS in html:
    html = html.replace(OLD_SEARCH_JS, NEW_SEARCH_JS)
    print("[3/3a] Successfully updated searchLaws and setupSuggestions.")
elif "focusAndSelectNode" in html:
    print("[3/3a] focusAndSelectNode already present.")
else:
    print("Warning: Could not find exact OLD_SEARCH_JS block.")

# Remove the old jarring search-input listener
OLD_SEARCH_INPUT_LISTENER = """    // General search bar
    document.getElementById('search-input').addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) {
        selectedNode = null;
        render();
        return;
      }
      const found = NODES.find(n => 
        (n.num && n.num.toLowerCase().includes(q)) ||
        (n.id && n.id.toLowerCase().includes(q)) ||
        (n.title && n.title.toLowerCase().includes(q))
      );
      if (found) {
        selectedNode = found;
        zoom = 1.1;
        panX = width / 2 - found.x * zoom;
        panY = height / 2 - found.y * zoom;
        showInspector(found);
        render();
      }
    });"""

if OLD_SEARCH_INPUT_LISTENER in html:
    html = html.replace(OLD_SEARCH_INPUT_LISTENER, "// (Old search-input listener replaced by autocomplete trace style)")
    print("[3/3b] Successfully removed obsolete jump-on-keypress search-input listener.")
else:
    print("Note: Obsolete search-input listener not found or already replaced.")

# Write updated HTML
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done! Updated {HTML_PATH} successfully. File size: {os.path.getsize(HTML_PATH)/(1024*1024):.2f} MB")
