"""
patch_ego_network_highlight.py
==============================
Updates render() in output/visualizations/statutory_kg_full_web.html so that
when any law is highlighted/selected (via clicking or quick search):
1. The highlighted law is prominently illuminated (gold/white glow, large radius).
2. Its directly connected laws (1-hop ego network) are illuminated with vibrant colors & cyan halo.
3. The connecting edges (amendments, repeals, citations) are drawn with high-contrast lines.
4. All unrelated nodes and edges fade into subtle dark background dust (same visual style as trace connections search).
5. Prominent labels are drawn for the selected law and its active connections.
"""

import os
import sys

HTML_PATH = "output/visualizations/statutory_kg_full_web.html"

if not os.path.exists(HTML_PATH):
    print(f"Error: {HTML_PATH} not found.")
    sys.exit(1)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Locate render()
idx_start = html.find("    function render() {")
if idx_start == -1:
    print("Error: Could not find function render()")
    sys.exit(1)

# Locate the end of render() before getNodeAtScreenPos
idx_end = html.find("    // Accurate Screen-Space Hit-Testing", idx_start)
if idx_end == -1:
    idx_end = html.find("    function getNodeAtScreenPos", idx_start)

if idx_end == -1:
    print("Error: Could not find end of render()")
    sys.exit(1)

old_render = html[idx_start:idx_end]

NEW_RENDER = """    function render() {
      ctx.clearRect(0, 0, width, height);

      let visibleNodesCount = 0;
      let visibleEdgesCount = 0;

      // Compute connected neighbors if a law is highlighted/selected
      let selectedNeighborIds = null;
      if (selectedNode) {
        selectedNeighborIds = new Set();
        selectedNeighborIds.add(selectedNode.id);
        const neighbors = adj.get(selectedNode.id) || [];
        for (let i = 0; i < neighbors.length; i++) {
          selectedNeighborIds.add(neighbors[i].target);
        }
      }

      // 1. Draw Edges
      for (let i = 0; i < EDGES.length; i++) {
        const edge = EDGES[i];
        if (filterEdge !== 'all' && edge.t !== filterEdge) continue;

        const u = nodeMap.get(edge.u);
        const v = nodeMap.get(edge.v);
        if (!u || !v) continue;

        const isConnectedToSelected = selectedNeighborIds && (
          (u.id === selectedNode.id && selectedNeighborIds.has(v.id)) ||
          (v.id === selectedNode.id && selectedNeighborIds.has(u.id))
        );

        if (!isConnectedToSelected && (!isNodeVisible(u) || !isNodeVisible(v))) continue;

        visibleEdgesCount++;

        const isPathEdge = activePathEdges && (activePathEdges.has(`${u.id}|${v.id}`) || activePathEdges.has(`${v.id}|${u.id}`));
        const isSelectedEdge = isConnectedToSelected;
        const isHoveredEdge = !selectedNode && hoveredNode && (u.id === hoveredNode.id || v.id === hoveredNode.id);

        if (isPathEdge) {
          ctx.strokeStyle = '#FFD700';
          ctx.lineWidth = 3.5;
        } else if (activePathNodes) {
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
          ctx.lineWidth = 0.3;
        } else if (isSelectedEdge) {
          if (edge.t === 'amends') {
            ctx.strokeStyle = '#FFA500';
            ctx.lineWidth = 2.6;
          } else if (edge.t === 'repeals') {
            ctx.strokeStyle = '#EF4444';
            ctx.lineWidth = 2.8;
          } else {
            ctx.strokeStyle = '#00F2FE';
            ctx.lineWidth = 2.4;
          }
        } else if (selectedNode) {
          // Dim all unrelated edges into subtle background when a law is highlighted
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.015)';
          ctx.lineWidth = 0.3;
        } else if (isHoveredEdge) {
          ctx.strokeStyle = '#00F2FE';
          ctx.lineWidth = 2.0;
        } else {
          if (edge.t === 'amends') {
            ctx.strokeStyle = 'rgba(255, 165, 0, 0.45)';
            ctx.lineWidth = 1.0;
          } else if (edge.t === 'repeals') {
            ctx.strokeStyle = 'rgba(239, 68, 68, 0.6)';
            ctx.lineWidth = 1.2;
          } else {
            ctx.strokeStyle = 'rgba(100, 150, 255, 0.18)';
            ctx.lineWidth = 0.6;
          }
        }

        ctx.beginPath();
        ctx.moveTo(toScreenX(u.x), toScreenY(u.y));
        ctx.lineTo(toScreenX(v.x), toScreenY(v.y));
        ctx.stroke();
      }

      // 2. Draw Nodes
      for (let i = 0; i < NODES.length; i++) {
        const n = NODES[i];
        const isSelected = selectedNode && selectedNode.id === n.id;
        const isConnectedNeighbor = selectedNeighborIds && selectedNeighborIds.has(n.id);

        if (!isSelected && !isConnectedNeighbor && !isNodeVisible(n)) continue;

        visibleNodesCount++;

        const sx = toScreenX(n.x);
        const sy = toScreenY(n.y);

        if (sx < -100 || sx > width + 100 || sy < -100 || sy > height + 100) continue;

        const isHovered = hoveredNode && hoveredNode.id === n.id;
        const isPathNode = activePathNodes && activePathNodes.has(n.id);
        const isPathEndpoint = pathStartNode && (n.id === pathStartNode.id || (pathEndNode && n.id === pathEndNode.id));

        // Dynamic node radius
        let sr = Math.max(2.2, n.r * zoom);
        if (isPathEndpoint) {
          sr = Math.max(3.8, n.r * zoom * 1.5);
        } else if (isPathNode) {
          sr = Math.max(3.0, n.r * zoom * 1.25);
        } else if (isSelected) {
          sr = Math.max(4.2, n.r * zoom * 1.6);
        } else if (isConnectedNeighbor) {
          sr = Math.max(3.2, n.r * zoom * 1.3);
        } else if (selectedNode || activePathNodes) {
          sr = Math.max(1.5, n.r * zoom * 0.7);
        }

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
          ctx.fillStyle = 'rgba(255, 255, 255, 0.06)';
          ctx.shadowBlur = 0;
        } else if (isSelected) {
          // Glowing Gold/White core for selected law
          ctx.fillStyle = '#FFFFFF';
          ctx.shadowColor = '#FFD700';
          ctx.shadowBlur = 26;
        } else if (isConnectedNeighbor) {
          // Vibrant color + cyan halo for connected laws
          ctx.fillStyle = getNodeColor(n);
          ctx.shadowColor = '#00F2FE';
          ctx.shadowBlur = 16;
        } else if (selectedNode) {
          // Dim non-connected laws into subtle background dust (trace search style)
          ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
          ctx.shadowBlur = 0;
        } else if (isHovered) {
          ctx.fillStyle = '#FFFFFF';
          ctx.shadowColor = '#00F2FE';
          ctx.shadowBlur = 18;
        } else {
          ctx.fillStyle = getNodeColor(n);
          ctx.shadowBlur = 0;
        }
        ctx.fill();

        if (n.id === 'ra_7160_1991' && !selectedNode && !activePathNodes) {
          ctx.strokeStyle = '#FFD700';
          ctx.lineWidth = 2.5;
          ctx.stroke();
        }

        // 3. Draw Labels on Highlighted Law, Connected Neighbors, Hover, Path, or Hubs
        const shouldDrawLabel = isSelected ||
                                (selectedNode && isConnectedNeighbor && (n.deg >= 15 || zoom >= 0.7 || isHovered)) ||
                                isHovered ||
                                (activePathNodes && activePathNodes.has(n.id)) ||
                                (!selectedNode && !activePathNodes && showHubLabels && (n.id === 'ra_7160_1991' || n.deg >= 60));

        if (shouldDrawLabel && n.label) {
          const fontSize = Math.max(10, Math.min(15, (isSelected ? 13 : 11) * zoom));
          ctx.font = `${isSelected ? '700' : '600'} ${fontSize}px Inter, sans-serif`;
          if (isSelected) {
            ctx.fillStyle = '#FFD700';
          } else if (isConnectedNeighbor) {
            ctx.fillStyle = '#00F2FE';
          } else if (isPathEndpoint) {
            ctx.fillStyle = '#FFD700';
          } else if (isPathNode || isHovered) {
            ctx.fillStyle = '#00F2FE';
          } else {
            ctx.fillStyle = '#F1F5F9';
          }
          ctx.shadowColor = '#000000';
          ctx.shadowBlur = 5;
          ctx.fillText(n.label, sx + sr + 6, sy + fontSize / 3);
          ctx.shadowBlur = 0;
        }
      }

      document.getElementById('stat-visible-nodes').innerText = visibleNodesCount.toLocaleString();
      document.getElementById('stat-visible-edges').innerText = visibleEdgesCount.toLocaleString();
    }

"""

html = html[:idx_start] + NEW_RENDER + html[idx_end:]

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully updated render() with 1-hop ego-network isolation!")
print(f"File size: {os.path.getsize(HTML_PATH)/(1024*1024):.2f} MB")
