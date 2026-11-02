// ==========================================
// USER DASHBOARD DYNAMIC DROPDOWN & AJAX
// ==========================================

// Handle Department to Doctor filtering
const deptSelect = document.getElementById('department');
const docSelect = document.getElementById('doctor');

if (deptSelect && docSelect) {
    deptSelect.addEventListener('change', function() {
        const selectedDept = this.value;
        
        // Reset doctor dropdown
        docSelect.innerHTML = '<option value="" disabled selected>Choose Doctor...</option>';
        docSelect.disabled = true;

        if (selectedDept && doctorMapping && doctorMapping[selectedDept]) {
            const doctors = doctorMapping[selectedDept];
            doctors.forEach(function(doc) {
                const opt = document.createElement('option');
                opt.value = doc;
                opt.textContent = doc;
                docSelect.appendChild(opt);
            });
            docSelect.disabled = false;
        }
    });
}

// AJAX Feedback Submission
const feedbackForm = document.getElementById('feedback-form');
if (feedbackForm) {
    feedbackForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const feedbackText = document.getElementById('feedback').value.trim();
        if (feedbackText.length < 10) {
            alert('Feedback must be at least 10 characters long.');
            return;
        }

        // UI Transition to Loading State
        document.getElementById('result-placeholder').classList.add('d-none');
        document.getElementById('result-success').classList.add('d-none');
        document.getElementById('result-loading').classList.remove('d-none');
        
        // Disable submit button
        const submitBtn = document.getElementById('btn-submit-feedback');
        submitBtn.disabled = true;

        // Collect Form Data
        const formData = new FormData(feedbackForm);

        // Fetch API Post
        fetch(feedbackForm.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Server error'); });
            }
            return response.json();
        })
        .then(data => {
            // Update prediction card details
            const emojiBox = document.getElementById('result-emoji');
            const labelText = document.getElementById('result-label');
            const confText = document.getElementById('result-confidence');
            const progressFill = document.getElementById('result-progress-fill');

            emojiBox.textContent = data.emoji;
            labelText.textContent = data.prediction;
            confText.textContent = data.confidence + '%';
            progressFill.style.width = data.confidence + '%';

            // Add sentiment-specific colors
            const resultSuccessCard = document.getElementById('result-success');
            resultSuccessCard.className = 'card result-card success-state'; // reset
            
            if (data.prediction.toLowerCase() === 'positive') {
                resultSuccessCard.classList.add('border-success-accent');
                labelText.className = 'sentiment-label text-success';
                progressFill.className = 'confidence-progress-fill bg-success';
                emojiBox.className = 'sentiment-emoji-box bounce-animation';
            } else {
                resultSuccessCard.classList.add('border-danger-accent');
                labelText.className = 'sentiment-label text-danger';
                progressFill.className = 'confidence-progress-fill bg-danger';
                emojiBox.className = 'sentiment-emoji-box shake-animation';
            }

            // Hide Loading State & Show Success State
            document.getElementById('result-loading').classList.add('d-none');
            document.getElementById('result-success').classList.remove('d-none');
        })
        .catch(err => {
            alert('Error: ' + err.message);
            // Revert back to placeholder state on error
            document.getElementById('result-loading').classList.add('d-none');
            document.getElementById('result-placeholder').classList.remove('d-none');
        })
        .finally(() => {
            submitBtn.disabled = false;
        });
    });
}

// Reset Form Button
const resetBtn = document.getElementById('btn-reset-form');
if (resetBtn) {
    resetBtn.addEventListener('click', function() {
        feedbackForm.reset();
        
        // Reset doctor dropdown
        docSelect.innerHTML = '<option value="" disabled selected>Select Department First...</option>';
        docSelect.disabled = true;

        // Toggle prediction UI panel back to placeholder
        document.getElementById('result-success').classList.add('d-none');
        document.getElementById('result-placeholder').classList.remove('d-none');
    });
}


// ==========================================
// ADMIN DASHBOARD TAB SWITCHING & ANALYTICS
// ==========================================

// Global variables for Admin charts
let pieChartInstance = null;
let lineChartInstance = null;
let hospitalChartInstance = null;
let doctorChartInstance = null;

// Tab Switching logic
function switchAdminTab(tabName, element) {
    // Hide all tab contents
    const tabs = document.querySelectorAll('.admin-tab-content');
    tabs.forEach(tab => tab.classList.add('d-none'));

    // Show selected tab content
    document.getElementById('tab-' + tabName).classList.remove('d-none');

    // Remove active class from all nav items
    const navItems = document.querySelectorAll('.sidebar-nav li');
    navItems.forEach(item => item.classList.remove('active'));

    // Add active class to clicked nav item
    if (element) {
        element.classList.add('active');
    } else {
        // Fallback search
        const listItems = document.querySelectorAll('.sidebar-nav li');
        listItems.forEach(li => {
            if (li.textContent.toLowerCase().includes(tabName)) {
                li.classList.add('active');
            }
        });
    }

    // Dynamic header change
    const title = document.getElementById('admin-title');
    const subtitle = document.getElementById('admin-subtitle');
    if (tabName === 'overview') {
        title.textContent = 'Admin Overview';
        subtitle.textContent = 'Analytics and overall stats dashboard';
    } else if (tabName === 'feedbacks') {
        title.textContent = 'View All Feedback';
        subtitle.textContent = 'Browse, filter, and search full patient feedback logs';
    } else if (tabName === 'doctors') {
        title.textContent = 'Doctor Performance';
        subtitle.textContent = 'Track and compare performance rating of all medical staff';
    } else if (tabName === 'hospitals') {
        title.textContent = 'Hospital Performance';
        subtitle.textContent = 'Rankings and statistics of active medical facilities';
    }
}

// Fetch Admin JSON Database
function loadAdminData() {
    const loadingOverlay = document.getElementById('admin-loading');
    if (loadingOverlay) loadingOverlay.classList.remove('hide-overlay');

    fetch('/admin/data')
    .then(response => {
        if (!response.ok) throw new Error('Failed to load database.');
        return response.json();
    })
    .then(data => {
        // 1. Populate Metrics Cards
        document.getElementById('stat-users').textContent = data.stats.total_users;
        document.getElementById('stat-hospitals').textContent = data.stats.total_hospitals;
        document.getElementById('stat-doctors').textContent = data.stats.total_doctors;
        document.getElementById('stat-feedback').textContent = data.stats.total_feedback;
        document.getElementById('stat-pos').textContent = data.stats.positive_reviews;
        document.getElementById('stat-neg').textContent = data.stats.negative_reviews;
        document.getElementById('stat-best-hosp').textContent = data.stats.best_hospital;
        document.getElementById('stat-best-doc').textContent = data.stats.best_doctor;

        // Save data globally for filters
        window.allFeedbacks = data.feedbacks;
        
        // 2. Render / Update Charts
        renderCharts(data);

        // 3. Render Rankings & Tables
        renderHospitalsRankings(data.hospital_rankings);
        renderDoctorsRankings(data.doctor_rankings);
        renderDoctorPerformanceCards(data.doctor_stats);
        
        // Dynamic Doctor Filter Populator
        const docFilter = document.getElementById('filter-doctor');
        if (docFilter) {
            const currentSelected = docFilter.value;
            docFilter.innerHTML = '<option value="">All Doctors</option>';
            Object.keys(data.doctor_stats).sort().forEach(doc => {
                const opt = document.createElement('option');
                opt.value = doc;
                opt.textContent = doc;
                if (doc === currentSelected) {
                    opt.selected = true;
                }
                docFilter.appendChild(opt);
            });
        }

        // Populate and filter feedbacks table
        applyFilters();
    })
    .catch(err => {
        console.error(err);
        alert('Error loading admin dashboard: ' + err.message);
    })
    .finally(() => {
        if (loadingOverlay) loadingOverlay.classList.add('hide-overlay');
    });
}

// Render dynamic Chart.js charts
function renderCharts(data) {
    // Colors configuration
    const positiveColor = '#10b981'; // Teal/Green
    const negativeColor = '#f43f5e'; // Red
    const primaryColor = '#0ea5e9';  // Blue
    
    // Destroy previous instances to avoid rendering glitches
    if (pieChartInstance) pieChartInstance.destroy();
    if (lineChartInstance) lineChartInstance.destroy();
    if (hospitalChartInstance) hospitalChartInstance.destroy();
    if (doctorChartInstance) doctorChartInstance.destroy();

    // Pie Chart: Positive vs Negative
    const ctxPie = document.getElementById('chart-pie');
    if (ctxPie) {
        pieChartInstance = new Chart(ctxPie, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Negative'],
                datasets: [{
                    data: [data.stats.positive_reviews, data.stats.negative_reviews],
                    backgroundColor: [positiveColor, negativeColor],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { font: { family: 'Outfit', size: 13 } }
                    }
                }
            }
        });
    }

    // Line Chart: Monthly Trends
    const ctxLine = document.getElementById('chart-line');
    if (ctxLine) {
        // Fallback empty trends labels if no feedback is logged yet
        const labels = data.monthly_trends.labels.length > 0 ? data.monthly_trends.labels : ['No Data'];
        const values = data.monthly_trends.values.length > 0 ? data.monthly_trends.values : [0];
        
        lineChartInstance = new Chart(ctxLine, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Feedback count',
                    data: values,
                    borderColor: primaryColor,
                    backgroundColor: 'rgba(14, 165, 233, 0.1)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 3,
                    pointBackgroundColor: primaryColor
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1, font: { family: 'Outfit' } }
                    },
                    x: {
                        ticks: { font: { family: 'Outfit' } }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Hospital Bar Chart (Positive reviews percentage per hospital)
    const ctxHosp = document.getElementById('chart-hospital');
    if (ctxHosp) {
        const hospLabels = data.hospital_rankings.map(h => h.hospital);
        const hospRatings = data.hospital_rankings.map(h => h.rating);
        
        hospitalChartInstance = new Chart(ctxHosp, {
            type: 'bar',
            data: {
                labels: hospLabels,
                datasets: [{
                    label: 'Positive Sentiment %',
                    data: hospRatings,
                    backgroundColor: primaryColor,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        ticks: { font: { family: 'Outfit' } }
                    },
                    x: { ticks: { font: { family: 'Outfit' } } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }

    // Doctor Bar Chart (Positive reviews percentage per doctor)
    const ctxDoc = document.getElementById('chart-doctor');
    if (ctxDoc) {
        // Take top 5 or all doctors
        const docs = data.doctor_rankings.slice(0, 5);
        const docLabels = docs.map(d => d.doctor);
        const docRatings = docs.map(d => d.rating);
        
        doctorChartInstance = new Chart(ctxDoc, {
            type: 'bar',
            data: {
                labels: docLabels,
                datasets: [{
                    label: 'Positive Rating %',
                    data: docRatings,
                    backgroundColor: positiveColor,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        ticks: { font: { family: 'Outfit' } }
                    },
                    x: { ticks: { font: { family: 'Outfit' } } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
}

// Render Hospital Rankings List
function renderHospitalsRankings(rankings) {
    const container = document.getElementById('hospital-ranking-list');
    if (!container) return;

    if (!rankings || rankings.length === 0) {
        container.innerHTML = '<p class="text-center py-4 text-muted">No hospital logs available yet.</p>';
        return;
    }

    let html = '';
    rankings.forEach((h, index) => {
        const rank = index + 1;
        const barColor = h.rating >= 80 ? 'bg-success' : (h.rating >= 60 ? 'bg-warning' : 'bg-danger');
        
        html += `
            <div class="ranking-item">
                <div class="ranking-header">
                    <div class="ranking-title">
                        <span class="ranking-number badge-rank-${rank}">${rank}</span>
                        <strong>${h.hospital}</strong>
                    </div>
                    <span class="ranking-percentage">${h.rating}% Positive <small class="text-muted">(${h.total} reviews)</small></span>
                </div>
                <div class="ranking-progress-bar">
                    <div class="ranking-progress-fill ${barColor}" style="width: ${h.total > 0 ? h.rating : 0}%;"></div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Render Doctor Rankings Table
function renderDoctorsRankings(rankings) {
    const tbody = document.getElementById('doctor-rankings-tbody');
    if (!tbody) return;

    if (!rankings || rankings.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-muted">No doctor logs available yet.</td></tr>';
        return;
    }

    let html = '';
    rankings.forEach((d, index) => {
        const rank = index + 1;
        html += `
            <tr>
                <td><span class="ranking-number badge-rank-${rank}">${rank}</span></td>
                <td><strong>${d.doctor}</strong></td>
                <td>
                    <div class="d-flex align-items-center">
                        <span class="mr-2 font-weight-bold">${d.rating}%</span>
                        <div class="mini-progress-bar">
                            <div class="mini-progress-fill ${d.rating >= 80 ? 'bg-success' : 'bg-warning'}" style="width: ${d.total > 0 ? d.rating : 0}%;"></div>
                        </div>
                    </div>
                </td>
                <td>${d.total} reviews</td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

// Render Doctor Performance detailed cards
function renderDoctorPerformanceCards(stats) {
    const container = document.getElementById('doctor-performance-cards');
    if (!container) return;

    if (!stats || Object.keys(stats).length === 0) {
        container.innerHTML = '<p class="text-center py-4 text-muted">No stats available.</p>';
        return;
    }

    let html = '';
    Object.keys(stats).forEach(doc => {
        const d = stats[doc];
        html += `
            <div class="doctor-perf-card">
                <div class="perf-header">
                    <h4>${doc}</h4>
                    <span class="perf-rating-badge ${d.rating >= 80 ? 'perf-success' : 'perf-warning'}">${d.rating}% Pos</span>
                </div>
                <div class="perf-details">
                    <div class="detail-row">
                        <span>Total Reviews:</span>
                        <strong>${d.total}</strong>
                    </div>
                    <div class="detail-row">
                        <span>Positive:</span>
                        <span class="text-success">${d.positive}</span>
                    </div>
                    <div class="detail-row">
                        <span>Negative:</span>
                        <span class="text-danger">${d.negative}</span>
                    </div>
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
}

// Apply Filters on feedbacks database
function applyFilters() {
    const tbody = document.getElementById('feedback-tbody');
    if (!tbody || !window.allFeedbacks) return;

    const searchVal = document.getElementById('filter-search').value.toLowerCase().trim();
    const hospVal = document.getElementById('filter-hospital').value;
    const docVal = document.getElementById('filter-doctor').value;
    const sentimentVal = document.getElementById('filter-sentiment').value;

    const filtered = window.allFeedbacks.filter(f => {
        // Keyword Search (User, Doctor, Hospital, Feedback)
        const matchSearch = !searchVal || 
            f.user_name.toLowerCase().includes(searchVal) ||
            f.doctor.toLowerCase().includes(searchVal) ||
            f.hospital.toLowerCase().includes(searchVal) ||
            f.feedback.toLowerCase().includes(searchVal);
            
        // Hospital Filter
        const matchHosp = !hospVal || f.hospital === hospVal;
        
        // Doctor Filter
        const matchDoc = !docVal || f.doctor === docVal;
        
        // Sentiment Filter
        const matchSentiment = !sentimentVal || f.predicted_sentiment.toLowerCase() === sentimentVal.toLowerCase();

        return matchSearch && matchHosp && matchDoc && matchSentiment;
    });

    // Sort logs descending by timestamp
    filtered.sort((a, b) => b.timestamp.localeCompare(a.timestamp));

    // Update Matched Count badge
    document.getElementById('filter-count').textContent = filtered.length + ' records match';

    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-muted">No records found matching filters.</td></tr>';
        return;
    }

    let html = '';
    filtered.forEach(f => {
        const sentimentClass = f.predicted_sentiment.toLowerCase() === 'positive' ? 'badge-positive' : 'badge-negative';
        const emoji = f.predicted_sentiment.toLowerCase() === 'positive' ? '😊' : '😟';
        
        html += `
            <tr>
                <td class="nowrap"><i class="fa-solid fa-circle-user text-muted"></i> ${f.user_name}</td>
                <td><strong>${f.hospital}</strong></td>
                <td>
                    <div class="doc-cell">
                        <span>${f.doctor}</span>
                        <small class="text-muted">${f.department}</small>
                    </div>
                </td>
                <td class="feedback-text-cell" title="${f.feedback}">${f.feedback}</td>
                <td>
                    <span class="sentiment-badge ${sentimentClass}">
                        ${emoji} ${f.predicted_sentiment} <span class="conf-percentage">(${f.confidence_score})</span>
                    </span>
                </td>
                <td class="nowrap"><small class="text-muted">${f.date}</small></td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}
