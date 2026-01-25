/**
 * Cypher Frontend - v2 (Box Full PFP Design)
 */

const API_BASE_URL = 'https://cypher-backend-vcwi.onrender.com/api';
let currentResults = null;
let chartInstance = null;

// DOM Elements
const searchContainer = document.getElementById('searchContainer');
const form = document.getElementById('resultsForm');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const dashboard = document.getElementById('resultsDashboard');

// Health Check Configuration
const HEALTH_CHECK_CONFIG = {
    maxAttempts: 20,      // 20 attempts × 3 seconds = 60 seconds max wait
    intervalMs: 3000,     // Check every 3 seconds
    timeoutMs: 5000       // 5 second timeout per health check
};

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

    // Show health check UI instead of simple loader
    showHealthCheckUI();

    try {
        // First, ensure backend is awake
        const isHealthy = await waitForBackendHealth();

        if (!isHealthy) {
            throw new Error('Backend service is taking longer than expected. Please try again.');
        }

        // Update UI to show fetching results
        updateHealthCheckStatus('Backend ready! Fetching your results...', 100);
        await new Promise(resolve => setTimeout(resolve, 500)); // Brief pause for UX

        await fetchResults({ hallTicket });
    } catch (err) {
        showError(err.message);
    } finally {
        hideHealthCheckUI();
    }
});

function showError(msg) {
    errorState.textContent = msg;
    errorState.style.display = 'block';
}

// Backend awake state cache
let backendAwakeUntil = 0;
const AWAKE_CACHE_DURATION = 10 * 60 * 1000; // 10 minutes

// Check if backend is healthy
async function checkHealth(timeoutMs = 5000) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            signal: controller.signal,
            method: 'GET'
        });
        clearTimeout(timeout);
        return response.ok;
    } catch (error) {
        clearTimeout(timeout);
        return false;
    }
}

// Wait for backend to be healthy with progress updates
async function waitForBackendHealth() {
    // Check if we recently confirmed backend is awake
    if (Date.now() < backendAwakeUntil) {
        console.log('Backend recently verified awake, skipping health check');
        return true;
    }

    // Try a quick check first (2 second timeout)
    const quickCheck = await checkHealth(2000);
    if (quickCheck) {
        console.log('Backend is awake (quick check passed)');
        backendAwakeUntil = Date.now() + AWAKE_CACHE_DURATION;
        return true;
    }

    // Backend is cold starting, show progress UI and poll
    console.log('Backend appears to be cold starting, initiating polling...');

    for (let attempt = 1; attempt <= HEALTH_CHECK_CONFIG.maxAttempts; attempt++) {
        const progress = (attempt / HEALTH_CHECK_CONFIG.maxAttempts) * 90; // Max 90% during polling

        updateHealthCheckStatus(
            `Waking up backend service... (${attempt}/${HEALTH_CHECK_CONFIG.maxAttempts})`,
            progress
        );

        const isHealthy = await checkHealth(HEALTH_CHECK_CONFIG.timeoutMs);

        if (isHealthy) {
            console.log(`Backend healthy after ${attempt} attempts`);
            backendAwakeUntil = Date.now() + AWAKE_CACHE_DURATION;
            return true;
        }

        // Wait before next attempt (except on last attempt)
        if (attempt < HEALTH_CHECK_CONFIG.maxAttempts) {
            await new Promise(resolve => setTimeout(resolve, HEALTH_CHECK_CONFIG.intervalMs));
        }
    }

    return false;
}

// Health Check UI Functions
function showHealthCheckUI() {
    // Create centered overlay
    const overlay = document.createElement('div');
    overlay.id = 'healthCheckOverlay';
    overlay.className = 'health-check-overlay';
    overlay.innerHTML = `
        <div class="health-check-container">
            <div class="spinner"></div>
            <div class="health-status">Checking backend status...</div>
            <div class="progress-bar-container">
                <div class="progress-bar" id="healthProgressBar"></div>
            </div>
            <div class="health-info">This may take up to 60 seconds on first request</div>
        </div>
    `;
    document.body.appendChild(overlay);
}

function updateHealthCheckStatus(message, progress) {
    const statusEl = document.querySelector('.health-status');
    const progressBar = document.getElementById('healthProgressBar');

    if (statusEl) statusEl.textContent = message;
    if (progressBar) progressBar.style.width = `${progress}%`;
}

function hideHealthCheckUI() {
    const overlay = document.getElementById('healthCheckOverlay');
    if (overlay) {
        overlay.remove();
    }
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
