/**
 * Cypher Frontend Application
 * Handles form submission, API communication, and results display
 */

const API_BASE_URL = 'http://localhost:5000/api';

let currentResults = null;

// Form elements
const form = document.getElementById('resultsForm');
const submitBtn = document.getElementById('submitBtn');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const resultsContainer = document.getElementById('resultsContainer');

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        hallTicket: document.getElementById('hallTicket').value.trim(),
        examType: document.getElementById('examType').value,
        viewType: document.getElementById('viewType').value
    };
    
    if (!formData.hallTicket) {
        showError('Please enter your hall ticket number');
        return;
    }
    
    await fetchResults(formData);
});

/**
 * Fetch results from the backend API
 */
async function fetchResults(formData) {
    try {
        // Show loading state
        showLoading();
        
        const response = await fetch(`${API_BASE_URL}/fetch-results`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to fetch results');
        }
        
        const data = await response.json();
        currentResults = data;
        
        // Hide loading and show results
        hideLoading();
        displayResults(data);
        
    } catch (error) {
        hideLoading();
        showError(error.message);
        console.error('Error fetching results:', error);
    }
}

/**
 * Display results in the UI
 */
function displayResults(data) {
    const { studentInfo, subjects, analytics, semesterInfo } = data;
    
    // Hide form card and show results
    form.style.display = 'none';
    resultsContainer.style.display = 'block';
    
    // Build results HTML
    resultsContainer.innerHTML = `
        <!-- Student Information Card -->
        <div class="results-card">
            <div class="results-header">
                <h3>Student Information</h3>
            </div>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Hall Ticket</span>
                    <span class="info-value">${studentInfo.hallTicket || 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Name</span>
                    <span class="info-value">${studentInfo.name || 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Program</span>
                    <span class="info-value">${studentInfo.program || 'N/A'}</span>
                </div>
            </div>
        </div>
        
        <!-- Performance Summary Card -->
        <div class="results-card">
            <div class="results-header">
                <h3>Performance Summary</h3>
            </div>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">GPA</span>
                    <span class="info-value" style="color: ${getGPAColor(analytics.gpa)}">${analytics.gpa || 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Performance Level</span>
                    <span class="info-value">${analytics.performanceLevel || 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Overall Status</span>
                    <span class="info-value" style="color: ${analytics.passFailStatus?.overallStatus === 'Pass' ? 'var(--success-color)' : 'var(--error-color)'}">
                        ${analytics.passFailStatus?.overallStatus || 'N/A'}
                    </span>
                </div>
                <div class="info-item">
                    <span class="info-label">Subjects Passed</span>
                    <span class="info-value">${analytics.passFailStatus?.passed || 0} / ${analytics.totalSubjects || 0}</span>
                </div>
            </div>
            
            ${analytics.passFailStatus?.failedSubjects?.length > 0 ? `
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(239, 68, 68, 0.1); border-left: 4px solid var(--error-color); border-radius: 8px;">
                    <h4 style="color: var(--error-color); margin-bottom: 0.5rem;">Failed Subjects</h4>
                    <ul style="list-style: none; padding: 0;">
                        ${analytics.passFailStatus.failedSubjects.map(subject => `
                            <li style="color: var(--text-secondary); margin: 0.25rem 0;">
                                ${subject.name} (${subject.code}) - Grade: ${subject.grade}
                            </li>
                        `).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
        
        <!-- Subjects Table Card -->
        ${subjects && subjects.length > 0 ? `
            <div class="results-card">
                <div class="results-header">
                    <h3>Subject-wise Results</h3>
                </div>
                <div style="overflow-x: auto;">
                    <table class="subjects-table">
                        <thead>
                            <tr>
                                <th>Subject Code</th>
                                <th>Subject Name</th>
                                <th>Credits</th>
                                <th>Grade</th>
                                <th>Marks</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${subjects.map(subject => `
                                <tr>
                                    <td>${subject.code || 'N/A'}</td>
                                    <td>${subject.name || 'N/A'}</td>
                                    <td>${subject.credits || 'N/A'}</td>
                                    <td><span class="grade-badge grade-${subject.grade ? subject.grade[0] : 'N'}">${subject.grade || 'N/A'}</span></td>
                                    <td>${subject.marks || 'N/A'}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        ` : ''}
        
        <!-- Export Options -->
        <div class="results-card">
            <div class="results-header">
                <h3>Export Results</h3>
            </div>
            <div class="export-buttons">
                <button class="btn-export" onclick="exportResults('csv')">
                    <span>📊 Export as CSV</span>
                </button>
                <button class="btn-export" onclick="exportResults('excel')">
                    <span>📈 Export as Excel</span>
                </button>
            </div>
        </div>
        
        <!-- Back Button -->
        <button class="btn-retry" onclick="resetForm()" style="width: 100%; margin-top: 1rem; background: var(--bg-card); border-color: var(--primary-color); color: var(--primary-color);">
            ← Fetch Another Result
        </button>
    `;
}

/**
 * Export results to CSV or Excel
 */
async function exportResults(format) {
    if (!currentResults) {
        showError('No results available to export');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                data: currentResults,
                format: format
            })
        });
        
        if (!response.ok) {
            throw new Error('Export failed');
        }
        
        // Download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `results_${Date.now()}.${format === 'excel' ? 'xlsx' : 'csv'}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
    } catch (error) {
        showError('Failed to export results. Please try again.');
        console.error('Export error:', error);
    }
}

/**
 * Utility function to get GPA color
 */
function getGPAColor(gpa) {
    if (!gpa) return 'var(--text-primary)';
    if (gpa >= 8.0) return 'var(--success-color)';
    if (gpa >= 6.0) return 'var(--warning-color)';
    return 'var(--error-color)';
}

/**
 * Show loading state
 */
function showLoading() {
    form.style.display = 'none';
    errorState.style.display = 'none';
    loadingState.style.display = 'block';
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingState.style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    form.style.display = 'none';
    loadingState.style.display = 'none';
    resultsContainer.style.display = 'none';
    errorMessage.textContent = message;
    errorState.style.display = 'block';
}

/**
 * Reset form to initial state
 */
function resetForm() {
    form.style.display = 'flex';
    errorState.style.display = 'none';
    resultsContainer.style.display = 'none';
    currentResults = null;
    form.reset();
}
