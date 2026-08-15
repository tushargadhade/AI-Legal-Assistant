document.addEventListener('DOMContentLoaded', () => {
  checkSystemStatus();
  loadAllProcedures();
  loadBnsMappings();
  updateScorecardQuestions();
});

// Check API Health & Status
async function checkSystemStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    const statusText = document.getElementById('status-text');
    if (data.status === 'online') {
      const modeStr = data.gemini_api_configured ? 'Gemini AI Active' : `${data.indexed_chunks} Legal Chunks`;
      statusText.innerText = modeStr;
    }
  } catch (err) {
    console.warn('Backend API connection check failed:', err);
    document.getElementById('status-text').innerText = 'Offline Mode';
  }
}

// Navigation Tab Switcher
function switchTab(tabName) {
  const tabs = ['qa', 'bns', 'scorecard', 'proc', 'simplify'];
  tabs.forEach(t => {
    const content = document.getElementById(`tab-${t}`);
    const btn = document.getElementById(`tab-${t}-btn`);
    if (content && btn) {
      if (t === tabName) {
        content.classList.remove('hidden');
        btn.classList.add('active');
      } else {
        content.classList.add('hidden');
        btn.classList.remove('active');
      }
    }
  });
}

// Speech Recognition (Voice Dictation)
function startVoiceInput() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert('Voice input is not supported in this browser. Please type your query.');
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'en-IN';
  recognition.interimResults = false;

  const btn = document.querySelector('button[onclick="startVoiceInput()"]');
  btn.innerText = '🎙️ Listening...';

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('query-input').value = transcript;
    btn.innerText = '🎙️ Speak';
    runQuery(transcript);
  };

  recognition.onerror = () => {
    btn.innerText = '🎙️ Speak';
  };

  recognition.onend = () => {
    btn.innerText = '🎙️ Speak';
  };

  recognition.start();
}

// Speech Synthesis (Audio Readout)
function readSummaryAudio() {
  const summaryOutput = document.getElementById('summary-output');
  if (!summaryOutput || !summaryOutput.innerText.trim()) {
    alert('No summary text to read.');
    return;
  }

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel(); // Stop ongoing
    const cleanText = summaryOutput.innerText.replace(/[*#>`]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  } else {
    alert('Text-to-speech audio is not supported in this browser.');
  }
}

// Quick Prompt Setters
function setQuery(q) {
  document.getElementById('query-input').value = q;
  runQuery(q);
}

// Search Form Submission Handler
function handleSearch(e) {
  e.preventDefault();
  const q = document.getElementById('query-input').value.trim();
  if (q) {
    runQuery(q);
  }
}

// Run Main Legal Query
async function runQuery(query) {
  const loading = document.getElementById('loading-indicator');
  const summaryOutput = document.getElementById('summary-output');
  const citationsOutput = document.getElementById('citations-output');
  const proceduresOutput = document.getElementById('procedures-output');
  const modeBadge = document.getElementById('ai-mode-badge');
  const countBadge = document.getElementById('citations-count-badge');

  // UI State: Loading
  loading.classList.remove('hidden');
  summaryOutput.innerHTML = '';
  citationsOutput.innerHTML = '';
  proceduresOutput.innerHTML = '';

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query })
    });

    const data = await response.json();
    loading.classList.add('hidden');

    if (data.error) {
      summaryOutput.innerHTML = `<p style="color:#ef4444;">Error: ${data.error}</p>`;
      return;
    }

    // 1. Render Mode Badge
    modeBadge.innerText = data.mode || 'AI Engine';

    // 2. Render Plain Language Summary
    summaryOutput.innerHTML = formatMarkdown(data.summary);

    // 3. Render Citations / Legal Clauses
    const citations = data.citations || [];
    countBadge.innerText = `${citations.length} Legal Clauses`;
    if (citations.length === 0) {
      citationsOutput.innerHTML = `<p style="color:var(--text-muted); font-size:0.9rem;">No direct matching legal sections found in indexed acts.</p>`;
    } else {
      citationsOutput.innerHTML = citations.map((c, i) => `
        <div class="citation-card" onclick="viewCitationDetail(${i})">
          <div class="citation-meta">
            <span class="act-badge">${escapeHtml(c.act_short_name || 'ACT')}</span>
            <span class="score-badge">Page ${c.page} | Sec ${escapeHtml(c.section)}</span>
          </div>
          <div class="citation-title">${escapeHtml(c.act_name)} - ${escapeHtml(c.section_title)}</div>
          <div class="citation-snippet">"${escapeHtml(c.text)}"</div>
        </div>
      `).join('');

      // Store globally for detail inspection
      window.currentCitations = citations;
    }

    // 4. Render Recommended Procedures
    const procs = data.recommended_procedures || [];
    if (procs.length === 0) {
      proceduresOutput.innerHTML = `<p style="color:var(--text-muted); font-size:0.85rem;">No specific step-by-step procedural guide matched for this query.</p>`;
    } else {
      proceduresOutput.innerHTML = procs.map(p => `
        <div class="procedure-card">
          <div class="procedure-title">
            <span>${escapeHtml(p.title)}</span>
            <span class="procedure-badge">${escapeHtml(p.short_act)}</span>
          </div>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">${escapeHtml(p.summary)}</p>
          <div style="font-size:0.8rem; color:var(--text-gold); margin-bottom:0.5rem;">
            ⏳ <strong>Timeline:</strong> ${escapeHtml(p.timeline)} | 💵 <strong>Fee:</strong> ${escapeHtml(p.fee)}
          </div>
          <div class="procedure-steps-list">
            ${p.steps.map(s => `
              <div class="step-item">
                <div class="step-item-title">Step ${s.step}: ${escapeHtml(s.title)}</div>
                <div class="step-item-desc">${escapeHtml(s.description)}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `).join('');
    }

  } catch (err) {
    loading.classList.add('hidden');
    summaryOutput.innerHTML = `<p style="color:#ef4444;">Failed to connect to backend server. Make sure Python app is running.</p>`;
    console.error(err);
  }
}

// Citation Detail Modal / Alert
function viewCitationDetail(idx) {
  const c = window.currentCitations[idx];
  if (!c) return;

  const detailHtml = `
    <div style="padding:1rem; background:var(--bg-dark); border-radius:12px; border:1px solid var(--primary-emerald); margin-top:1rem;">
      <h4 style="color:var(--text-emerald); margin-bottom:0.4rem;">${escapeHtml(c.act_name)}</h4>
      <p style="font-size:0.85rem; color:var(--text-gold); margin-bottom:0.5rem;">Section ${escapeHtml(c.section)} - ${escapeHtml(c.section_title)} (Page ${c.page})</p>
      <div style="font-size:0.9rem; color:#e5e7eb; white-space:pre-wrap; background:rgba(0,0,0,0.4); padding:0.75rem; border-radius:8px;">${escapeHtml(c.text)}</div>
    </div>
  `;

  const citationsOutput = document.getElementById('citations-output');
  // Check if detail container already exists
  let detailBox = document.getElementById('citation-detail-view');
  if (!detailBox) {
    detailBox = document.createElement('div');
    detailBox.id = 'citation-detail-view';
    citationsOutput.prepend(detailBox);
  }
  detailBox.innerHTML = detailHtml;
}

// Load All Citizen Procedures for Tab 2
async function loadAllProcedures() {
  const grid = document.getElementById('all-procedures-grid');
  try {
    const res = await fetch('/api/procedures');
    const data = await res.json();
    const procs = data.procedures || [];

    grid.innerHTML = procs.map(p => `
      <div class="procedure-card" style="margin-bottom:0;">
        <div class="procedure-title">
          <span>${escapeHtml(p.title)}</span>
          <span class="procedure-badge">${escapeHtml(p.short_act)}</span>
        </div>
        <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:0.6rem;">${escapeHtml(p.summary)}</p>
        <div style="font-size:0.82rem; color:var(--text-gold); margin-bottom:0.75rem; background:rgba(245,158,11,0.1); padding:0.4rem 0.6rem; border-radius:6px;">
          ⏳ <strong>Timeline:</strong> ${escapeHtml(p.timeline)}<br>
          💵 <strong>Fee:</strong> ${escapeHtml(p.fee)}
        </div>
        <div class="procedure-steps-list">
          ${p.steps.map(s => `
            <div class="step-item">
              <div class="step-item-title">Step ${s.step}: ${escapeHtml(s.title)}</div>
              <div class="step-item-desc">${escapeHtml(s.description)}</div>
            </div>
          `).join('')}
        </div>
        <div style="margin-top:0.75rem; padding-top:0.5rem; border-top:1px dashed var(--border-color); font-size:0.78rem; color:var(--text-emerald);">
          ℹ️ ${escapeHtml(p.important_note)}
        </div>
      </div>
    `).join('');
  } catch (err) {
    grid.innerHTML = `<p style="color:var(--text-muted);">Failed to load procedure guides.</p>`;
  }
}

// Direct Legalese Simplifier Handler
async function handleDirectSimplification() {
  const text = document.getElementById('raw-legal-text').value.trim();
  const wrapper = document.getElementById('simplifier-output-wrapper');
  const output = document.getElementById('simplifier-output');

  if (!text) return;

  wrapper.classList.remove('hidden');
  output.innerHTML = 'Simplifying text...';

  try {
    const res = await fetch('/api/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });
    const data = await res.json();
    output.innerHTML = formatMarkdown(data.simplified_summary);
  } catch (err) {
    output.innerHTML = '<p style="color:#ef4444;">Simplification failed.</p>';
  }
}

// Export Summary as PDF
function exportSummaryPDF() {
  const element = document.getElementById('summary-panel');
  const opt = {
    margin:       0.5,
    filename:     'AI_Legal_Assistant_Summary.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, backgroundColor: '#070d0d' },
    jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
  };
  html2pdf().set(opt).from(element).save();
}

// Markdown Formatter Utility
function formatMarkdown(text) {
  if (!text) return '';

  let html = text
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n\n/g, '<br><br>')
    .replace(/^\- (.*$)/gim, '<ul><li>$1</li></ul>')
    .replace(/^• (.*$)/gim, '<ul><li>$1</li></ul>');

  // Clean double nested lists
  html = html.replace(/<\/ul>\s*<ul>/g, '');
  return html;
}

// BNS Section Converter Logic
async function loadBnsMappings(query = '') {
  const container = document.getElementById('bns-mapping-results');
  if (!container) return;

  try {
    const res = await fetch(`/api/bns-mapper?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    const mappings = data.mappings || [];

    if (mappings.length === 0) {
      container.innerHTML = `<p style="color:var(--text-muted); padding:1rem;">No matching section mapping found.</p>`;
      return;
    }

    container.innerHTML = mappings.map(m => `
      <div style="background:rgba(7,13,13,0.7); border:1px solid var(--border-color); border-radius:12px; padding:1rem; margin-bottom:0.85rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
          <span style="color:#ef4444; font-weight:700; font-size:0.9rem; background:rgba(239,68,68,0.15); padding:0.15rem 0.5rem; border-radius:6px;">Old: ${escapeHtml(m.old)}</span>
          <span style="color:var(--text-emerald); font-weight:700; font-size:0.9rem; background:rgba(16,185,129,0.15); padding:0.15rem 0.5rem; border-radius:6px;">New: ${escapeHtml(m.new)}</span>
        </div>
        <p style="font-size:0.85rem; color:var(--text-muted);">${escapeHtml(m.notes)}</p>
      </div>
    `).join('');
  } catch (err) {
    container.innerHTML = `<p style="color:#ef4444;">Failed to load BNS mappings.</p>`;
  }
}

function handleBnsSearch() {
  const q = document.getElementById('bns-search-input').value.trim();
  loadBnsMappings(q);
}

// Action Readiness Scorecard Logic
function updateScorecardQuestions() {
  const type = document.getElementById('scorecard-type').value;
  const area = document.getElementById('scorecard-questions-area');
  if (!area) return;

  if (type === 'cyber_fraud') {
    area.innerHTML = `
      <div style="margin-bottom:1rem;">
        <label style="display:block; font-size:0.9rem; margin-bottom:0.3rem;">Hours elapsed since transaction:</label>
        <input type="number" id="sc-time" value="2" style="width:100%; padding:0.5rem; background:var(--bg-dark); color:white; border:1px solid var(--border-color); border-radius:8px;" />
      </div>
      <div style="display:flex; flex-direction:column; gap:0.5rem;">
        <label><input type="checkbox" id="sc-1930" checked /> Called 1930 National Cyber Crime Helpline</label>
        <label><input type="checkbox" id="sc-bank" checked /> Notified Bank to freeze cards/account</label>
        <label><input type="checkbox" id="sc-proof" checked /> Have SMS & Transaction ID proof</label>
      </div>
    `;
  } else if (type === 'consumer') {
    area.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:0.5rem;">
        <label><input type="checkbox" id="sc-invoice" checked /> Have Tax Invoice / Receipt</label>
        <label><input type="checkbox" id="sc-notice" /> Sent 15-day written notice to seller</label>
        <label><input type="checkbox" id="sc-2years" checked /> Purchase within last 2 years</label>
      </div>
    `;
  } else {
    area.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:0.5rem;">
        <label><input type="checkbox" id="sc-dept" checked /> Identified exact Ministry / Public Authority</label>
        <label><input type="checkbox" id="sc-questions" checked /> Formulated specific questions (file status/certified copy)</label>
        <label><input type="checkbox" id="sc-bpl" /> Belongs to BPL cardholder family (Free fee)</label>
      </div>
    `;
  }
}

async function calculateScorecard() {
  const type = document.getElementById('scorecard-type').value;
  let answers = {};

  if (type === 'cyber_fraud') {
    answers = {
      time_elapsed_hours: parseFloat(document.getElementById('sc-time').value || 24),
      called_1930: document.getElementById('sc-1930').checked,
      notified_bank: document.getElementById('sc-bank').checked,
      has_txn_proof: document.getElementById('sc-proof').checked
    };
  } else if (type === 'consumer') {
    answers = {
      has_invoice: document.getElementById('sc-invoice').checked,
      notice_sent: document.getElementById('sc-notice').checked,
      within_2_years: document.getElementById('sc-2years').checked
    };
  } else {
    answers = {
      knows_department: document.getElementById('sc-dept').checked,
      has_specific_questions: document.getElementById('sc-questions').checked,
      is_bpl: document.getElementById('sc-bpl').checked
    };
  }

  try {
    const res = await fetch('/api/scorecard', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_type: type, answers: answers })
    });
    const data = await res.json();

    const box = document.getElementById('scorecard-result-box');
    box.classList.remove('hidden');
    document.getElementById('score-display-number').innerText = `Empowerment Score: ${data.score}%`;
    document.getElementById('score-display-level').innerText = `Status: ${data.readiness_level}`;
    document.getElementById('score-display-factors').innerHTML = data.factors.map(f => `<p style="margin-bottom:0.3rem;">${escapeHtml(f)}</p>`).join('');
  } catch (err) {
    alert('Calculation failed.');
  }
}

// Helper to escape HTML characters
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
