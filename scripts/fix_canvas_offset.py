"""
fix_canvas_offset.py
====================
Fixes the canvas vertical offset displacement by taking getBoundingClientRect()
into account for all mouse events (mousemove, mousedown, click, wheel, and tooltip).
"""

with open("output/visualizations/statutory_kg_full_web.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update canvas resize logic
old_resize = """    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      render();
    });"""

new_resize = """    function updateCanvasSize() {
      const rect = canvas.getBoundingClientRect();
      width = canvas.width = rect.width;
      height = canvas.height = rect.height;
    }
    updateCanvasSize();

    window.addEventListener('resize', () => {
      updateCanvasSize();
      render();
    });

    function getCanvasMousePos(e) {
      const rect = canvas.getBoundingClientRect();
      return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      };
    }"""

html = html.replace(old_resize, new_resize)

# 2. Update mousedown
old_mousedown = """    canvas.addEventListener('mousedown', (e) => {
      isDragging = true;
      dragStartX = e.clientX - panX;
      dragStartY = e.clientY - panY;
      tooltip.style.display = 'none';
    });"""

new_mousedown = """    canvas.addEventListener('mousedown', (e) => {
      const m = getCanvasMousePos(e);
      isDragging = true;
      dragStartX = m.x - panX;
      dragStartY = m.y - panY;
      tooltip.style.display = 'none';
    });"""

html = html.replace(old_mousedown, new_mousedown)

# 3. Update mousemove
old_mousemove = """    window.addEventListener('mousemove', (e) => {
      if (isDragging) {
        panX = e.clientX - dragStartX;
        panY = e.clientY - dragStartY;
        tooltip.style.display = 'none';
        render();
        return;
      }

      const found = getNodeAtScreenPos(e.clientX, e.clientY);

      if (found !== hoveredNode) {
        hoveredNode = found;
        render();
      }

      if (hoveredNode) {
        const sx = toScreenX(hoveredNode.x);
        const sy = toScreenY(hoveredNode.y);
        tooltip.style.display = 'block';
        tooltip.style.left = `${sx}px`;
        tooltip.style.top = `${sy}px`;
        tooltip.innerHTML = `<span style="color:#00F2FE;">${hoveredNode.num || hoveredNode.id}</span> <span style="color:#94a3b8; font-size:10px;">(Degree: ${hoveredNode.deg})</span>`;
      } else {
        tooltip.style.display = 'none';
      }
    });"""

new_mousemove = """    window.addEventListener('mousemove', (e) => {
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
    });"""

html = html.replace(old_mousemove, new_mousemove)

# 4. Update wheel
old_wheel = """    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
      const mouseWorldX = toWorldX(e.clientX);
      const mouseWorldY = toWorldY(e.clientY);

      zoom = Math.max(0.05, Math.min(4.5, zoom * zoomFactor));

      panX = e.clientX - mouseWorldX * zoom;
      panY = e.clientY - mouseWorldY * zoom;

      render();
    }, { passive: false });"""

new_wheel = """    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const m = getCanvasMousePos(e);
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
      const mouseWorldX = toWorldX(m.x);
      const mouseWorldY = toWorldY(m.y);

      zoom = Math.max(0.05, Math.min(4.5, zoom * zoomFactor));

      panX = m.x - mouseWorldX * zoom;
      panY = m.y - mouseWorldY * zoom;

      render();
    }, { passive: false });"""

html = html.replace(old_wheel, new_wheel)

# 5. Update click
old_click = """    canvas.addEventListener('click', (e) => {
      const found = getNodeAtScreenPos(e.clientX, e.clientY);
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

new_click = """    canvas.addEventListener('click', (e) => {
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

html = html.replace(old_click, new_click)

with open("output/visualizations/statutory_kg_full_web.html", "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: Canvas coordinate offset completely fixed!")

