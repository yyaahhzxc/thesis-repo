"""
update_pathfinder_ui.py
=======================
Inserts the 2-Law Lineage & Distance Pathfinding feature directly into
output/visualizations/statutory_kg_full_web.html without needing to recalculate
NetworkX coordinates.
"""

import os
import re

HTML_PATH = "output/visualizations/statutory_kg_full_web.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Left Panel: Add Pathfinding UI Section above Search
old_search = '<div class="search-box">\n        <input type="text" id="search-input" placeholder="Search RA 7160, Ordinance No., keyword...">\n      </div>'

new_pathfinder_ui = """<!-- 2-Law Path & Distance Finder -->
      <div class="filter-section" style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.2); border-radius: 8px; padding: 10px;">
        <div class="filter-label" style="color: #00F2FE;">
          <span>Trace Connection Between 2 Laws</span>
          <span id="path-distance-badge" style="font-family:'Fira Code'; font-size:10px; color:#FFD700; background:rgba(255,215,0,0.1); padding:2px 6px; border-radius:4px; display:none;">Distance: 2 hops</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; margin-top: 6px;">
          <input type="text" id="path-input-a" placeholder="Law A (e.g. 0270-23, 158-05)..." style="width:100%; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); border-radius:6px; padding:6px 10px; color:#f1f5f9; font-size:11px; outline:none;">
          <input type="text" id="path-input-b" placeholder="Law B (e.g. RA 7160, RA 4136)..." style="width:100%; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); border-radius:6px; padding:6px 10px; color:#f1f5f9; font-size:11px; outline:none;">
          <div class="btn-row" style="margin-top: 4px;">
            <button class="toggle-btn" id="btn-trace-path" style="background:#00F2FE; color:#07090e; font-weight:700; flex:1;">Find Path</button>
            <button class="toggle-btn" id="btn-clear-path" style="flex:1;">Clear Path</button>
          </div>
          <div id="path-status" style="font-size:11px; color:#94a3b8; line-height:1.4; margin-top:2px; display:none;"></div>
        </div>
      </div>

      <div class="search-box">
        <input type="text" id="search-input" placeholder="Search individual law, keyword...">
      </div>"""

html = html.replace(old_search, new_pathfinder_ui)

# 2. Update JavaScript: Add Adjacency Graph, Shortest-Path BFS, and Glowing Path Rendering
old_js_start = """    const nodeMap = new Map();
    NODES.forEach(n => nodeMap.set(n.id, n));"""

new_js_logic = """    const nodeMap = new Map();
    NODES.forEach(n => nodeMap.set(n.id, n));

    // Build Adjacency List for Breadth-First Search (BFS) Shortest Path
    const adj = new Map();
    NODES.forEach(n => adj.set(n.id, []));
    EDGES.forEach(e => {
      if (adj.has(e.u) && adj.has(e.v)) {
        adj.get(e.u).push({ target: e.v, type: e.t });
        adj.get(e.v).push({ target: e.u, type: e.t });
      }
    });

    let activePathNodes = null; // Set of node IDs along shortest path
    let activePathEdges = null; // Set of "u|v" strings along shortest path
    let pathStartNode = null;
    let pathEndNode = null;

    function findShortestPath(startId, endId) {
      if (startId === endId) return { distance: 0, path: [startId] };
      const queue = [[startId]];
      const visited = new Set([startId]);

      while (queue.length > 0) {
        const currentPath = queue.shift();
        const current = currentPath[currentPath.length - 1];

        const neighbors = adj.get(current) || [];
        for (let i = 0; i < neighbors.length; i++) {
          const neighbor = neighbors[i].target;
          if (neighbor === endId) {
            currentPath.push(neighbor);
            return { distance: currentPath.length - 1, path: currentPath };
          }
          if (!visited.has(neighbor)) {
            visited.add(neighbor);
            const newPath = [...currentPath, neighbor];
            queue.push(newPath);
          }
        }
      }
      return null; // Not connected in active graph component
    }"""

html = html.replace(old_js_start, new_js_logic)

# 3. Update Edge Drawing in render(): Highlight Path Edges with Neon Gold/Cyan Glow
old_edge_render = """        const isHighlighted = (selectedNode && (u.id === selectedNode.id || v.id === selectedNode.id)) ||
                              (hoveredNode && (u.id === hoveredNode.id || v.id === hoveredNode.id));

        if (isHighlighted) {
          ctx.strokeStyle = '#00F2FE';
          ctx.lineWidth = 2.0;
        } else if (selectedNode) {
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
          ctx.lineWidth = 0.3;
        } else {"""

new_edge_render = """        const isPathEdge = activePathEdges && (activePathEdges.has(`${u.id}|${v.id}`) || activePathEdges.has(`${v.id}|${u.id}`));
        const isHighlighted = (selectedNode && (u.id === selectedNode.id || v.id === selectedNode.id)) ||
                              (hoveredNode && (u.id === hoveredNode.id || v.id === hoveredNode.id));

        if (isPathEdge) {
          ctx.strokeStyle = '#FFD700';
          ctx.lineWidth = 3.5;
        } else if (activePathNodes) {
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
          ctx.lineWidth = 0.3;
        } else if (isHighlighted) {
          ctx.strokeStyle = '#00F2FE';
          ctx.lineWidth = 2.0;
        } else if (selectedNode) {
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
          ctx.lineWidth = 0.3;
        } else {"""

html = html.replace(old_edge_render, new_edge_render)

# 4. Update Node Drawing in render(): Highlight Path Nodes
old_node_draw = """        const isHovered = hoveredNode && hoveredNode.id === n.id;
        const isSelected = selectedNode && selectedNode.id === n.id;
        const sr = Math.max(2.2, n.r * zoom);

        ctx.beginPath();
        ctx.arc(sx, sy, sr, 0, Math.PI * 2);

        if (isHovered || isSelected) {
          ctx.fillStyle = '#FFFFFF';
          ctx.shadowColor = '#00F2FE';
          ctx.shadowBlur = 18;
        } else {
          ctx.fillStyle = n.c;
          ctx.shadowBlur = 0;
        }
        ctx.fill();"""

new_node_draw = """        const isHovered = hoveredNode && hoveredNode.id === n.id;
        const isSelected = selectedNode && selectedNode.id === n.id;
        const isPathNode = activePathNodes && activePathNodes.has(n.id);
        const isPathEndpoint = pathStartNode && (n.id === pathStartNode.id || (pathEndNode && n.id === pathEndNode.id));
        const sr = Math.max(2.2, n.r * zoom * (isPathEndpoint ? 1.5 : (isPathNode ? 1.25 : 1.0)));

        ctx.beginPath();
        ctx.arc(sx, sy, sr, 0, Math.PI * 2);

        if (isPathEndpoint) {
          ctx.fillStyle = '#FFD700';
          ctx.shadowColor = '#FFD700';
          ctx.shadowBlur = 24;
        } else if (isPathNode) {
          ctx.fillStyle = '#00F2FE';
          ctx.shadowColor = '#00F2FE';
          ctx.shadowBlur = 18;
        } else if (activePathNodes) {
          ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
          ctx.shadowBlur = 0;
        } else if (isHovered || isSelected) {
          ctx.fillStyle = '#FFFFFF';
          ctx.shadowColor = '#00F2FE';
          ctx.shadowBlur = 18;
        } else {
          ctx.fillStyle = n.c;
          ctx.shadowBlur = 0;
        }
        ctx.fill();"""

html = html.replace(old_node_draw, new_node_draw)

# 5. Update Label Drawing: Always show labels along active path
old_label_draw = """        const shouldDrawLabel = isHovered || isSelected || (showHubLabels && (n.id === 'ra_7160_1991' || n.deg >= 60));"""
new_label_draw = """        const shouldDrawLabel = isHovered || isSelected || (activePathNodes && activePathNodes.has(n.id)) || (showHubLabels && (n.id === 'ra_7160_1991' || n.deg >= 60));"""
html = html.replace(old_label_draw, new_label_draw)

# 6. Add Event Handlers for Pathfinding Buttons
old_initial_render = """    // Initial render
    render();"""

new_path_handlers = """    // Pathfinding Event Handlers
    function findNodeByQuery(q) {
      if (!q) return null;
      q = q.toLowerCase().trim();
      return NODES.find(n => 
        (n.num && n.num.toLowerCase().includes(q)) ||
        (n.id && n.id.toLowerCase().includes(q)) ||
        (n.title && n.title.toLowerCase().includes(q))
      );
    }

    document.getElementById('btn-trace-path').addEventListener('click', () => {
      const qA = document.getElementById('path-input-a').value;
      const qB = document.getElementById('path-input-b').value;
      const statusDiv = document.getElementById('path-status');
      const badge = document.getElementById('path-distance-badge');

      statusDiv.style.display = 'block';

      if (!qA || !qB) {
        statusDiv.innerHTML = '<span style="color:#EF4444;">Please specify both Law A and Law B.</span>';
        return;
      }

      const nodeA = findNodeByQuery(qA);
      const nodeB = findNodeByQuery(qB);

      if (!nodeA) {
        statusDiv.innerHTML = `<span style="color:#EF4444;">Law A ("${qA}") not found in graph.</span>`;
        return;
      }
      if (!nodeB) {
        statusDiv.innerHTML = `<span style="color:#EF4444;">Law B ("${qB}") not found in graph.</span>`;
        return;
      }

      const res = findShortestPath(nodeA.id, nodeB.id);
      if (!res) {
        statusDiv.innerHTML = `<span style="color:#F59E0B;">No direct or intermediate topological path connects <b>${nodeA.num}</b> and <b>${nodeB.num}</b>. They belong to separate statutory components.</span>`;
        badge.style.display = 'none';
        activePathNodes = null;
        activePathEdges = null;
        render();
        return;
      }

      // Path found!
      pathStartNode = nodeA;
      pathEndNode = nodeB;
      activePathNodes = new Set(res.path);
      activePathEdges = new Set();
      for (let i = 0; i < res.path.length - 1; i++) {
        activePathEdges.add(`${res.path[i]}|${res.path[i+1]}`);
      }

      badge.style.display = 'inline-block';
      badge.innerText = `Distance: ${res.distance} hop${res.distance === 1 ? '' : 's'}`;

      const pathSteps = res.path.map((nid, idx) => {
        const n = nodeMap.get(nid);
        const name = n.num || nid;
        return `<span style="color:${idx === 0 || idx === res.path.length-1 ? '#FFD700' : '#00F2FE'}; font-weight:600;">${name}</span>`;
      }).join(' &rarr; ');

      statusDiv.innerHTML = `<div style="margin-bottom:4px; color:#F1F5F9;">Connected via <b>${res.distance} hop${res.distance === 1 ? '' : 's'}</b>:</div><div>${pathSteps}</div>`;

      // Center view between the two nodes
      const midX = (nodeA.x + nodeB.x) / 2;
      const midY = (nodeA.y + nodeB.y) / 2;
      const distSpan = Math.sqrt((nodeA.x - nodeB.x)**2 + (nodeA.y - nodeB.y)**2);
      zoom = Math.max(0.18, Math.min(1.4, (width * 0.5) / (distSpan + 300)));
      panX = width / 2 - midX * zoom;
      panY = height / 2 - midY * zoom;

      render();
    });

    document.getElementById('btn-clear-path').addEventListener('click', () => {
      activePathNodes = null;
      activePathEdges = null;
      pathStartNode = null;
      pathEndNode = null;
      document.getElementById('path-status').style.display = 'none';
      document.getElementById('path-distance-badge').style.display = 'none';
      document.getElementById('path-input-a').value = '';
      document.getElementById('path-input-b').value = '';
      render();
    });

    // Initial render
    render();"""

html = html.replace(old_initial_render, new_path_handlers)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: 2-Law Path & Distance Finder integrated into statutory_kg_full_web.html!")

