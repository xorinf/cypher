/**
 * Cypher Frontend - v2 (Box Full PFP Design)
 */

const API_BASE_URL = 'http://localhost:5001/api';
let currentResults = null;
let chartInstance = null;

// DOM Elements
const searchContainer = document.getElementById('searchContainer');
const form = document.getElementById('resultsForm');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const dashboard = document.getElementById('resultsDashboard');
const batchPanel = document.getElementById('batchPanel');

// Show/hide the batch panel when search bar transitions up
function revealBatchPanel() {
    if (batchPanel.style.display === 'none') {
        batchPanel.style.display = 'block';
        loadFavorites();
    }
}

// Event Listener
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const hallTicket = document.getElementById('hallTicket').value.trim().toUpperCase();

    if (!hallTicket || hallTicket.length < 6) {
        showError('Invalid Hall Ticket');
        return;
    }

    // UI Transition: Move Search Bar Up
    searchContainer.classList.remove('centered');
    errorState.style.display = 'none';
    dashboard.style.display = 'none';
    loadingState.style.display = 'block';
    revealBatchPanel();

    try {
        await fetchResults({ hallTicket });
    } catch (err) {
        showError(err.message);
    } finally {
        loadingState.style.display = 'none';
    }
});

function showError(msg) {
    errorState.textContent = msg;
    errorState.style.display = 'block';
}

async function fetchResults(formData) {
    const response = await fetch(`${API_BASE_URL}/fetch-results`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });

    if (!response.ok) throw new Error('Result not found or server error');
    const data = await response.json();

    currentResults = data;
    renderDashboard(data);
}

function renderDashboard(data) {
    dashboard.style.display = 'block';

    const student = data.studentInfo || {};
    const analytics = data.analytics || {};
    const semesters = data.semesterInfo?.semesters || [];

    // 1. Hero Profile (Box Full PFP)
    const isFav = favoritesSet.has((student.hallTicket || '').toUpperCase());
    document.getElementById('heroProfile').innerHTML = `
        <div class="pfp-box">
            <img src="${student.photo || 'https://via.placeholder.com/200'}" onerror="this.src='https://via.placeholder.com/200/333/fff?text=No+Photo'">
        </div>
        <div class="hero-info">
            <h2>${student.name || 'N/A'}</h2>
            <div class="subtitle">${student.program || 'Program N/A'}</div>
            
            <div class="info-chips">
                <div class="chip chip-id">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    ${student.batch || 'Batch N/A'}
                </div>
                <div class="chip">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                    ${student.hallTicket}
                </div>
                <button class="fav-star-btn ${isFav ? 'fav-active' : ''}" onclick="toggleFavorite('${student.hallTicket}', '${student.name || ''}')" title="${isFav ? 'Remove from favorites' : 'Save to favorites'}">
                    ⭐ ${isFav ? 'Saved' : 'Save'}
                </button>
            </div>
        </div>
    `;

    // 2. Stats Grid
    const marks = data.analytics?.rawSummary?.marks || {};
    const percentage = data.analytics?.overallPercentage || 0;

    document.getElementById('statsGrid').innerHTML = `
        <div class="stat-item">
            <h4>CGPA</h4>
            <div class="val" style="color: ${getGPAColor(analytics.gpa)}">${analytics.gpa || '-'}</div>
        </div>
        <div class="stat-item">
            <h4>Backlogs</h4>
            <div class="val" style="color: ${analytics.passFailStatus?.failed > 0 ? '#fb923c' : '#10b981'}">
                ${analytics.passFailStatus?.failed || 0}
            </div>
        </div>
        <div class="stat-item">
            <h4>Total Marks</h4>
            <div class="val" style="font-size: 1.1rem; line-height: 1.4;">
                ${marks.obtained > 0 ? `${marks.obtained} / ${marks.total}` : '<span style="color:var(--text-secondary); font-size: 1rem">Not Available</span>'}<br>
                ${marks.obtained > 0 ? `<span style="font-size: 0.85rem; color: #a5b4fc;">${percentage}%</span>` : ''}
            </div>
        </div>
        <div class="stat-item">
            <h4>Status</h4>
            <div class="val" style="font-size: 1.1rem; line-height: 2rem; color: ${analytics.passFailStatus?.overallStatus === 'All Clear' ? '#10b981' : '#fb923c'}">
               ${analytics.passFailStatus?.overallStatus === 'All Clear' ? 'All Clear' : 'Active Backlogs'}
            </div>
        </div>
    `;

    // 3. Semester Summary
    renderSemesterSummary(analytics.trends);

    // 4. Semesters List
    const container = document.getElementById('semestersContainer');
    container.innerHTML = semesters.map(sem => `
        <div class="sem-block" style="margin-bottom: 1rem;">
            <div class="sem-header" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
                <div class="sem-title">Semester ${sem.semester}</div>
                <div class="sem-meta">
                    <span class="sem-sgpa">SGPA ${sem.sgpa || 'N/A'}</span>
                </div>
            </div>
            <div class="sem-body" style="display: ${sem.semester === semesters[semesters.length - 1].semester ? 'block' : 'none'}">
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Subject</th>
                            <th>Type</th>
                            <th>Month/Year</th>
                            <th>Max Marks (I/E)</th>
                            <th>Grade</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${sem.subjects.map(sub => `
                            <tr>
                                <td>
                                    <div style="font-weight: 600; color: #fff;">${sub.name}</div>
                                    <div style="font-size: 0.8rem; color: #64748b;">${sub.code}</div>
                                </td>
                                <td>${sub.type === 1 ? 'Theory' : 'Lab'}</td>
                                <td style="color: #94a3b8;">${sub.examMonth || '-'}</td>
                                <td style="color: #94a3b8;">
                                    ${sub.maxMarks?.internal || 0} / ${sub.maxMarks?.external || 0}
                                </td>
                                <td>
                                    <span class="grade-dot grade-${sub.grade?.[0]}"></span>
                                    <span style="font-weight: 700; color: ${getGradeColor(sub.grade)}">${sub.grade}</span>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `).join('');
}

function getGPAColor(gpa) {
    if (!gpa) return '#fff';
    return gpa >= 8 ? '#34d399' : (gpa >= 6 ? '#fbbf24' : '#fb923c');
}

function getGradeColor(grade) {
    if (!grade) return '#fff';
    if (grade.startsWith('F') || grade === 'Ab' || grade === 'M') return '#fb923c';
    if (grade === 'O' || grade.startsWith('A')) return '#34d399';
    return '#f8fafc';
}

function renderSemesterSummary(trends) {
    const grid = document.getElementById('semesterSummaryGrid');
    if (!grid) return;
    if (!trends || !trends.data.length) {
        grid.innerHTML = '<div style="grid-column: 1/-1; color: var(--text-secondary); text-align: center;">No trend data available</div>';
        return;
    }

    grid.innerHTML = trends.labels.map((label, idx) => `
        <div class="sem-summary-item">
            <div class="lbl">${label.replace('Sem ', 'S')}</div>
            <div class="val" style="color: ${getGPAColor(trends.data[idx])}">${trends.data[idx]}</div>
        </div>
    `).join('');
}

// ============================================================
// Batch Fetch
// ============================================================

function switchBatchTab(tab, btn) {
    document.querySelectorAll('.batch-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('batchTab').style.display = tab === 'batch' ? 'block' : 'none';
    document.getElementById('favoritesTab').style.display = tab === 'favorites' ? 'block' : 'none';
    if (tab === 'favorites') loadFavorites();
}

function loadCSVFile(input) {
    const file = input.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        const lines = e.target.result.split(/[\r\n,]+/).map(l => l.trim()).filter(Boolean);
        // Skip header-like lines
        const cleaned = lines.filter(l => !/^(hall.?ticket|roll.?no|roll.?number|id)/i.test(l));
        document.getElementById('batchInput').value = cleaned.join('\n');
    };
    reader.readAsText(file);
}

async function startBatchFetch() {
    const raw = document.getElementById('batchInput').value;
    const rollNumbers = raw.split(/[\r\n,]+/).map(r => r.trim().toUpperCase()).filter(r => r.length >= 5);

    if (rollNumbers.length === 0) {
        alert('Please enter at least one valid roll number (min 5 characters).');
        return;
    }
    if (rollNumbers.length > 50) {
        alert('Maximum 50 roll numbers per batch.');
        return;
    }

    document.getElementById('batchLoading').style.display = 'flex';
    document.getElementById('batchProgress').textContent = `Fetching ${rollNumbers.length} result(s)…`;
    document.getElementById('batchResults').style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/batch-fetch`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rollNumbers })
        });
        const data = await response.json();
        renderBatchResults(data);
    } catch (err) {
        alert('Batch fetch failed: ' + err.message);
    } finally {
        document.getElementById('batchLoading').style.display = 'none';
    }
}

function renderBatchResults(data) {
    const panel = document.getElementById('batchResults');
    const tbody = document.getElementById('batchTableBody');
    const badge = document.getElementById('batchSummaryBadge');
    const errorsEl = document.getElementById('batchErrors');

    const { results = [], errors = [], topPerformer, summary = {} } = data;

    badge.textContent = `${summary.succeeded} fetched · ${summary.failed} failed`;

    // Sort by CGPA descending
    const sorted = [...results].sort((a, b) =>
        (b.analytics?.gpa || 0) - (a.analytics?.gpa || 0)
    );

    tbody.innerHTML = sorted.map(r => {
        const s = r.studentInfo || {};
        const a = r.analytics || {};
        const isTop = s.hallTicket && s.hallTicket === topPerformer;
        const isFav = favoritesSet.has((s.hallTicket || '').toUpperCase());
        return `
            <tr class="${isTop ? 'batch-row-top' : ''}">
                <td>
                    ${isTop ? '<span class="top-badge">🏆 Top</span>' : ''}
                    ${s.hallTicket || '-'}
                </td>
                <td>${s.name || '-'}</td>
                <td style="color: var(--text-secondary); font-size: 0.9rem;">${s.program || '-'}</td>
                <td style="font-weight: 700; color: ${getGPAColor(a.gpa)}">${a.gpa || '-'}</td>
                <td style="color: ${(a.passFailStatus?.failed || 0) > 0 ? '#fb923c' : '#10b981'}">${a.passFailStatus?.failed || 0}</td>
                <td style="color: ${a.passFailStatus?.overallStatus === 'All Clear' ? '#10b981' : '#fb923c'}">${a.passFailStatus?.overallStatus || '-'}</td>
                <td class="batch-row-actions">
                    <button class="action-btn" onclick="viewBatchStudent('${s.hallTicket}', ${sorted.indexOf(r)})" title="View full results">👁</button>
                    <button class="action-btn fav-toggle-btn ${isFav ? 'fav-active' : ''}" onclick="toggleFavoriteFromBatch('${s.hallTicket}', '${s.name || ''}', this)" title="${isFav ? 'Remove favorite' : 'Save favorite'}">⭐</button>
                </td>
            </tr>
        `;
    }).join('');

    if (errors.length) {
        errorsEl.style.display = 'block';
        errorsEl.innerHTML = `<strong>Failed (${errors.length}):</strong> ` +
            errors.map(e => `${e.hallTicket}: ${e.error}`).join(' · ');
    } else {
        errorsEl.style.display = 'none';
    }

    // Store batch results for quick view
    window._batchResults = sorted;
    panel.style.display = 'block';
    panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function viewBatchStudent(hallTicket, index) {
    const data = window._batchResults?.[index];
    if (!data) return;
    currentResults = data;
    renderDashboard(data);
    dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ============================================================
// Favorites
// ============================================================

let favoritesSet = new Set(); // cache of saved hall tickets (uppercase)

async function loadFavorites() {
    try {
        const res = await fetch(`${API_BASE_URL}/favorites`);
        const data = await res.json();
        const favorites = data.favorites || [];
        favoritesSet = new Set(favorites.map(f => f.hallTicket.toUpperCase()));
        renderFavoritesList(favorites);
    } catch (_) {
        // Silently fail if backend not reachable
    }
}

function renderFavoritesList(favorites) {
    const container = document.getElementById('favoritesList');
    if (!favorites.length) {
        container.innerHTML = '<div class="fav-empty">No favorites saved yet. Star a student\'s result to save them here.</div>';
        return;
    }
    container.innerHTML = favorites.map(f => `
        <div class="fav-item" id="fav-${f.hallTicket}">
            <div class="fav-info">
                <span class="fav-ht">${f.hallTicket}</span>
                <span class="fav-label">${f.label !== f.hallTicket ? f.label : ''}</span>
            </div>
            <div class="fav-actions">
                <button class="action-btn" onclick="quickFetch('${f.hallTicket}')" title="Fetch results">👁</button>
                <button class="action-btn" onclick="removeFav('${f.hallTicket}')" title="Remove">✕</button>
            </div>
        </div>
    `).join('');
}

async function toggleFavorite(hallTicket, name) {
    if (!hallTicket) return;
    const ht = hallTicket.toUpperCase();
    if (favoritesSet.has(ht)) {
        await removeFav(ht);
    } else {
        await addFav(ht, name);
    }
    // Re-render profile star button
    if (currentResults) renderDashboard(currentResults);
}

async function toggleFavoriteFromBatch(hallTicket, name, btn) {
    const ht = hallTicket.toUpperCase();
    if (favoritesSet.has(ht)) {
        await removeFav(ht);
        btn.classList.remove('fav-active');
    } else {
        await addFav(ht, name);
        btn.classList.add('fav-active');
    }
}

async function addFav(hallTicket, label) {
    try {
        await fetch(`${API_BASE_URL}/favorites`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ hallTicket, label })
        });
        favoritesSet.add(hallTicket.toUpperCase());
        await loadFavorites();
    } catch (err) {
        alert('Could not save favorite: ' + err.message);
    }
}

async function removeFav(hallTicket) {
    try {
        await fetch(`${API_BASE_URL}/favorites/${encodeURIComponent(hallTicket)}`, { method: 'DELETE' });
        favoritesSet.delete(hallTicket.toUpperCase());
        await loadFavorites();
    } catch (err) {
        alert('Could not remove favorite: ' + err.message);
    }
}

async function quickFetch(hallTicket) {
    document.getElementById('hallTicket').value = hallTicket;
    searchContainer.classList.remove('centered');
    errorState.style.display = 'none';
    dashboard.style.display = 'none';
    loadingState.style.display = 'block';
    try {
        await fetchResults({ hallTicket });
    } catch (err) {
        showError(err.message);
    } finally {
        loadingState.style.display = 'none';
    }
    dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function fetchAllFavorites() {
    const favorites = [...favoritesSet];
    if (!favorites.length) {
        alert('No favorites saved yet.');
        return;
    }
    document.getElementById('batchInput').value = favorites.join('\n');
    switchBatchTab('batch', document.querySelectorAll('.batch-tab')[0]);
    await startBatchFetch();
}

