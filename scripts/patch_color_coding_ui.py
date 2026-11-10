"""
patch_color_coding_ui.py
========================
Injects the dynamic Color Coding Palette selector, color lookup tables,
dynamic legend updates, and getNodeColor(n) rendering into statutory_kg_full_web.html.
"""

import os
import sys

HTML_PATH = 'output/visualizations/statutory_kg_full_web.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. UI Dropdown for Color Coding
COLOR_UI_HTML = """      <!-- Color Scheme / Partition Selector -->
      <div class="filter-section" style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 8px; padding: 10px; margin-bottom: 6px;">
        <div class="filter-label" style="color: #00F2FE; font-weight: 700; display: flex; justify-content: space-between; align-items: center;">
          <span>Color Coding Palette</span>
          <span id="active-color-badge" style="font-size: 10px; background: rgba(0,242,254,0.18); padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">Domain Topics</span>
        </div>
        <select id="color-mode-select" class="filter-dropdown" style="margin-top: 6px; border-color: rgba(0, 242, 254, 0.4); font-weight: 600; color: #00F2FE;">
          <option value="domain" selected>1. Macro Legal Domain (10 Topic Models)</option>
          <option value="corpus_typology">2. Corpus-Specific Typology (National vs. Local Topics)</option>
          <option value="instrument">3. Statutory Instrument Type (RA, ORD, PD, BP, EO, CA, ACT)</option>
          <option value="jurisdiction">4. Jurisdiction Contrast (National vs. Davao Local)</option>
          <option value="era">5. Legislative Era (Temporal Evolution)</option>
        </select>
        <div id="color-desc" style="font-size: 11px; color: #94a3b8; line-height: 1.4; margin-top: 6px;">
          Nodes colored by their 10 macro legal domains from dual-corpus topic modeling.
        </div>
      </div>
"""

TARGET_LOC = '      <!-- Visual Layout Perspective Selector -->'
if 'Color Scheme / Partition Selector' not in html:
    idx = html.find('</div>\n      </div>\n\n      <!-- 2-Law Path & Distance Finder -->')
    if idx != -1:
        # Insert after Visual Layout Perspective Selector
        html = html[:idx+13] + '\n' + COLOR_UI_HTML + html[idx+13:]
        print("Injected Color Scheme Selector UI panel after Layout Perspective.")
    else:
        # Fallback insert before 2-Law Path
        html = html.replace('      <!-- 2-Law Path & Distance Finder -->', COLOR_UI_HTML + '\n      <!-- 2-Law Path & Distance Finder -->')
        print("Injected Color Scheme Selector UI panel before 2-Law Path.")
else:
    print("Color Scheme Selector UI panel already present.")

# 2. JavaScript Color Engine and Dynamic Legend
COLOR_JS = """
    // ==========================================
    // Multi-Color Palette Classification Engine
    // ==========================================
    let currentColorMode = 'domain';

    const COLOR_DESCRIPTIONS = {
      'domain': '10 Macro Legal Domains: All enactments mapped to canonical subject-matter domains from dual-corpus topic modeling.',
      'corpus_typology': 'Corpus-Specific Typology: Differentiates authentic local functional classes (Traffic, Substantive, Donations, Calamity, Zoning) and national statutory topic categories.',
      'instrument': 'Statutory Instrument Classification: Republic Acts (RA), City Ordinances (ORD), Presidential Decrees (PD), Batas Pambansa (BP), Executive Orders (EO), Commonwealth Acts (CA), Public Acts (ACT).',
      'jurisdiction': 'Jurisdictional Contrast: Vivid contrast between Davao City Local Ordinances (Neon Cyan) and National Statutes (Warm Amber & Gold).',
      'era': 'Temporal Evolution: Legislative eras spanning Pre-War (<1946), Third Republic / Martial Law (1946–1986), Fifth Republic / LGC (1987–2015), and Modern Digital Era (2016–Present).'
    };

    const COLOR_PALETTES = {
      domain: {
        'General Administration, Organization & Civil Service': '#38BDF8',
        'Public Finance, Taxation, Fiscal Policy & Budget': '#F59E0B',
        'Police Power, Public Order, Safety & Penal Law': '#EF4444',
        'Social Services, Education, Labor & Human Development': '#10B981',
        'Public Works, Transportation, Utilities & Infrastructure': '#8B5CF6',
        'Commerce, Trade, Industry, Agriculture & Economic Enterprise': '#06B6D4',
        'Environmental Protection, Zoning, Land Use & Natural Resources': '#84CC16',
        'Executive Issuances & Policy Reorganization': '#EC4899',
        'Inter-Agency Agreements & Institutional MOAs/MOUs': '#F97316',
        'Substantive Regulatory, Health & Penal Ordinances': '#14B8A6'
      },
      local_typology: {
        'Substantive Regulatory, Health & Penal Ordinances': '#00F2FE',
        'Temporary Road Closures & Traffic Management': '#38BDF8',
        'Deeds of Donation & Property Usufruct': '#C084FC',
        'Disaster Risk Reduction, Calamity & QRF Funds': '#F43F5E',
        'Zoning Reclassifications & Subdivision Development': '#4ADE80',
        'Inter-Agency Agreements & Institutional MOAs/MOUs': '#FB923C'
      },
      national_typology: {
        'Executive Issuances & Policy Reorganization': '#EC4899',
        'Education & Academic Institutions': '#10B981',
        'Local Government & Territorial Boundaries': '#38BDF8',
        'Public Utilities & Telecommunications Franchises': '#8B5CF6',
        'Public Health, Hospitals & Medical Services': '#06B6D4',
        'Statutory Codes & General Legal Amendments': '#FFD700',
        'Public Finance & General Appropriations': '#F59E0B',
        'Taxation, Tariffs & Revenue Administration': '#EAB308'
      },
      instrument: {
        'ORD': '#00F2FE',
        'RA': '#10B981',
        'PD': '#8B5CF6',
        'BP': '#F59E0B',
        'EO': '#EC4899',
        'CA': '#EAB308',
        'ACT': '#EF4444',
        'OTHER': '#64748B'
      },
      era: {
        'Pre-War & Commonwealth (<1946)': '#D97706',
        'Third Republic & Martial Law (1946–1986)': '#EF4444',
        'Fifth Republic & Decentralization (1987–2015)': '#0EA5E9',
        'Modern Digital Era (2016–Present)': '#10B981'
      }
    };

    function getNodeColor(n) {
      if (n.id === 'ra_7160_1991') return '#FFD700';

      if (currentColorMode === 'domain') {
        if (n.deg >= 50 && n.jur === 'national') return '#FFB300';
        if (n.jur === 'local') return n.deg >= 8 ? '#00F2FE' : '#38BDF8';
        return COLOR_PALETTES.domain[n.dom] || '#38BDF8';
      }

      if (currentColorMode === 'corpus_typology') {
        if (n.jur === 'local') {
          return COLOR_PALETTES.local_typology[n.raw_dom] || '#00F2FE';
        } else {
          return COLOR_PALETTES.national_typology[n.raw_dom] || (COLOR_PALETTES.domain[n.dom] || '#64748B');
        }
      }

      if (currentColorMode === 'instrument') {
        return COLOR_PALETTES.instrument[n.type] || '#64748B';
      }

      if (currentColorMode === 'jurisdiction') {
        if (n.jur === 'local') {
          return n.deg >= 6 ? '#00F2FE' : '#38BDF8';
        } else {
          if (n.deg >= 30) return '#FFD700';
          if (n.deg >= 5) return '#F59E0B';
          return '#6366F1';
        }
      }

      if (currentColorMode === 'era') {
        return COLOR_PALETTES.era[n.era] || '#64748B';
      }

      return n.c;
    }

    function updateLegend() {
      const legendEl = document.querySelector('.legend');
      if (!legendEl) return;

      let html = '';
      if (currentColorMode === 'domain') {
        const items = [
          { c: '#38BDF8', l: 'General Admin & LGU' },
          { c: '#F59E0B', l: 'Finance & Taxation' },
          { c: '#EF4444', l: 'Police Power & Penal' },
          { c: '#10B981', l: 'Social & Education' },
          { c: '#8B5CF6', l: 'Public Works & Infra' },
          { c: '#06B6D4', l: 'Commerce & Enterprise' },
          { c: '#84CC16', l: 'Environment & Zoning' },
          { c: '#EC4899', l: 'Executive Policy' },
          { c: '#00F2FE', l: 'Davao City Ordinances' }
        ];
        html = items.map(it => `<div class="legend-item"><span class="legend-dot" style="background:${it.c};"></span><span>${it.l}</span></div>`).join('');
      } else if (currentColorMode === 'corpus_typology') {
        const items = [
          { c: '#00F2FE', l: 'Local: Substantive/Penal' },
          { c: '#38BDF8', l: 'Local: Traffic/Roads' },
          { c: '#C084FC', l: 'Local: Donations/Usufruct' },
          { c: '#F43F5E', l: 'Local: Calamity/QRF' },
          { c: '#4ADE80', l: 'Local: Zoning' },
          { c: '#FFD700', l: 'National: Codes & Amendments' },
          { c: '#F59E0B', l: 'National: Finance/Tax' },
          { c: '#EC4899', l: 'National: Exec Directives' },
          { c: '#8B5CF6', l: 'National: Utilities/Infra' }
        ];
        html = items.map(it => `<div class="legend-item"><span class="legend-dot" style="background:${it.c};"></span><span>${it.l}</span></div>`).join('');
      } else if (currentColorMode === 'instrument') {
        const items = [
          { c: '#00F2FE', l: 'Ordinance (ORD)' },
          { c: '#10B981', l: 'Republic Act (RA)' },
          { c: '#8B5CF6', l: 'Presidential Decree (PD)' },
          { c: '#F59E0B', l: 'Batas Pambansa (BP)' },
          { c: '#EC4899', l: 'Executive Order (EO)' },
          { c: '#EAB308', l: 'Commonwealth Act (CA)' },
          { c: '#EF4444', l: 'Public Act (ACT)' }
        ];
        html = items.map(it => `<div class="legend-item"><span class="legend-dot" style="background:${it.c};"></span><span>${it.l}</span></div>`).join('');
      } else if (currentColorMode === 'jurisdiction') {
        const items = [
          { c: '#00F2FE', l: 'Davao City Local Ordinances (SP)' },
          { c: '#FFD700', l: 'National Bedrock Super-Hubs (RA 7160, Codes)' },
          { c: '#F59E0B', l: 'Primary National Statutes' },
          { c: '#6366F1', l: 'Other National Statutes' }
        ];
        html = items.map(it => `<div class="legend-item"><span class="legend-dot" style="background:${it.c};"></span><span>${it.l}</span></div>`).join('');
      } else if (currentColorMode === 'era') {
        const items = [
          { c: '#D97706', l: 'Pre-War & Commonwealth (<1946)' },
          { c: '#EF4444', l: 'Third Republic & Martial Law (1946–1986)' },
          { c: '#0EA5E9', l: 'Fifth Republic & Decentralization (1987–2015)' },
          { c: '#10B981', l: 'Modern Digital Era (2016–Present)' }
        ];
        html = items.map(it => `<div class="legend-item"><span class="legend-dot" style="background:${it.c};"></span><span>${it.l}</span></div>`).join('');
      }
      legendEl.innerHTML = html;
    }
"""

if 'Multi-Color Palette Classification Engine' not in html:
    # Inject before render()
    idx_render = html.find('function render() {')
    html = html[:idx_render] + COLOR_JS + '\n    ' + html[idx_render:]
    print("Injected Color Classification Engine.")
else:
    print("Color Classification Engine already present.")

# 3. Replace static ctx.fillStyle = n.c with dynamic getNodeColor(n)
html = html.replace('ctx.fillStyle = n.c;', 'ctx.fillStyle = getNodeColor(n);')
print("Updated canvas node fill to use getNodeColor(n).")

# 4. Attach event listener for color selector
EVENT_JS = """
    const colorSelectEl = document.getElementById('color-mode-select');
    if (colorSelectEl) {
      colorSelectEl.addEventListener('change', (e) => {
        currentColorMode = e.target.value;
        const badge = document.getElementById('active-color-badge');
        if (badge) {
          const parts = e.target.options[e.target.selectedIndex].text.split('.');
          badge.innerText = (parts.length > 1 ? parts[1] : parts[0]).trim();
        }
        const desc = document.getElementById('color-desc');
        if (desc) desc.innerText = COLOR_DESCRIPTIONS[currentColorMode] || '';
        updateLegend();
        render();
      });
    }
"""

if 'colorSelectEl.addEventListener' not in html:
    idx_bottom = html.rfind('render();\n  </script>')
    html = html[:idx_bottom] + EVENT_JS + '\n    ' + html[idx_bottom:]
    print("Attached color selector event listener.")
else:
    print("Color selector event listener already present.")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: statutory_kg_full_web.html updated with dynamic color coding!")

