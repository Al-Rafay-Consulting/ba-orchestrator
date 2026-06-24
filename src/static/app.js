const storageKey = 'ba-engine-history';

const requirementInput = document.getElementById('requirement-input');
const characterCounter = document.getElementById('character-counter');
const generateButton = document.getElementById('generate-button');
const loadingPanel = document.getElementById('loading-panel');
const errorPanel = document.getElementById('error-panel');
const errorMessage = document.getElementById('error-message');
const outputPanel = document.getElementById('output-panel');
const outputMeta = document.getElementById('output-meta');
const emptyState = document.getElementById('empty-state');
const srsViewer = document.getElementById('srs-viewer');
const copySrsButton = document.getElementById('copy-srs-button');
const exportSrsButton = document.getElementById('export-srs-button');
const exportFormatSelect = document.getElementById('export-format');
const historyList = document.getElementById('history-list');
const historyTemplate = document.getElementById('history-item-template');
const newSessionButton = document.getElementById('new-session-button');

let historyEntries = loadHistory();
let activeEntryId = historyEntries[0]?.id ?? null;

function loadHistory() {
  try {
    const raw = localStorage.getItem(storageKey);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function persistHistory() {
  localStorage.setItem(storageKey, JSON.stringify(historyEntries));
}

function getActiveEntry() {
  return historyEntries.find((entry) => entry.id === activeEntryId) ?? null;
}

function setCharacterCounter() {
  characterCounter.textContent = `${requirementInput.value.length} / 5000`;
}

function setLoadingState(isLoading) {
  generateButton.disabled = isLoading;
  generateButton.textContent = isLoading ? 'Generating...' : 'Generate SRS';
  loadingPanel.classList.toggle('hidden', !isLoading);
}

function showError(message) {
  errorMessage.textContent = message;
  errorPanel.classList.remove('hidden');
}

function hideError() {
  errorPanel.classList.add('hidden');
  errorMessage.textContent = '';
}

function formatTimestamp(value) {
  return new Date(value).toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
}

function createTitleFromPrompt(prompt) {
  const trimmed = prompt.trim();
  if (!trimmed) return 'Untitled Request';
  return trimmed.length > 42 ? `${trimmed.slice(0, 42)}...` : trimmed;
}

function createPreview(prompt) {
  const trimmed = prompt.trim().replace(/\s+/g, ' ');
  return trimmed.length > 88 ? `${trimmed.slice(0, 88)}...` : trimmed;
}

function createMetaPill(label, value) {
  const span = document.createElement('span');
  span.className = 'meta-pill';
  span.textContent = `${label}: ${value}`;
  return span;
}

function setOutputActionsEnabled(isEnabled) {
  copySrsButton.disabled = !isEnabled;
  exportSrsButton.disabled = !isEnabled;
  exportFormatSelect.disabled = !isEnabled;
}

function buildSrsPlainText(entry) {
  const { srs } = entry;
  const lines = [
    'Software Requirements Specification',
    '',
    'Project Overview',
    `Project Name: ${srs.projectOverview.projectName}`,
    `Client Description: ${srs.projectOverview.clientDescription}`,
    `Clean Description: ${srs.projectOverview.cleanDescription}`,
    `Business Goal: ${srs.projectOverview.businessGoal}`,
    '',
    'Objectives',
    ...srs.objectives.map((objective, index) => `${index + 1}. ${objective}`),
    '',
    'Stakeholders',
    ...srs.stakeholders.map((stakeholder, index) => `${index + 1}. ${stakeholder.role}: ${stakeholder.description}`),
    '',
    'Functional Requirements',
    ...srs.functionalRequirements.flatMap((requirement) => [
      `${requirement.id} - ${requirement.title}`,
      `Description: ${requirement.description}`,
      `Priority: ${requirement.priority}`,
      'Acceptance Criteria:',
      ...requirement.acceptance_criteria.map((criteria) => `- ${criteria}`),
      '',
    ]),
    'Non-Functional Requirements',
    ...srs.nonFunctionalRequirements.flatMap((requirement) => [
      `${requirement.id} - ${requirement.title}`,
      `Type: ${requirement.type}`,
      `Description: ${requirement.description}`,
      '',
    ]),
    'Assumptions',
    ...srs.assumptions.map((assumption) => `- ${assumption}`),
    '',
    'Constraints',
    ...(srs.constraints ?? []).map((constraint) => `- ${constraint}`),
    '',
    'Acceptance Criteria',
    ...srs.acceptanceCriteria.map((criteria) => `- ${criteria}`),
  ];

  return lines.join('\n');
}

function buildSrsDocumentHtml(entry) {
  const { srs } = entry;
  const renderList = (items) => items.map((item) => `<li>${escapeHtml(item)}</li>`).join('');
  const renderRequirements = (requirements, includePriority) => requirements.map((requirement) => `
    <section style="margin-bottom:16px; padding:14px; border:1px solid #d8d1c3; border-radius:12px;">
      <h3 style="margin:0 0 8px; font-size:16px;">${escapeHtml(requirement.id)} - ${escapeHtml(requirement.title)}</h3>
      <p style="margin:6px 0;"><strong>Description:</strong> ${escapeHtml(requirement.description)}</p>
      ${includePriority ? `<p style="margin:6px 0;"><strong>Priority:</strong> ${escapeHtml(requirement.priority)}</p>` : `<p style="margin:6px 0;"><strong>Type:</strong> ${escapeHtml(requirement.type)}</p>`}
      ${requirement.acceptance_criteria ? `<div><strong>Acceptance Criteria:</strong><ul>${renderList(requirement.acceptance_criteria)}</ul></div>` : ''}
    </section>
  `).join('');

  return `
    <html>
      <head>
        <meta charset="UTF-8">
        <title>${escapeHtml(srs.projectOverview.projectName)} - SRS</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 28px; color: #1f1b16; }
          h1, h2 { color: #0a4f47; }
          h2 { margin-top: 28px; }
          ul, ol { line-height: 1.6; }
          dl { display: grid; grid-template-columns: 180px 1fr; gap: 8px 12px; }
          dt { font-weight: bold; }
          dd { margin: 0; }
        </style>
      </head>
      <body>
        <h1>Software Requirements Specification</h1>
        <h2>Project Overview</h2>
        <dl>
          <dt>Project Name</dt><dd>${escapeHtml(srs.projectOverview.projectName)}</dd>
          <dt>Client Description</dt><dd>${escapeHtml(srs.projectOverview.clientDescription)}</dd>
          <dt>Clean Description</dt><dd>${escapeHtml(srs.projectOverview.cleanDescription)}</dd>
          <dt>Business Goal</dt><dd>${escapeHtml(srs.projectOverview.businessGoal)}</dd>
        </dl>
        <h2>Objectives</h2>
        <ol>${renderList(srs.objectives)}</ol>
        <h2>Stakeholders</h2>
        <ol>${srs.stakeholders.map((stakeholder) => `<li><strong>${escapeHtml(stakeholder.role)}:</strong> ${escapeHtml(stakeholder.description)}</li>`).join('')}</ol>
        <h2>Functional Requirements</h2>
        ${renderRequirements(srs.functionalRequirements, true)}
        <h2>Non-Functional Requirements</h2>
        ${renderRequirements(srs.nonFunctionalRequirements, false)}
        <h2>Assumptions</h2>
        <ul>${renderList(srs.assumptions)}</ul>
        <h2>Constraints</h2>
        <ul>${renderList(srs.constraints ?? [])}</ul>
        <h2>Acceptance Criteria</h2>
        <ul>${renderList(srs.acceptanceCriteria)}</ul>
      </body>
    </html>
  `;
}

function createFileSafeName(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'srs-document';
}

function downloadBlob(blob, fileName) {
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.href = url;
  link.download = fileName;
  link.click();
  URL.revokeObjectURL(url);
}

async function copySrsToClipboard() {
  const entry = getActiveEntry();
  if (!entry) {
    showError('Generate or load an SRS before copying.');
    return;
  }

  try {
    await navigator.clipboard.writeText(buildSrsPlainText(entry));
    const previousLabel = copySrsButton.textContent;
    copySrsButton.textContent = 'Copied';
    window.setTimeout(() => {
      copySrsButton.textContent = previousLabel;
    }, 1600);
  } catch {
    showError('Clipboard access failed. Please allow clipboard permissions and try again.');
  }
}

function exportSrsDocument() {
  const entry = getActiveEntry();
  if (!entry) {
    showError('Generate or load an SRS before exporting.');
    return;
  }

  const fileBase = createFileSafeName(entry.srs.projectOverview.projectName);
  const format = exportFormatSelect.value;

  if (format === 'word') {
    const blob = new Blob([buildSrsDocumentHtml(entry)], { type: 'application/msword' });
    downloadBlob(blob, `${fileBase}-srs.doc`);
    return;
  }

  if (!window.jspdf?.jsPDF) {
    showError('PDF export is unavailable because the PDF library did not load.');
    return;
  }

  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF({ unit: 'pt', format: 'a4' });
  const margin = 40;
  const pageWidth = pdf.internal.pageSize.getWidth() - margin * 2;
  const pageHeight = pdf.internal.pageSize.getHeight();
  const lines = pdf.splitTextToSize(buildSrsPlainText(entry), pageWidth);
  let y = margin;

  pdf.setFont('helvetica', 'normal');
  pdf.setFontSize(11);

  lines.forEach((line) => {
    if (y > pageHeight - margin) {
      pdf.addPage();
      y = margin;
    }
    pdf.text(line, margin, y);
    y += 16;
  });

  pdf.save(`${fileBase}-srs.pdf`);
}

function renderProjectOverview(projectOverview) {
  const section = document.createElement('section');
  section.className = 'srs-section';
  section.innerHTML = `
    <h4>Project Overview</h4>
    <dl class="definition-grid">
      <dt>Project Name</dt><dd>${escapeHtml(projectOverview.projectName)}</dd>
      <dt>Client Description</dt><dd>${escapeHtml(projectOverview.clientDescription)}</dd>
      <dt>Clean Description</dt><dd>${escapeHtml(projectOverview.cleanDescription)}</dd>
      <dt>Business Goal</dt><dd>${escapeHtml(projectOverview.businessGoal)}</dd>
    </dl>
  `;
  return section;
}

function renderSimpleList(title, items, className = 'check-list') {
  const section = document.createElement('section');
  section.className = 'srs-section';
  const listItems = items.map((item) => `<li>${escapeHtml(item)}</li>`).join('');
  section.innerHTML = `<h4>${title}</h4><ul class="${className}">${listItems}</ul>`;
  return section;
}

function renderStakeholders(stakeholders) {
  const section = document.createElement('section');
  section.className = 'srs-section';
  const items = stakeholders
    .map(
      (stakeholder) => `
        <li>
          <strong>${escapeHtml(stakeholder.role)}</strong><br>
          <span>${escapeHtml(stakeholder.description)}</span>
        </li>
      `,
    )
    .join('');
  section.innerHTML = `<h4>Stakeholders</h4><ol class="number-list">${items}</ol>`;
  return section;
}

function renderRequirements(title, requirements, kind = 'functional') {
  const section = document.createElement('section');
  section.className = 'srs-section';
  const cards = requirements
    .map((requirement) => {
      const priorityMarkup = requirement.priority
        ? `<span class="priority-pill ${requirement.priority.toLowerCase()}">${escapeHtml(requirement.priority)}</span>`
        : `<span class="priority-pill low">${escapeHtml(requirement.type ?? kind)}</span>`;

      const acceptanceMarkup = requirement.acceptance_criteria
        ? `<ul class="check-list">${requirement.acceptance_criteria.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`
        : '';

      return `
        <article class="requirement-card">
          <div class="requirement-card-header">
            <div>
              <span class="requirement-id">${escapeHtml(requirement.id)}</span>
              <h5>${escapeHtml(requirement.title)}</h5>
            </div>
            ${priorityMarkup}
          </div>
          <p>${escapeHtml(requirement.description)}</p>
          ${acceptanceMarkup}
        </article>
      `;
    })
    .join('');

  section.innerHTML = `<h4>${title}</h4><div class="requirement-list">${cards}</div>`;
  return section;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderEntry(entry) {
  outputPanel.classList.remove('hidden');
  emptyState.classList.add('hidden');
  srsViewer.innerHTML = '';
  outputMeta.innerHTML = '';
  setOutputActionsEnabled(true);

  requirementInput.value = entry.prompt;
  setCharacterCounter();

  if (entry.metadata?.model) {
    outputMeta.appendChild(createMetaPill('Model', entry.metadata.model));
  }
  if (entry.metadata?.processing_time_ms) {
    outputMeta.appendChild(createMetaPill('Latency', `${entry.metadata.processing_time_ms} ms`));
  }
  outputMeta.appendChild(createMetaPill('Saved', formatTimestamp(entry.createdAt)));

  srsViewer.appendChild(renderProjectOverview(entry.srs.projectOverview));
  srsViewer.appendChild(renderSimpleList('Objectives', entry.srs.objectives));
  srsViewer.appendChild(renderStakeholders(entry.srs.stakeholders));
  srsViewer.appendChild(renderRequirements('Functional Requirements', entry.srs.functionalRequirements, 'functional'));
  srsViewer.appendChild(renderRequirements('Non-Functional Requirements', entry.srs.nonFunctionalRequirements, 'non-functional'));
  srsViewer.appendChild(renderSimpleList('Assumptions', entry.srs.assumptions));
  srsViewer.appendChild(renderSimpleList('Constraints', entry.srs.constraints ?? []));
  srsViewer.appendChild(renderSimpleList('Acceptance Criteria', entry.srs.acceptanceCriteria));
}

function renderHistory() {
  historyList.innerHTML = '';

  if (!historyEntries.length) {
    const empty = document.createElement('div');
    empty.className = 'history-intro';
    empty.textContent = 'No history yet. Generate your first SRS to populate this panel.';
    historyList.appendChild(empty);
    return;
  }

  historyEntries.forEach((entry) => {
    const fragment = historyTemplate.content.cloneNode(true);
    const button = fragment.querySelector('.history-item');
    fragment.querySelector('.history-item-title').textContent = entry.title;
    fragment.querySelector('.history-item-preview').textContent = entry.preview;
    fragment.querySelector('.history-item-time').textContent = formatTimestamp(entry.createdAt);

    if (entry.id === activeEntryId) {
      button.classList.add('is-active');
    }

    button.addEventListener('click', () => {
      activeEntryId = entry.id;
      hideError();
      renderHistory();
      renderEntry(entry);
    });

    historyList.appendChild(fragment);
  });
}

function resetWorkspace() {
  activeEntryId = null;
  requirementInput.value = '';
  setCharacterCounter();
  hideError();
  outputMeta.innerHTML = '';
  srsViewer.innerHTML = '';
  emptyState.classList.remove('hidden');
  outputPanel.classList.remove('hidden');
  setOutputActionsEnabled(false);
  renderHistory();
}

async function generateSrs() {
  const prompt = requirementInput.value.trim();
  hideError();

  if (!prompt) {
    showError('Please enter a client requirement before generating an SRS.');
    return;
  }

  setLoadingState(true);

  try {
    const response = await fetch('/api/generate-srs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client_request: prompt }),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || payload.error || 'SRS generation failed.');
    }

    const entry = {
      id: crypto.randomUUID(),
      title: createTitleFromPrompt(prompt),
      preview: createPreview(prompt),
      prompt,
      srs: payload.data,
      metadata: payload.metadata,
      createdAt: new Date().toISOString(),
    };

    historyEntries = [entry, ...historyEntries].slice(0, 20);
    activeEntryId = entry.id;
    persistHistory();
    renderHistory();
    renderEntry(entry);
  } catch (error) {
    showError(error.message || 'An unexpected error occurred while generating the SRS.');
  } finally {
    setLoadingState(false);
  }
}

requirementInput.addEventListener('input', setCharacterCounter);
generateButton.addEventListener('click', generateSrs);
newSessionButton.addEventListener('click', resetWorkspace);
copySrsButton.addEventListener('click', copySrsToClipboard);
exportSrsButton.addEventListener('click', exportSrsDocument);

setCharacterCounter();
renderHistory();
outputPanel.classList.remove('hidden');
setOutputActionsEnabled(historyEntries.length > 0);

if (historyEntries.length) {
  renderEntry(historyEntries[0]);
} else {
  emptyState.classList.remove('hidden');
}
