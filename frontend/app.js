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
