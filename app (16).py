"""Streamlit shell: renders the whole Q2O app as ONE HTML component (single-page,
views toggled by JS exactly like the original HTML). No parent navigation is
ever attempted, so the iframe sandbox cannot block anything."""

import json
import streamlit as st
import streamlit.components.v1 as components

from theme import page, header_html, API_URL
import page_order_entry
import page_processing
import page_validation
import page_results

st.set_page_config(page_title="Quote to Order Drafting Agent", layout="wide",
                   initial_sidebar_state="collapsed")

# ULTRA-AGGRESSIVE CSS to remove ALL gaps and headers
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');
  /* Reset everything */
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    height: 100% !important;
    overflow: hidden !important;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
  }
  
  /* Kill ALL Streamlit headers, toolbars, and decorations */
  header[data-testid="stHeader"],
  .stAppHeader,
  [data-testid="stHeader"],
  [data-testid="stToolbar"],
  [data-testid="stDecoration"],
  [data-testid="stSidebar"],
  [data-testid="collapsedControl"],
  #MainMenu,
  footer,
  .stApp > header,
  .main > header,
  .css-1ps4mg5,
  .css-1rs6os,
  .css-1l02zno,
  .css-1v3fvcr,
  .css-1dp5vir,
  .css-1ht1j8u,
  .css-1r6slb0,
  .css-1aumxhk,
  .e1f1d6gn0,
  .e1f1d6gn1,
  .e1f1d6gn2,
  .e1f1d6gn3,
  .e1f1d6gn4,
  .e1f1d6gn5,
  .e1f1d6gn6 {
    display: none !important;
    height: 0px !important;
    min-height: 0px !important;
    max-height: 0px !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    clip: rect(0, 0, 0, 0) !important;
    position: absolute !important;
    overflow: hidden !important;
  }

  /* Remove ALL padding/margin from main containers */
  .stApp,
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"],
  [data-testid="stMainBlockContainer"],
  section.main,
  .main,
  .block-container,
  [data-testid="stVerticalBlock"],
  [data-testid="element-container"],
  [data-testid="stElementContainer"],
  [data-testid="stIFrame"],
  div:has(> iframe) {
    margin: 0 !important;
    padding: 0 !important;
    top: 0 !important;
    gap: 0 !important;
    border: 0 !important;
    background: #f8f9fa !important;
  }

  /* Force app container to full height with no offset */
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"] {
    height: 100vh !important;
    max-height: 100vh !important;
    min-height: 100vh !important;
    overflow: hidden !important;
    margin-top: 0 !important;
    padding-top: 0 !important;
  }

  /* Remove any extra padding from the main block */
  .block-container,
  [data-testid="stMainBlockContainer"] {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
  }

  /* Iframe should fill entire container */
  iframe {
    display: block !important;
    height: 100vh !important;
    width: 100% !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    vertical-align: top !important;
  }

  /* Remove any app-level padding/gaps */
  .st-emotion-cache-1r6slb0,
  .st-emotion-cache-1dp5vir,
  .st-emotion-cache-1v3fvcr,
  .st-emotion-cache-1l02zno,
  .st-emotion-cache-1rs6os,
  .st-emotion-cache-1ps4mg5 {
    padding-top: 0 !important;
    margin-top: 0 !important;
  }
</style>
""", unsafe_allow_html=True)

# SUPER AGGRESSIVE JavaScript injection via multiple methods
# Method 1: components.html with script
components.html("""
<script>
  (function() {
    // Immediately execute
    function killStreamlitHeader() {
      try {
        const doc = window.parent.document;
        const body = doc.body;
        
        // Find and destroy ALL possible header elements
        const selectors = [
          '[data-testid="stHeader"]',
          '.stAppHeader',
          'header[data-testid="stHeader"]',
          '.stApp > header',
          '.main > header',
          '.css-1ps4mg5',
          '.css-1rs6os',
          '.css-1l02zno',
          '.css-1v3fvcr',
          '.e1f1d6gn0',
          '.e1f1d6gn1',
          '.e1f1d6gn2',
          '.e1f1d6gn3',
          '.e1f1d6gn4',
          '.e1f1d6gn5'
        ];
        
        selectors.forEach(selector => {
          const els = doc.querySelectorAll(selector);
          els.forEach(el => {
            // Remove completely
            if (el && el.parentNode) {
              el.style.setProperty('display', 'none', 'important');
              el.style.setProperty('height', '0px', 'important');
              el.style.setProperty('min-height', '0px', 'important');
              el.style.setProperty('max-height', '0px', 'important');
              el.style.setProperty('visibility', 'hidden', 'important');
              el.style.setProperty('opacity', '0', 'important');
              el.style.setProperty('pointer-events', 'none', 'important');
              el.style.setProperty('margin', '0', 'important');
              el.style.setProperty('padding', '0', 'important');
              el.style.setProperty('border', '0', 'important');
              el.style.setProperty('overflow', 'hidden', 'important');
              el.style.setProperty('position', 'absolute', 'important');
              el.style.setProperty('clip', 'rect(0,0,0,0)', 'important');
              // Try to remove from DOM
              try { el.remove(); } catch(e) {}
            }
          });
        });
        
        // Fix the app container positioning
        const appContainer = doc.querySelector('[data-testid="stAppViewContainer"]');
        if (appContainer) {
          appContainer.style.setProperty('margin-top', '0', 'important');
          appContainer.style.setProperty('padding-top', '0', 'important');
          appContainer.style.setProperty('top', '0', 'important');
        }
        
        // Remove any empty space from body
        if (body) {
          body.style.setProperty('margin', '0', 'important');
          body.style.setProperty('padding', '0', 'important');
          body.style.setProperty('padding-top', '0', 'important');
          body.style.setProperty('margin-top', '0', 'important');
        }
      } catch(e) {
        // Silently fail
      }
    }
    
    // Run immediately
    killStreamlitHeader();
    
    // Run on DOM changes
    const observer = new MutationObserver(function(mutations) {
      killStreamlitHeader();
    });
    
    try {
      observer.observe(window.parent.document.body, {
        childList: true,
        subtree: true,
        attributes: true
      });
    } catch(e) {}
    
    // Also run periodically to catch any late-loading elements
    setInterval(killStreamlitHeader, 100);
  })();
</script>
""", height=0, width=0)

# Method 2: Additional inline script via st.markdown (bypasses iframe)
st.markdown("""
<script>
  (function() {
    function killHeaders() {
      const selectors = [
        '[data-testid="stHeader"]', '.stAppHeader', 'header[data-testid="stHeader"]',
        '.stApp > header', '.main > header', '.css-1ps4mg5', '.css-1rs6os',
        '.css-1l02zno', '.css-1v3fvcr', '.e1f1d6gn0', '.e1f1d6gn1',
        '.e1f1d6gn2', '.e1f1d6gn3', '.e1f1d6gn4', '.e1f1d6gn5'
      ];
      selectors.forEach(s => {
        document.querySelectorAll(s).forEach(el => {
          el.style.display = 'none !important';
          el.style.height = '0px !important';
          el.style.minHeight = '0px !important';
          el.style.maxHeight = '0px !important';
          el.style.visibility = 'hidden !important';
          el.style.opacity = '0 !important';
          el.style.margin = '0 !important';
          el.style.padding = '0 !important';
        });
      });
      const app = document.querySelector('[data-testid="stAppViewContainer"]');
      if (app) {
        app.style.marginTop = '0 !important';
        app.style.paddingTop = '0 !important';
        app.style.top = '0 !important';
      }
    }
    killHeaders();
    new MutationObserver(killHeaders).observe(document.body, {childList: true, subtree: true});
    setInterval(killHeaders, 100);
  })();
</script>
""", unsafe_allow_html=True)

# Method 3: Force iframe to be full height with no gaps
components.html("""
<style>
  /* Make sure the iframe itself has no gaps */
  iframe {
    display: block !important;
    height: 100vh !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    vertical-align: top !important;
  }
</style>
""", height=0, width=0)

CONTROLLER_JS = """
<script>
  const API = __API__;
  let OPP = '';
  let RESULT = null;
  // One session id per app session (page load). Used for app-run logging so
  // each user session is tracked separately.
  const SESSION_ID = 's-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8);

  // ---------- View Navigator (same as original HTML) ----------
  function showSection(sectionId) {
    document.getElementById('view-ingestion').style.display = 'none';
    document.getElementById('view-processing').style.display = 'none';
    document.getElementById('view-validation').style.display = 'none';
    document.getElementById('view-results').style.display = 'none';
    if (sectionId === 'ingestion') document.getElementById('view-ingestion').style.display = 'flex';
    else if (sectionId === 'processing') document.getElementById('view-processing').style.display = 'flex';
    else if (sectionId === 'validation') { renderValidation(); document.getElementById('view-validation').style.display = 'block'; }
    else if (sectionId === 'results') { renderResults(); document.getElementById('view-results').style.display = 'flex'; }
    window.scrollTo(0, 0);
  }

  function handleOpportunityInput(input) {
    const btn = document.getElementById('begin-btn');
    if (input.value.trim().length > 0) {
      btn.disabled = false;
      btn.classList.remove('bg-gray-200','text-gray-400','cursor-not-allowed');
      btn.classList.add('bg-primary','hover:bg-red-700','text-white','cursor-pointer');
    } else {
      btn.disabled = true;
      btn.classList.add('bg-gray-200','text-gray-400','cursor-not-allowed');
      btn.classList.remove('bg-primary','hover:bg-red-700','text-white','cursor-pointer');
    }
  }

  function resetToLanding() {
    const inp = document.getElementById('opportunity-id');
    inp.value = ''; handleOpportunityInput(inp);
    RESULT = null; OPP = '';
    resetProcessingView();
    showSection('ingestion');
  }

  // ---------- Processing ----------
  const CIRC = 2 * Math.PI * 44;
  let progress = 0, procDone = false, currentStep = 1, creepTimer = null;
  const stepThresholds = [15, 30, 50, 65, 80, 100];
  const fillPct = ['80%','60%','40%','20%','0%','0%'];
  const statusMessages = ['Ingesting raw data...','Parsing documents...','Checking order acceptance criteria...',
                          'Cross-checking knowledge base...','Evaluating data integrity...','Drafting order...'];

  function resetProcessingView() {
    progress = 0; procDone = false; currentStep = 1;
    if (creepTimer) { clearInterval(creepTimer); creepTimer = null; }
    const $ = (id) => document.getElementById(id);
    for (let n = 1; n <= 6; n++) {
      const node = $('pn'+n), icon = $('pi'+n), title = $('pt'+n), err = $('pe'+n);
      if (node) node.className = 'proc-node';
      if (icon) icon.innerText = n;
      if (title) title.className = 'proc-step-title';
      if (err) { err.style.display = 'none'; err.innerText = ''; }
    }
    const fill = $('proc-fill-line'); if (fill) fill.style.bottom = '100%';
    const ring = $('proc-ring-fill'); if (ring) ring.setAttribute('stroke-dashoffset', CIRC);
    const pct = $('progress-percent'); if (pct) pct.innerText = '0';
    const statusEl = $('proc-status');
    if (statusEl) { statusEl.classList.add('animate-pulse'); statusEl.style.color = ''; statusEl.style.fontWeight = ''; statusEl.innerText = 'Ingesting raw data...'; }
    const pctLabel = $('pct-label');
    if (pctLabel) { pctLabel.innerText = 'Processing'; pctLabel.classList.add('animate-pulse'); }
    const echoIcon = $('echo-icon');
    if (echoIcon) { echoIcon.classList.add('animate-spin'); echoIcon.innerText = 'sync'; }
    const echo = $('proc-echo'); if (echo) echo.style.color = '';
    const fa = $('fail-actions'); if (fa) fa.style.display = 'none';
  }

  function setActive(n) {
    document.getElementById('pn'+n).classList.add('active');
    document.getElementById('pt'+n).classList.add('active-t');
  }
  function setDone(n) {
    const node = document.getElementById('pn'+n), icon = document.getElementById('pi'+n),
          title = document.getElementById('pt'+n);
    node.classList.remove('active'); node.classList.add('done');
    title.classList.remove('active-t'); title.classList.add('done-t');
    icon.innerHTML = '<span class="material-symbols-outlined" style="font-size:14px;">check</span>';
  }
  function setFailed(n, msg) {
    const node = document.getElementById('pn'+n), icon = document.getElementById('pi'+n),
          title = document.getElementById('pt'+n), err = document.getElementById('pe'+n);
    node.classList.remove('active'); node.classList.add('failed');
    title.classList.remove('active-t'); title.classList.add('failed-t');
    icon.innerHTML = '<span class="material-symbols-outlined" style="font-size:14px;">close</span>';
    err.style.display = 'block'; err.innerText = msg;
    const statusEl = document.getElementById('proc-status');
    statusEl.classList.remove('animate-pulse');
    statusEl.style.color = '#e60000'; statusEl.style.fontWeight = '700';
    statusEl.innerText = 'Processing halted - validation issues detected';
    const pctLabel = document.getElementById('pct-label');
    pctLabel.innerText = 'Attention'; pctLabel.classList.remove('animate-pulse');
    const echoIcon = document.getElementById('echo-icon');
    echoIcon.classList.remove('animate-spin'); echoIcon.innerText = 'error';
    document.getElementById('proc-echo').style.color = '#e60000';
    document.getElementById('proc-echo-text').innerText = 'Review required for Opportunity ID: ' + OPP;
    document.getElementById('fail-actions').style.display = 'flex';
    procDone = true;
  }
  function paint() {
    document.getElementById('proc-ring-fill').setAttribute('stroke-dashoffset', CIRC - (progress/100)*CIRC);
    document.getElementById('progress-percent').innerText = Math.round(progress);
    while (currentStep <= 6 && progress >= stepThresholds[currentStep-1]) {
      setDone(currentStep);
      document.getElementById('proc-fill-line').style.bottom = fillPct[currentStep-1];
      currentStep++;
      if (currentStep <= 6) setActive(currentStep);
    }
  }

  // Poll the backend for REAL processing progress and reflect it on the
  // step nodes. Best-effort: if a poll fails, we simply try again; the fake
  // creep animation still runs underneath as a smooth visual.
  let statusPoll = null;
  const STEP_INDEX = { // backend node key -> processing node number (1-based)
    'qto_retrieval_agent': 1,
    'product_code_agent': 2,
    'bsp_extraction_agent': 3,
    'email_agent': 4,
  };
  function startStatusPolling() {
    if (statusPoll) clearInterval(statusPoll);
    statusPoll = setInterval(() => {
      if (procDone) { clearInterval(statusPoll); statusPoll = null; return; }
      fetch(API + '/status/' + encodeURIComponent(OPP))
        .then(r => r.json())
        .then(st => {
          if (!st || !st.steps) return;
          // find the furthest active/done step and reflect it
          let activeNum = 1;
          st.steps.forEach(s => {
            const num = STEP_INDEX[s.key];
            if (!num) return;
            if (s.state === 'active') activeNum = Math.max(activeNum, num);
            if (s.state === 'done')   activeNum = Math.max(activeNum, num);
            // update the label with friendly text + technical detail
            const titleEl = document.getElementById('pt' + num);
            if (titleEl) titleEl.innerText = s.label;
          });
          if (activeNum !== currentStep) setActive(activeNum);
          // let the status line show the real friendly label
          const active = st.steps.find(s => s.state === 'active');
          if (active) document.getElementById('proc-status').innerText = active.label + '...';
        })
        .catch(() => {}); // ignore transient poll errors
    }, 1000);
  }

  function startProcessing() {
    const oppId = document.getElementById('opportunity-id').value.trim();
    if (!oppId) return;
    OPP = oppId;

    // Check the opportunity exists (its validation.json is present) BEFORE
    // moving to the processing page. If not found, show an alert and stop.
    const btn = document.getElementById('begin-btn');
    const origLabel = btn ? btn.innerHTML : '';
    if (btn) { btn.disabled = true; btn.innerHTML = 'Checking...'; }

    fetch(API + '/exists/' + encodeURIComponent(oppId))
      .then(r => r.json())
      .then(res => {
        if (btn) { btn.disabled = false; btn.innerHTML = origLabel; }
        if (res && res.exists) {
          // Write the initial app log for this session now that the user has
          // clicked "Begin Order Creation Process" on a valid opportunity.
          // Best effort - never blocks the run.
          try {
            fetch(API + '/log', {
              method: 'POST', headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ session_id: SESSION_ID, opp_id: OPP })
            }).catch(() => {});
          } catch (e) {}
          runProcessing();
        } else {
          showOppNotFound(oppId);
        }
      })
      .catch(() => {
        // If the check itself fails (network/backend down), don't silently
        // block - fall through and let the run surface the real error.
        if (btn) { btn.disabled = false; btn.innerHTML = origLabel; }
        runProcessing();
      });
  }

  // Alert shown when the opportunity id isn't found in the processed folder.
  function showOppNotFound(oppId) {
    let modal = document.getElementById('opp-notfound-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'opp-notfound-modal';
      modal.style.cssText = 'position:fixed;inset:0;z-index:200;background:rgba(0,0,0,0.35);display:flex;align-items:center;justify-content:center;';
      modal.innerHTML =
        '<div style="background:#fff;border-radius:16px;max-width:460px;width:92vw;box-shadow:0 10px 40px rgba(0,0,0,0.2);overflow:hidden;">' +
          '<div style="display:flex;align-items:center;gap:10px;padding:18px 22px;border-bottom:1px solid #eee;">' +
            '<span class="material-symbols-outlined" style="color:#e60000;">error</span>' +
            '<h3 style="margin:0;font-size:17px;font-weight:700;color:#1f1f1f;">Opportunity Not Found</h3>' +
          '</div>' +
          '<div style="padding:20px 22px;font-size:14px;color:#444;line-height:1.5;">' +
            '<p style="margin:0 0 10px;">Opportunity ID <b id="opp-nf-id"></b> was not found in the processed folder.</p>' +
            '<p style="margin:0;">Please check the ID and try again later &mdash; it may still be in the processing phase, which can take up to <b>30 minutes</b>.</p>' +
          '</div>' +
          '<div style="display:flex;justify-content:flex-end;padding:14px 22px;border-top:1px solid #eee;">' +
            '<button onclick="closeOppNotFound()" ' +
              'style="padding:8px 18px;background:#e60000;color:#fff;border:none;border-radius:8px;font-size:14px;cursor:pointer;">Close</button>' +
          '</div>' +
        '</div>';
      document.body.appendChild(modal);
    }
    const idEl = document.getElementById('opp-nf-id');
    if (idEl) idEl.innerText = oppId;
    modal.style.display = 'flex';
  }

  function closeOppNotFound() {
    const m = document.getElementById('opp-notfound-modal');
    if (m) m.style.display = 'none';
  }

  // The actual processing run (moves to the processing page and calls /process).
  function runProcessing() {
    resetProcessingView();
    document.getElementById('proc-echo-text').innerText = 'Analyzing Opportunity ID: ' + OPP + '...';
    showSection('processing');
    setActive(1);
    startStatusPolling();   // real backend progress drives the step nodes
    creepTimer = setInterval(() => {
      if (procDone) { clearInterval(creepTimer); return; }
      if (progress < 60) {
        progress += 0.4; paint();
        document.getElementById('proc-status').innerText = statusMessages[Math.min(currentStep-1, 5)];
      }
    }, 120);

    fetch(API + '/process/' + encodeURIComponent(OPP), { method: 'POST' })
      .then(r => r.json())
      .then(data => {
        clearInterval(creepTimer);
        if (statusPoll) { clearInterval(statusPoll); statusPoll = null; }
        if (data.status === 'error') {
          RESULT = data; window.RESULT = data;
          progress = Math.max(progress, 12); paint();
          setFailed(1, 'Failed to retrieve/process opportunity data: ' + (data.message || 'unknown error') + ' - View Validation for details.');
          return;
        }
        normaliseForOrderType(data);   // drop circuit-only checks for non-circuit orders
        RESULT = data; window.RESULT = data;
        if (data.failed_count > 0) {
          progress = Math.max(progress, 42); paint();
          setFailed(3, data.failed_count + ' validation check(s) failed - order acceptance criteria not met. View Validation for details.');
          return;
        }
        const finish = setInterval(() => {
          progress += 2.5;
          if (progress >= 100) {
            progress = 100; paint(); clearInterval(finish);
            setDone(6);
            setTimeout(() => showSection('results'), 500);
          } else paint();
        }, 40);
      })
      .catch(err => {
        clearInterval(creepTimer);
        if (statusPoll) { clearInterval(statusPoll); statusPoll = null; }
        progress = Math.max(progress, 12); paint();
        setFailed(1, 'Agent API unreachable: ' + err + '. Check the agent service is running on ' + API);
      });
  }

  // ---------- Validation ----------
  function esc(s) { const d = document.createElement('div'); d.innerText = String(s == null ? '' : s); return d.innerHTML; }

  // Feedback dropdown options (owner of the follow-up action)
  const FEEDBACK_OPTIONS = [
    ["", "Select action..."],
    ["raise_mdg", "Raise with MDG"],
    ["raise_mdm", "Raise with MDM"],
    ["raise_sales", "Raise with Sales Team"],
    ["manual_correction", "Manual correction"],
    ["no_action", "No action needed"],
  ];

  // Single row renderer used for BOTH the Criteria Checklist and the Checks list.
  // Passed items render as a compact confirmed row. Failed items get the red
  // fail styling PLUS an inline "raise feedback" control so a reviewer can log
  // who owns the follow-up (BSP / MDM / MDG / Sales / manual / no action) and
  // an optional comment, right where the failure is shown.
  function itemRow(idx, c) {
    const ok = c.ok;
    const wide = idx >= 10 ? 'w-6' : 'w-4';

    if (ok) {
      return `
      <li class="flex items-start justify-between p-2.5 px-4 border-b border-surface-variant hover:bg-surface-container-low transition-colors">
        <div class="flex gap-2 items-start flex-1">
          <span class="font-label-sm text-secondary-fixed-dim ${wide} shrink-0">${idx}</span>
          <div class="flex flex-col flex-1">
            <span class="font-body-md text-sm text-on-surface leading-snug">${esc(c.label)}</span>
            ${c.description ? `<span class="text-[11px] text-secondary mt-0.5 leading-snug">${esc(c.description)}</span>` : ''}
          </div>
        </div>
        <span class="material-symbols-outlined text-tertiary shrink-0">check_circle</span>
      </li>`;
    }

    // Has a request already been raised for this check? (from validation
    // file's feedbacks list). If so, don't show the raise controls again.
    const R = (window.RESULT || RESULT || {});
    const raisedForKey = (R.feedbacks || []).filter(f => f.check_key === c.key);
    const alreadyRaised = raisedForKey.length > 0;
    const fb = alreadyRaised ? raisedForKey[raisedForKey.length - 1] : null;
    const selected = fb ? fb.option : (c.action && c.action !== 'none' ? c.action : '');
    const opts = FEEDBACK_OPTIONS.map(([v, l]) =>
      `<option value="${v}" ${v === selected ? 'selected' : ''}>${esc(l)}</option>`).join('');

    const isSaved = alreadyRaised;
    // Panel is collapsed by default in ALL cases (unsaved or saved) - the
    // action/comment controls only appear once the reviewer explicitly asks
    // for them, so a failed row doesn't look noisy or half-filled-in.
    const panelId = `fb-panel-${c.key}`;
    const toggleBtn = isSaved ? `
      <span class="text-[11px] font-medium text-tertiary flex items-center gap-1 shrink-0">
        <span class="material-symbols-outlined text-[14px]" style="font-variation-settings:'FILL' 1;">check_circle</span>
        Request raised
      </span>` : `
      <button type="button" onclick="toggleFeedbackPanel('${c.key}')"
        class="text-[11px] font-medium text-primary hover:underline flex items-center gap-1 shrink-0">
        <span class="material-symbols-outlined text-[14px]">flag</span>
        Raise Request
      </button>`;

    const savedLine = isSaved && fb ? `
      <div class="mt-1 text-[11px] text-secondary">
        <span class="font-mono bg-gray-100 px-1.5 py-0.5 rounded">${esc(FEEDBACK_LABEL(fb.option))}</span>
        ${fb.comment ? '<span class="ml-1">' + esc(fb.comment) + '</span>' : ''}
      </div>` : '';

    const panel = `
      <div id="${panelId}" class="mt-2 flex flex-wrap items-center gap-2" style="display:none;">
        <select id="fb-opt-${c.key}" class="text-[11px] border border-gray-300 rounded px-3 py-1 bg-white text-on-surface min-w-[220px]">
          ${opts}
        </select>
        <input id="fb-cmt-${c.key}" type="text" placeholder="Comment (optional)"
          value="${fb && fb.comment ? esc(fb.comment) : ''}"
          class="text-[11px] border border-gray-300 rounded px-2 py-1 bg-white flex-1 min-w-[160px]">
        <button id="fb-save-${c.key}" onclick="saveFeedback('${c.key}')"
          class="text-[10px] uppercase tracking-wider px-3 py-1 rounded bg-sidebar-dark text-white hover:bg-black"
          style="font-family:'JetBrains Mono',monospace;">Save</button>
        <span id="fb-status-${c.key}" class="text-[10px] text-secondary"></span>
      </div>`;

    return `
      <li class="flex flex-col p-2.5 px-4 border-b border-surface-variant bg-[#fff0f0] border-l-4 border-l-primary">
        <div class="flex items-start justify-between gap-2">
          <div class="flex gap-2 items-start flex-1">
            <span class="font-label-sm text-secondary ${wide} shrink-0 pt-0.5">${idx}</span>
            <div class="flex flex-col flex-1">
              <span class="font-button text-sm text-on-surface font-bold leading-snug">${esc(c.label)}</span>
              ${c.description ? `<span class="text-[11px] text-secondary mt-0.5 leading-snug">${esc(c.description)}</span>` : ''}
              <span class="font-label-sm text-[11px] text-error mt-0.5">${esc(c.notes || 'Not verified')}</span>
              ${savedLine}
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0 pt-0.5">
            ${toggleBtn}
            <span class="material-symbols-outlined text-primary">cancel</span>
          </div>
        </div>
        ${panel}
      </li>`;
  }

  function FEEDBACK_LABEL(v) {
    const hit = FEEDBACK_OPTIONS.find(([val]) => val === v);
    return hit ? hit[1] : (v || 'Action pending');
  }

  function toggleFeedbackPanel(key) {
    const el = document.getElementById('fb-panel-' + key);
    if (!el) return;
    el.style.display = (el.style.display === 'none') ? 'flex' : 'none';
  }

  function saveFeedback(key) {
    const opt = document.getElementById('fb-opt-' + key).value;
    const cmt = document.getElementById('fb-cmt-' + key).value;
    const statusEl = document.getElementById('fb-status-' + key);
    if (!opt) { statusEl.style.color = '#e60000'; statusEl.innerText = 'Pick an action first'; return; }
    statusEl.style.color = '#6b7280'; statusEl.innerText = 'Saving...';
    fetch(API + '/feedback/' + encodeURIComponent(OPP), {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ check_key: key, option: opt, comment: cmt, by: 'ui', session_id: SESSION_ID })
    }).then(r => r.json()).then(res => {
      if (res.status === 'success') {
        statusEl.style.color = '#107c10';
        statusEl.innerText = 'Request raised';
        // Hide the Save button + inputs now that the request is saved.
        const saveBtn = document.getElementById('fb-save-' + key);
        if (saveBtn) saveBtn.style.display = 'none';
        const optEl = document.getElementById('fb-opt-' + key);
        const cmtEl = document.getElementById('fb-cmt-' + key);
        if (optEl) optEl.disabled = true;
        if (cmtEl) cmtEl.disabled = true;
        // The API returns the full feedbacks list - use it as the source of truth.
        const R = (window.RESULT || RESULT || {});
        R.feedbacks = res.feedbacks || (R.feedbacks || []).concat([res.feedback]);
        renderFeedbacks();   // refresh the raised-requests list without wiping row state
      } else {
        statusEl.style.color = '#e60000';
        statusEl.innerText = res.message || 'Save failed';
      }
    }).catch(err => { statusEl.style.color = '#e60000'; statusEl.innerText = 'Error: ' + err; });
  }

  // Enable "Proceed to Order Creation" only when every FAILED check has a
  // raised request against it. Otherwise keep it disabled (greyed out).
  function updateProceedButton() {
    const btn = document.getElementById('proceed-btn');
    if (!btn) return;
    const R = (window.RESULT || RESULT || {});
    const isCircuit = !!R.is_circuit;
    const allItems = []
      .concat(stripCircuitOnly(R.criteria || [], isCircuit))
      .concat(stripCircuitOnly(R.checks || [], isCircuit))
      .concat(R.base_checks || [])
      .concat(isCircuit ? (R.circuit_checks || []) : []);
    const failedKeys = allItems.filter(i => !i.ok).map(i => i.key);
    const raisedKeys = new Set((R.feedbacks || []).map(f => f.check_key));
    // every failed check must have at least one raised request
    const allCovered = failedKeys.length === 0 || failedKeys.every(k => raisedKeys.has(k));

    const onCls = ['bg-tertiary-container','text-white','hover:bg-tertiary','cursor-pointer'];
    const offCls = ['bg-gray-200','text-gray-400','cursor-not-allowed'];
    if (allCovered) {
      btn.disabled = false;
      offCls.forEach(c => btn.classList.remove(c));
      onCls.forEach(c => btn.classList.add(c));
      btn.title = '';
    } else {
      btn.disabled = true;
      onCls.forEach(c => btn.classList.remove(c));
      offCls.forEach(c => btn.classList.add(c));
      const remaining = failedKeys.filter(k => !raisedKeys.has(k)).length;
      btn.title = 'Raise a request for all ' + remaining + ' remaining failed check(s) to proceed.';
    }
  }

  // Guarded proceed - only navigates when the button is enabled.
  function tryProceed() {
    const btn = document.getElementById('proceed-btn');
    if (btn && btn.disabled) return;
    showSection('results');
  }

  // ── Raise a request from the Raised Requests section (+ button) ──────
  // Lists only FAILED checks that do not already have a request, by title,
  // filtered as the user types.
  function failedChecksWithoutRequest() {
    const R = (window.RESULT || RESULT || {});
    const isCircuit = !!R.is_circuit;
    const all = []
      .concat(stripCircuitOnly(R.criteria || [], isCircuit))
      .concat(stripCircuitOnly(R.checks || [], isCircuit))
      .concat(R.base_checks || [])
      .concat(isCircuit ? (R.circuit_checks || []) : []);
    const raised = new Set((R.feedbacks || []).map(f => f.check_key));
    return all.filter(c => !c.ok && !raised.has(c.key));
  }

  function filterFailedChecks() {
    const term = (document.getElementById('fb-new-search').value || '').toLowerCase();
    const sel = document.getElementById('fb-new-check');
    const empty = document.getElementById('fb-new-empty');
    if (!sel) return;
    const items = failedChecksWithoutRequest()
      .filter(c => !term || String(c.label).toLowerCase().includes(term)
                        || String(c.key).toLowerCase().includes(term));
    sel.innerHTML = items.map(c =>
      `<option value="${esc(c.key)}">${esc(c.label)}</option>`).join('');
    const none = items.length === 0;
    if (empty) empty.style.display = none ? 'block' : 'none';
    sel.style.display = none ? 'none' : 'block';
  }

  function toggleNewRequest(show) {
    const form = document.getElementById('fb-new-form');
    if (!form) return;
    const open = (show === undefined) ? (form.style.display === 'none') : !!show;
    form.style.display = open ? 'block' : 'none';
    if (open) {
      document.getElementById('fb-new-search').value = '';
      document.getElementById('fb-new-cmt').value = '';
      document.getElementById('fb-new-status').innerText = '';
      const opt = document.getElementById('fb-new-opt');
      opt.innerHTML = FEEDBACK_OPTIONS.map(([v, l]) =>
        `<option value="${v}">${esc(l)}</option>`).join('');
      filterFailedChecks();
      document.getElementById('fb-new-search').focus();
    }
  }

  function submitNewRequest() {
    const sel = document.getElementById('fb-new-check');
    const key = sel && sel.value;
    const opt = document.getElementById('fb-new-opt').value;
    const cmt = document.getElementById('fb-new-cmt').value;
    const statusEl = document.getElementById('fb-new-status');
    if (!key) { statusEl.style.color = '#e60000'; statusEl.innerText = 'Pick a failed check'; return; }
    if (!opt) { statusEl.style.color = '#e60000'; statusEl.innerText = 'Pick an action'; return; }
    statusEl.style.color = '#6b7280'; statusEl.innerText = 'Saving...';
    fetch(API + '/feedback/' + encodeURIComponent(OPP), {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ check_key: key, option: opt, comment: cmt,
                             by: 'ui', session_id: SESSION_ID })
    }).then(r => r.json()).then(res => {
      if (res.status === 'success') {
        const R = (window.RESULT || RESULT || {});
        R.feedbacks = res.feedbacks || (R.feedbacks || []).concat([res.feedback]);
        statusEl.style.color = '#107c10';
        statusEl.innerText = 'Request raised';
        renderValidation();          // refresh rows, list and the proceed gate
        toggleNewRequest(false);
      } else {
        statusEl.style.color = '#e60000';
        statusEl.innerText = res.message || 'Save failed';
      }
    }).catch(err => { statusEl.style.color = '#e60000'; statusEl.innerText = 'Error: ' + err; });
  }

  // Render the SEPARATE feedbacks list (raised requests) - what the FE shows.
  // Find the full human label for a check key (e.g. "B10_vendor_quote..." ->
  // "Vendor quote still valid (within 30 days, not expired)"). Falls back to
  // the key if no match is found.
  function labelForCheckKey(key) {
    if (!key) return '';
    const R = (window.RESULT || RESULT || {});
    const all = [].concat(R.criteria || [], R.checks || [], R.base_checks || [], R.circuit_checks || []);
    const hit = all.find(c => c.key === key);
    return hit ? hit.label : key;
  }

  function renderFeedbacks() {
    const R = (window.RESULT || RESULT || {});
    const fbs = R.feedbacks || [];
    const host = document.getElementById('val-feedbacks-list');
    const countEl = document.getElementById('val-feedbacks-count');
    if (!host) return;
    if (countEl) countEl.innerText = fbs.length ? (fbs.length + (fbs.length === 1 ? ' request' : ' requests')) : '';
    if (!fbs.length) {
      host.innerHTML = '<div class="flex flex-col items-center justify-center py-8 text-center gap-1">' +
        '<span class="material-symbols-outlined text-gray-300 text-[28px]">inbox</span>' +
        '<span class="text-[12px] text-gray-400">No requests raised yet</span></div>';
      return;
    }
    host.innerHTML = fbs.map(f => {
      let dstr = '';
      if (f.date) {
        const d = new Date(f.date);
        if (!isNaN(d)) {
          const dd = String(d.getDate()).padStart(2, '0');
          const mm = String(d.getMonth() + 1).padStart(2, '0');
          dstr = dd + ' | ' + mm + ' | ' + d.getFullYear();
        } else { dstr = String(f.date).slice(0, 10); }
      }
      return `
      <li class="flex items-start gap-3 px-4 py-3.5 border-b border-gray-100 hover:bg-gray-50 transition-colors">
        <div class="mt-0.5 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
          <span class="material-symbols-outlined text-primary text-[18px]">flag</span>
        </div>
        <div class="flex flex-col flex-grow min-w-0">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-[14px] font-semibold text-gray-800">${esc(labelForCheckKey(f.check_key))}</span>
          </div>
          <span class="text-[12px] text-primary font-medium mt-0.5">${esc(FEEDBACK_LABEL(f.option))}</span>
          ${f.comment ? `<span class="text-[13px] text-gray-600 mt-1 leading-snug">${esc(f.comment)}</span>` : ''}
          <span class="text-[12px] text-gray-400 mt-1">${esc(dstr)}${f.by ? ' · ' + esc(f.by) : ''}</span>
        </div>
      </li>`;
    }).join('');
    updateProceedButton();   // re-evaluate the proceed gate whenever feedbacks change
    // Hide the + button when every failed check already has a request.
    const addBtn = document.getElementById('fb-add-btn');
    if (addBtn) addBtn.style.display = failedChecksWithoutRequest().length ? 'flex' : 'none';
  }

  // ── Checks that only make sense for CIRCUIT orders ──────────────
  // Hidden entirely when the order category is not Circuit (e.g. Kit).
  // Edit this list to tune what disappears for non-circuit orders.
  const CIRCUIT_ONLY_KEYS = [
    "R4_site_id",                     // Site ID - circuit orders only
    "C2_circuit_order_form_attached", // Circuit Order Form
    "C5_third_party_vendor_docs",     // eir / enet / SIRO / Ripplecom quotes
    "C6_infra_orders_product_speed",  // infra orders, product & speed
    "C11_lan_ip_for_dia",             // DIA LAN IP
    "C12_public_ip_range_approved",   // public IP ranges
    "C13_standard_offering_slash30",  // /30 standard offering
    "C18_bend_info_correct",          // B-End: EIL, SAB, eir exchange, enet NNI
    "C19_qos_af_ef_correct",          // QoS AF / EF %
  ];

  // Remove circuit-only items from the payload for non-circuit orders and
  // recompute the failure count so the loader, banner and lists all agree.
  function normaliseForOrderType(data) {
    const isCircuit = !!data.is_circuit;
    if (!isCircuit) {
      data.criteria = stripCircuitOnly(data.criteria || [], false);
      data.checks = stripCircuitOnly(data.checks || [], false);
      data.circuit_checks = [];
    }
    const all = (data.criteria || []).concat(
      data.checks || [], data.base_checks || [], isCircuit ? (data.circuit_checks || []) : []);
    data.failed_count = all.filter(i => !i.ok).length;
    return data;
  }

  function stripCircuitOnly(list, isCircuit) {
    if (isCircuit) return list;
    return (list || []).filter(c => CIRCUIT_ONLY_KEYS.indexOf(c.key) === -1);
  }

  // ── Topic-based grouping of validation checks ─────────────────────────
  // Each check key is mapped to a business topic. Order defines display order.
  // Any check not listed falls into "Other Checks".
  const TOPIC_ORDER = [
    'PO', 'Customer Quote', 'Vendor Quote', 'BSP', 'Tech Spec',
    'Site & Contact', 'Product & Kit', 'Pricing & Commercial',
    'Design & Summary', 'Circuit & Service', 'Other Checks',
  ];
  const TOPIC_MAP = {
    // PO
    R1: 'PO', C3: 'PO', B5: 'PO', X7: 'PO', X9: 'PO',
    // Customer Quote
    R2: 'Customer Quote', C24: 'Customer Quote',
    // Vendor Quote
    R3: 'Vendor Quote', C4: 'Vendor Quote', C5: 'Vendor Quote', C23: 'Vendor Quote',
    C26: 'Vendor Quote', B10: 'Vendor Quote', C16: 'Vendor Quote',
    // BSP
    B1: 'BSP', B2: 'BSP', B3: 'BSP', B8: 'BSP', B13: 'BSP', X6: 'BSP',
    // Tech Spec
    B4: 'Tech Spec', B7: 'Tech Spec', B11: 'Tech Spec', C27: 'Tech Spec',
    // Site & Contact
    R4: 'Site & Contact', R5: 'Site & Contact', C7: 'Site & Contact', C8: 'Site & Contact',
    // Product & Kit
    C14: 'Product & Kit', C15: 'Product & Kit', X5: 'Product & Kit',
    // Pricing & Commercial
    B6: 'Pricing & Commercial', C6: 'Pricing & Commercial',
    // Design & Summary
    R6: 'Design & Summary', R7: 'Design & Summary', C9: 'Design & Summary',
    // Circuit & Service
    C2: 'Circuit & Service', X1: 'Circuit & Service', X2: 'Circuit & Service',
    X3: 'Circuit & Service', X4: 'Circuit & Service', X8: 'Circuit & Service',
    // (everything else -> Other Checks)
  };

  // Extract the short id (e.g. "C24") from a check key like "C24_vf_quote...".
  function shortId(key) {
    return String(key || '').split('_')[0].toUpperCase();
  }

  // Group a flat list of check items into topic buckets, in TOPIC_ORDER.
  function groupByTopic(items) {
    const buckets = {};
    (items || []).forEach(c => {
      const topic = TOPIC_MAP[shortId(c.key)] || 'Other Checks';
      (buckets[topic] = buckets[topic] || []).push(c);
    });
    return TOPIC_ORDER
      .filter(t => buckets[t] && buckets[t].length)
      .map(t => ({ key: t.replace(/[^A-Za-z0-9]/g, '_'), title: t, items: buckets[t] }));
  }

  // Render one accordion group: a header with roll-up status (check/cross +
  // N/M passed) and a collapsible body listing the individual checks.
  // Failed groups are expanded by default; passed groups collapsed.
  function groupRow(g) {
    const items = g.items || [];
    const total = items.length;
    const passed = items.filter(i => i.ok).length;
    const allOk = passed === total && total > 0;
    const expanded = false;   // all groups collapsed by default

    const fillStyle = 'font-variation-settings:' + String.fromCharCode(39) + 'FILL' + String.fromCharCode(39) + ' 1;';
    const statusIcon = allOk
      ? '<span class="material-symbols-outlined text-tertiary" style="' + fillStyle + '">check_circle</span>'
      : '<span class="material-symbols-outlined text-primary" style="' + fillStyle + '">cancel</span>';

    const body = items.map((c, i) => itemRow(i + 1, c)).join('');

    return `
      <div class="border-b border-gray-200">
        <button type="button" onclick="toggleGroup('${g.key}')"
                class="w-full flex items-center justify-between px-4 py-3 bg-white hover:bg-gray-50 transition-colors text-left">
          <div class="flex items-center gap-3">
            <span id="grp-caret-${g.key}" class="material-symbols-outlined text-gray-400 transition-transform"
                  style="${expanded ? 'transform:rotate(90deg);' : ''}">chevron_right</span>
            <span class="font-semibold text-[14px] text-gray-800">${esc(g.title)}</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-[12px] font-medium ${allOk ? 'text-tertiary' : 'text-primary'}">${passed}/${total} passed</span>
            ${statusIcon}
          </div>
        </button>
        <ul id="grp-body-${g.key}" class="flex flex-col border-t border-gray-100" style="background-color:#fafafa; ${expanded ? '' : 'display:none;'}">
          ${body}
        </ul>
      </div>`;
  }

  function toggleGroup(key) {
    const body = document.getElementById('grp-body-' + key);
    const caret = document.getElementById('grp-caret-' + key);
    if (!body) return;
    const open = body.style.display !== 'none';
    body.style.display = open ? 'none' : '';
    if (caret) caret.style.transform = open ? '' : 'rotate(90deg)';
  }

  function renderValidation() {
    const data = RESULT || {};
    const isCircuit = !!data.is_circuit;
    // Circuit-specific items are removed entirely for non-circuit (e.g. Kit) orders.
    const criteria = stripCircuitOnly(data.criteria || [], isCircuit);
    const checks = stripCircuitOnly(data.checks || [], isCircuit);
    const baseChecks = data.base_checks || [], circuitChecks = data.circuit_checks || [];
    // BSP base checks and (for circuit orders) circuit checks are folded into
    // the single "Checks" list rather than shown as separate sections.
    const allChecks = checks.concat(baseChecks, isCircuit ? circuitChecks : []);
    const allItems = criteria.concat(allChecks);
    const failed = allItems.filter(i => !i.ok);

    document.getElementById('val-opp-subtitle').innerText = 'Opportunity ID: ' + (OPP || '-');
    const cat = data.order_category || '-';
    document.getElementById('val-order-category-text').innerText = cat;

    // Build the grouped accordion by business topic (PO, Customer Quote, ...).
    // All checks (required info + document checks + BSP + circuit) are pooled
    // and then grouped by topic.
    const pooled = criteria.concat(checks, baseChecks, isCircuit ? circuitChecks : []);
    const groups = groupByTopic(pooled);

    document.getElementById('val-groups').innerHTML =
      groups.map(g => groupRow(g)).join('') ||
      '<div class="p-4 text-sm text-secondary">No validation data. Run the order process first.</div>';

    renderFeedbacks();   // render the separate raised-requests list

    let banner;
    if (data.status === 'error' || !RESULT) {
      banner = `
      <div class="bg-error-container border border-error rounded-lg p-3 flex items-center gap-3 shrink-0">
        <span class="material-symbols-outlined text-error">error</span>
        <div>
          <h3 class="font-bold text-sm text-on-error-container">Validation data unavailable</h3>
          <p class="text-sm mt-0.5 text-on-surface-variant">${esc((data && data.message) || 'No validation result. Run the order process first.')}</p>
        </div>
      </div>`;
    } else if (failed.length > 0) {
      banner = `
      <div class="bg-error-container border border-error rounded-lg p-3 flex flex-col sm:flex-row items-start sm:items-center gap-3 justify-between shrink-0">
        <div class="flex items-center gap-3 text-on-error-container">
          <span class="material-symbols-outlined text-error">error</span>
          <div>
            <h3 class="font-bold text-sm">Mandatory Fields Missing</h3>
            <p class="text-sm mt-0.5 text-on-surface-variant">${failed.length} critical item${failed.length !== 1 ? 's' : ''} require resolution before proceeding.</p>
          </div>
        </div>
        <button onclick="openEmailDraft()"
           class="flex items-center gap-1 px-3 py-1.5 bg-primary text-white text-[12px] rounded hover:bg-red-700 transition-colors uppercase tracking-wider shrink-0 whitespace-nowrap"
           style="font-family:'JetBrains Mono',monospace;">
          <span class="material-symbols-outlined text-[16px] mr-0.5">mail</span> Draft Email
        </button>
      </div>`;
    } else {
      banner = `
      <div class="bg-[#e5ffe0] border border-tertiary rounded-lg p-3 flex items-center gap-3 shrink-0">
        <span class="material-symbols-outlined text-tertiary">check_circle</span>
        <div>
          <h3 class="font-bold text-sm text-on-background">All checks passed</h3>
          <p class="text-sm mt-0.5 text-on-surface-variant">This order meets the acceptance criteria and is ready for order creation.</p>
        </div>
      </div>`;
    }
    document.getElementById('val-banner').innerHTML = banner;

    const guidanceEl = document.getElementById('val-guidance');
    if (guidanceEl) {
      if (failed.length > 0) {
        guidanceEl.innerHTML = failed.slice(0, 6).map(f => `<strong>${esc(f.label)}</strong> (${esc(f.notes || 'missing')})`).join('; ') + '.';
      } else {
        guidanceEl.innerText = 'All acceptance criteria are satisfied.';
      }
    }
  }

  // ---------- Results ----------
  function renderResults() {
    const data = RESULT || {};
    const order = data.order || {};
    const lines = order.line_items || [];
    const g = (li, k) => { const v = li[k]; return (v === null || v === undefined || v === '') ? 'Not Specified' : String(v); };
    const review = lines.filter(li => ['', 'Not Specified'].includes(String(li.fulfilment || ''))).length;

    document.getElementById('results-opp-subtitle').innerText = 'Opportunity ID: ' + (OPP || 'None');
    const _ot = document.getElementById('results-order-title'); if (_ot) _ot.innerText = order.order_title || '';
    document.getElementById('stat-total').innerText = lines.length;
    document.getElementById('stat-verified').innerText = lines.length - review;
    document.getElementById('stat-review').innerText = review;
    document.getElementById('stat-category').innerText = order.order_category || '-';
    document.getElementById('results-count-label').innerText = 'Showing 1-' + lines.length + ' of ' + lines.length + ' lines';

    document.getElementById('results-tbody').innerHTML = lines.map((li, i) => {
      const mat = g(li, 'fulfilment');
      const missing = mat === 'Not Specified';
      const matCell = missing ? `
        <td class="px-md py-2 bg-error-container/40 border-r border-outline/10 relative">
          <div class="flex items-center justify-between text-primary">
            <span class="font-label-sm text-[11px] font-bold">ERR_404</span>
            <span class="material-symbols-outlined text-primary text-[16px]">warning</span>
          </div></td>` : `
        <td class="px-md py-2 font-label-sm text-[11px] border-r border-outline/10 font-mono">${esc(mat)}</td>`;
      const badge = missing ? `
        <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-error-container text-primary rounded-full text-[10px] uppercase font-bold">
          <span class="material-symbols-outlined text-[14px]">priority_high</span> Review</span>` : `
        <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-tertiary/10 text-tertiary rounded-full text-[10px] uppercase font-bold">
          <span class="material-symbols-outlined text-[14px]" style="font-variation-settings:'FILL' 1;">check_circle</span> Verified</span>`;
      const charge = g(li, 'charge_type');
      const period = g(li, 'recurring_period');
      const chargeDisp = charge + ((charge.toLowerCase().startsWith('recur') && !['Not Applicable','Not Specified'].includes(period)) ? ' / ' + period : '');
      return `
      <tr class="hover:bg-gray-50 transition-colors group">
        <td class="px-md py-2 font-label-sm text-[11px] text-secondary border-r border-outline/10">${String(i+1).padStart(3,'0')}</td>
        <td class="px-md py-2 font-label-sm text-[11px] border-r border-outline/10 font-mono">${esc(g(li,'sku'))}</td>
        <td class="px-md py-2 border-r border-outline/10">${esc(g(li,'location'))}</td>
        <td class="px-md py-2 font-semibold border-r border-outline/10">${esc(g(li,'item'))}</td>
        ${matCell}
        <td class="px-md py-2 border-r border-outline/10 font-mono">${esc(g(li,'quantity'))}</td>
        <td class="px-md py-2 border-r border-outline/10 font-mono">${esc(g(li,'price'))}</td>
        <td class="px-md py-2 border-r border-outline/10">${esc(chargeDisp)}</td>
        <td class="px-md py-2">${badge}</td>
      </tr>`;
    }).join('') || '<tr><td colspan="9" class="px-md py-6 text-center text-secondary text-sm">No order lines extracted. Run the order process first.</td></tr>';
  }

  function exportExcel() {
    const lines = ((RESULT || {}).order || {}).line_items || [];
    const rows = lines.map((li, i) => ({
      "Line": i+1, "SKU": li.sku || '', "Item": li.item || '', "Location": li.location || '',
      "Quantity": li.quantity || '', "Price": li.price || '', "Charge Type": li.charge_type || '',
      "Period": li.recurring_period || '', "Fulfilment": li.fulfilment || ''
    }));
    const ws = XLSX.utils.json_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Order Lines");
    XLSX.writeFile(wb, "Q2O_" + (OPP || 'export') + "_order_lines.xlsx");
  }

  showSection('ingestion');
</script>
"""

# Header with JS-based New Order button (no parent navigation)
HEADER = """
<header class="bg-sidebar-dark text-white flex items-center justify-between px-6 py-3 border-b-2 border-primary shrink-0 z-50">
  <div class="flex items-center space-x-3">
    <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
      <span class="material-symbols-outlined text-white text-[18px]">receipt_long</span>
    </div>
    <div class="flex flex-col">
      <span class="font-bold text-sm leading-tight text-white">Quote to Order Drafting Agent</span>
    </div>
  </div>
</header>
"""

doc_body = (
    HEADER
    + page_order_entry.view()
    + page_processing.view()
    + page_validation.view()
    + page_results.view()
    + CONTROLLER_JS.replace("__API__", json.dumps(API_URL))
)

components.html(page(doc_body), height=900, scrolling=False)