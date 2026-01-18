/**
 * Cypher Frontend Application
 * Handles form submission, API communication, and results display
 * Enhanced with comprehensive edge case handling
 */

const API_BASE_URL = 'http://localhost:5001/api';
const REQUEST_TIMEOUT_MS = 30000; // 30 second timeout

let currentResults = null;
let isSubmitting = false; // Debounce flag

// Form elements
const form = document.getElementById('resultsForm');
const submitBtn = document.getElementById('submitBtn');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const resultsContainer = document.getElementById('resultsContainer');

// Input validation patterns
const HALL_TICKET_PATTERN = /^[A-Za-z0-9]+$/;
const MIN_HALL_TICKET_LENGTH = 6;
const MAX_HALL_TICKET_LENGTH = 20;

/**
 * Validate hall ticket number
 * @param {string} hallTicket - Hall ticket number to validate
 * @returns {object} - { valid: boolean, message?: string }
 */
function validateHallTicket(hallTicket) {
    if (!hallTicket) {
        return { valid: false, message: 'Please enter your hall ticket number' };
    }

    if (hallTicket.length < MIN_HALL_TICKET_LENGTH) {
        return { valid: false, message: `Hall ticket must be at least ${MIN_HALL_TICKET_LENGTH} characters` };
    }

    if (hallTicket.length > MAX_HALL_TICKET_LENGTH) {
        return { valid: false, message: `Hall ticket cannot exceed ${MAX_HALL_TICKET_LENGTH} characters` };
    }

    if (!HALL_TICKET_PATTERN.test(hallTicket)) {
        return { valid: false, message: 'Hall ticket can only contain letters and numbers' };
    }

    return { valid: true };
}

/**
 * Safely access nested object properties
 * @param {object} obj - Object to access
 * @param {string} path - Dot-separated path (e.g., 'a.b.c')
 * @param {*} defaultValue - Default value if path doesn't exist
 * @returns {*} - Value at path or default
 */
function safeGet(obj, path, defaultValue = null) {
    try {
        const keys = path.split('.');
        let result = obj;
        for (const key of keys) {
            if (result === null || result === undefined) {
                return defaultValue;
            }
            result = result[key];
        }
        return result !== null && result !== undefined ? result : defaultValue;
    } catch {
        return defaultValue;
    }
}

/**
 * Escape HTML to prevent XSS
 * @param {string} str - String to escape
 * @returns {string} - Escaped string
 */
function escapeHtml(str) {
    if (str === null || str === undefined) return 'N/A';
    const div = document.createElement('div');
    div.textContent = String(str);
    return div.innerHTML;
}

/**
 * Fetch with timeout wrapper
 * @param {string} url - URL to fetch
 * @param {object} options - Fetch options
 * @param {number} timeout - Timeout in milliseconds
 * @returns {Promise<Response>}
 */
async function fetchWithTimeout(url, options, timeout = REQUEST_TIMEOUT_MS) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. Please check your connection and try again.');
        }
        throw error;
    }
}

/**
 * Categorize and format error messages for user display
 * @param {Error} error - Error object
 * @returns {object} - { title: string, message: string, isRetryable: boolean }
 */
function categorizeError(error) {
    const message = error.message || 'An unexpected error occurred';

    // Network errors
    if (error.name === 'TypeError' && message.includes('fetch')) {
        return {
            title: 'Connection Error',
            message: 'Unable to connect to the server. Please check if the backend is running.',
            isRetryable: true
        };
    }

    // Timeout errors
    if (message.includes('timed out')) {
        return {
            title: 'Request Timeout',
            message: 'The request took too long. Please try again.',
            isRetryable: true
        };
    }

    // Server errors
    if (message.includes('Internal server error')) {
        return {
            title: 'Server Error',
            message: 'Something went wrong on our end. Please try again later.',
            isRetryable: true
        };
    }

    // Not found errors
    if (message.includes('No results found') || message.includes('Failed to retrieve')) {
        return {
            title: 'Results Not Found',
            message: message,
            isRetryable: false
        };
    }

    // Generic error
    return {
        title: 'Error',
        message: message,
        isRetryable: true
    };
}

/**
 * Set button loading state
 * @param {boolean} loading - Whether button is in loading state
 */
function setButtonLoading(loading) {
    if (loading) {
        submitBtn.disabled = true;
        submitBtn.setAttribute('aria-busy', 'true');
        submitBtn.querySelector('.btn-text').textContent = 'Fetching...';
    } else {
        submitBtn.disabled = false;
        submitBtn.setAttribute('aria-busy', 'false');
        submitBtn.querySelector('.btn-text').textContent = 'Get Results';
    }
}

// Form submission handler with debouncing
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Prevent double submission
    if (isSubmitting) {
        return;
    }

    const hallTicketInput = document.getElementById('hallTicket');
    const formData = {
        hallTicket: hallTicketInput.value.trim().toUpperCase(),
        examType: document.getElementById('examType').value,
        viewType: document.getElementById('viewType').value
    };

    // Validate hall ticket
    const validation = validateHallTicket(formData.hallTicket);
    if (!validation.valid) {
        showError(validation.message);
        hallTicketInput.focus();
        return;
    }

    await fetchResults(formData);
});

// Real-time input validation feedback
document.getElementById('hallTicket').addEventListener('input', (e) => {
    const value = e.target.value.trim();
    const inputGroup = e.target.closest('.form-group');

    // Remove any existing validation state
    inputGroup.classList.remove('valid', 'invalid');

    if (value.length > 0) {
        const validation = validateHallTicket(value);
        inputGroup.classList.add(validation.valid ? 'valid' : 'invalid');
    }
});

/**
 * Fetch results from the backend API
 */
async function fetchResults(formData) {
    try {
        isSubmitting = true;
        setButtonLoading(true);
        showLoading();

        const response = await fetchWithTimeout(`${API_BASE_URL}/fetch-results`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch {
                errorData = { error: `Server returned status ${response.status}` };
            }
            throw new Error(errorData.error || 'Failed to fetch results');
        }

        const data = await response.json();

        // Validate response structure
        if (!data || typeof data !== 'object') {
            throw new Error('Invalid response from server');
        }

        currentResults = data;

        // Hide loading and show results
        hideLoading();
        displayResults(data);

    } catch (error) {
        hideLoading();
        const categorized = categorizeError(error);
        showError(categorized.message, categorized.title, categorized.isRetryable);
        console.error('Error fetching results:', error);
    } finally {
        isSubmitting = false;
        setButtonLoading(false);
    }
}

/**
 * Display results in the UI with null-safe access
 */
function displayResults(data) {
    const studentInfo = safeGet(data, 'studentInfo', {});
    const subjects = safeGet(data, 'subjects', []);
    const analytics = safeGet(data, 'analytics', {});

    // Hide form card and show results
    form.style.display = 'none';
    resultsContainer.style.display = 'block';
    resultsContainer.setAttribute('role', 'region');
    resultsContainer.setAttribute('aria-label', 'Results Display');

    // Get safe values
    const hallTicket = escapeHtml(safeGet(studentInfo, 'hallTicket', 'N/A'));
    const name = escapeHtml(safeGet(studentInfo, 'name', 'N/A'));
    const program = escapeHtml(safeGet(studentInfo, 'program', 'N/A'));
    const gpa = safeGet(analytics, 'gpa', null);
    const performanceLevel = escapeHtml(safeGet(analytics, 'performanceLevel', 'N/A'));
    const overallStatus = safeGet(analytics, 'passFailStatus.overallStatus', 'N/A');
    const passed = safeGet(analytics, 'passFailStatus.passed', 0);
    const totalSubjects = safeGet(analytics, 'totalSubjects', 0);
    const failedSubjects = safeGet(analytics, 'passFailStatus.failedSubjects', []);

    // Build results HTML
    resultsContainer.innerHTML = `
        <!-- Student Information Card -->
        <div class="results-card" role="article" aria-labelledby="student-info-heading">
            <div class="results-header">
                <h3 id="student-info-heading">Student Information</h3>
            </div>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Hall Ticket</span>
                    <span class="info-value">${hallTicket}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Name</span>
                    <span class="info-value">${name}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Program</span>
                    <span class="info-value">${program}</span>
                </div>
            </div>
        </div>
        
        <!-- Performance Summary Card -->
        <div class="results-card" role="article" aria-labelledby="performance-heading">
            <div class="results-header">
                <h3 id="performance-heading">Performance Summary</h3>
            </div>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">GPA</span>
                    <span class="info-value" style="color: ${getGPAColor(gpa)}">${gpa !== null ? gpa : 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Performance Level</span>
                    <span class="info-value">${performanceLevel}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Overall Status</span>
                    <span class="info-value" style="color: ${overallStatus === 'Pass' ? 'var(--success-color)' : 'var(--error-color)'}">
                        ${escapeHtml(overallStatus)}
                    </span>
                </div>
                <div class="info-item">
                    <span class="info-label">Subjects Passed</span>
                    <span class="info-value">${passed} / ${totalSubjects}</span>
                </div>
            </div>
            
            ${Array.isArray(failedSubjects) && failedSubjects.length > 0 ? `
                <div class="failed-subjects-alert" role="alert" style="margin-top: 1.5rem; padding: 1rem; background: rgba(239, 68, 68, 0.1); border-left: 4px solid var(--error-color); border-radius: 8px;">
                    <h4 style="color: var(--error-color); margin-bottom: 0.5rem;">Failed Subjects</h4>
                    <ul style="list-style: none; padding: 0;">
                        ${failedSubjects.map(subject => `
                            <li style="color: var(--text-secondary); margin: 0.25rem 0;">
                                ${escapeHtml(safeGet(subject, 'name', 'Unknown'))} (${escapeHtml(safeGet(subject, 'code', 'N/A'))}) - Grade: ${escapeHtml(safeGet(subject, 'grade', 'N/A'))}
                            </li>
                        `).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
        
        <!-- Subjects Table Card -->
        ${Array.isArray(subjects) && subjects.length > 0 ? `
            <div class="results-card" role="article" aria-labelledby="subjects-heading">
                <div class="results-header">
                    <h3 id="subjects-heading">Subject-wise Results</h3>
                </div>
                <div style="overflow-x: auto;">
                    <table class="subjects-table" role="table" aria-describedby="subjects-heading">
                        <thead>
                            <tr>
                                <th scope="col">Subject Code</th>
                                <th scope="col">Subject Name</th>
                                <th scope="col">Credits</th>
                                <th scope="col">Grade</th>
                                <th scope="col">Marks</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${subjects.map(subject => {
        const code = escapeHtml(safeGet(subject, 'code', 'N/A'));
        const subjectName = escapeHtml(safeGet(subject, 'name', 'N/A'));
        const credits = escapeHtml(safeGet(subject, 'credits', 'N/A'));
        const grade = safeGet(subject, 'grade', 'N');
        const marks = escapeHtml(safeGet(subject, 'marks', 'N/A'));
        const gradeClass = grade && grade.length > 0 ? grade[0] : 'N';

        return `
                                    <tr>
                                        <td>${code}</td>
                                        <td>${subjectName}</td>
                                        <td>${credits}</td>
                                        <td><span class="grade-badge grade-${gradeClass}">${escapeHtml(grade) || 'N/A'}</span></td>
                                        <td>${marks}</td>
                                    </tr>
                                `;
    }).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        ` : `
            <div class="results-card" role="article">
                <div class="no-subjects-message" style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                    <p>No subject details available</p>
                </div>
            </div>
        `}
        
        <!-- Export Options -->
        <div class="results-card" role="article" aria-labelledby="export-heading">
            <div class="results-header">
                <h3 id="export-heading">Export Results</h3>
            </div>
            <div class="export-buttons">
                <button class="btn-export" onclick="exportResults('csv')" aria-label="Export results as CSV file">
                    <span>📊 Export as CSV</span>
                </button>
                <button class="btn-export" onclick="exportResults('excel')" aria-label="Export results as Excel file">
                    <span>📈 Export as Excel</span>
                </button>
            </div>
        </div>
        
        <!-- Back Button -->
        <button class="btn-retry" onclick="resetForm()" style="width: 100%; margin-top: 1rem; background: var(--bg-card); border-color: var(--primary-color); color: var(--primary-color);" aria-label="Go back to fetch another result">
            ← Fetch Another Result
        </button>
    `;

    // Announce results to screen readers
    announceToScreenReader('Results loaded successfully');
}

/**
 * Announce message to screen readers
 * @param {string} message - Message to announce
 */
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    document.body.appendChild(announcement);

    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

/**
 * Export results to CSV or Excel with error handling
 */
async function exportResults(format) {
    if (!currentResults) {
        showError('No results available to export');
        return;
    }

    // Find and disable export buttons during export
    const exportButtons = document.querySelectorAll('.btn-export');
    exportButtons.forEach(btn => {
        btn.disabled = true;
        btn.style.opacity = '0.6';
    });

    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                data: currentResults,
                format: format
            })
        }, 15000); // 15 second timeout for exports

        if (!response.ok) {
            let errorMsg = 'Export failed';
            try {
                const errorData = await response.json();
                errorMsg = errorData.error || errorMsg;
            } catch {
                // Use default error message
            }
            throw new Error(errorMsg);
        }

        // Check content type
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            // Server returned an error as JSON
            const errorData = await response.json();
            throw new Error(errorData.error || 'Export failed');
        }

        // Download the file
        const blob = await response.blob();

        if (blob.size === 0) {
            throw new Error('Export file is empty');
        }

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `results_${Date.now()}.${format === 'excel' ? 'xlsx' : 'csv'}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        // Show success feedback
        announceToScreenReader(`Results exported as ${format.toUpperCase()} successfully`);

    } catch (error) {
        showError(`Failed to export results: ${error.message}`);
        console.error('Export error:', error);
    } finally {
        // Re-enable export buttons
        exportButtons.forEach(btn => {
            btn.disabled = false;
            btn.style.opacity = '1';
        });
    }
}

/**
 * Utility function to get GPA color
 */
function getGPAColor(gpa) {
    if (gpa === null || gpa === undefined) return 'var(--text-primary)';
    const numGpa = parseFloat(gpa);
    if (isNaN(numGpa)) return 'var(--text-primary)';
    if (numGpa >= 8.0) return 'var(--success-color)';
    if (numGpa >= 6.0) return 'var(--warning-color)';
    return 'var(--error-color)';
}

/**
 * Show loading state
 */
function showLoading() {
    form.style.display = 'none';
    errorState.style.display = 'none';
    resultsContainer.style.display = 'none';
    loadingState.style.display = 'block';
    loadingState.setAttribute('aria-live', 'polite');
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingState.style.display = 'none';
}

/**
 * Show error message with optional title and retry button
 */
function showError(message, title = 'Oops! Something went wrong', isRetryable = true) {
    form.style.display = 'none';
    loadingState.style.display = 'none';
    resultsContainer.style.display = 'none';

    // Update error state content
    const errorTitle = errorState.querySelector('h3');
    if (errorTitle) {
        errorTitle.textContent = title;
    }
    errorMessage.textContent = message;

    // Show/hide retry button based on error type
    const retryBtn = errorState.querySelector('.btn-retry');
    if (retryBtn) {
        retryBtn.style.display = isRetryable ? 'inline-block' : 'none';
    }

    errorState.style.display = 'block';
    errorState.setAttribute('role', 'alert');

    // Announce error to screen readers
    announceToScreenReader(`Error: ${message}`);
}

/**
 * Reset form to initial state
 */
function resetForm() {
    form.style.display = 'flex';
    errorState.style.display = 'none';
    resultsContainer.style.display = 'none';
    loadingState.style.display = 'none';
    currentResults = null;
    isSubmitting = false;
    setButtonLoading(false);
    form.reset();

    // Clear validation states
    const inputGroups = form.querySelectorAll('.form-group');
    inputGroups.forEach(group => {
        group.classList.remove('valid', 'invalid');
    });

    // Focus on hall ticket input
    document.getElementById('hallTicket').focus();
}

// Check API health on page load
async function checkApiHealth() {
    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/health`, {
            method: 'GET'
        }, 5000);

        if (!response.ok) {
            console.warn('API health check failed');
        }
    } catch (error) {
        console.warn('Unable to reach API server:', error.message);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkApiHealth();

    // Add keyboard navigation support
    document.addEventListener('keydown', (e) => {
        // Allow Escape to go back from results/error view
        if (e.key === 'Escape') {
            if (resultsContainer.style.display === 'block' || errorState.style.display === 'block') {
                resetForm();
            }
        }
    });
});
