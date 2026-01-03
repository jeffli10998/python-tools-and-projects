let trendChart = null;
let currentColumnCount = 2;

const COLOR_PALETTE = [
    '#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#f97316'
];

// Attach global listener immediately
document.addEventListener('paste', handlePaste);

document.addEventListener('DOMContentLoaded', () => {
    initTable();
    initChart();

    // Add listener to the specific fallback paste area if it exists
    const pasteArea = document.getElementById('manual-paste-area');
    if (pasteArea) {
        pasteArea.addEventListener('paste', (e) => {
            // Let the text paste into the box so user sees it, then process it
            setTimeout(() => {
                const text = e.target.value;
                if (text) processPastedData(text);
                e.target.value = ''; // Clear after processing
                e.target.blur(); // Remove focus
            }, 100);
        });

        // Also allow manual button click
        document.getElementById('manual-import-btn')?.addEventListener('click', () => {
            const text = pasteArea.value;
            if (text) {
                processPastedData(text);
                pasteArea.value = '';
            }
        });
    }
});

function initTable() {
    // Start with some empty rows if no data
    for (let i = 0; i < 5; i++) {
        addRow();
    }

    // Load some demo data
    const demo = [
        ['2023-01-01', 20000, 150],
        ['2023-01-02', 20500, 155],
        ['2023-01-03', 20200, 152],
        ['2023-01-04', 21000, 158],
        ['2023-01-05', 20800, 156]
    ];

    fillTableWithData(demo, false);
}

function addRow(values = []) {
    const body = document.getElementById('data-body');
    const tr = document.createElement('tr');

    // Date cell
    let html = `<td><input type="date" class="input-date" value="${values[0] || ''}"></td>`;

    // Series cells
    for (let i = 0; i < currentColumnCount; i++) {
        const val = values[i + 1] !== undefined ? values[i + 1] : '';
        html += `<td><input type="number" class="input-val series-${i}" value="${val}" step="any"></td>`;
    }

    // Action cell
    html += `<td class="action-cell"><button class="btn-secondary" onclick="this.parentElement.parentElement.remove()" style="padding: 0.25rem 0.5rem; background: var(--danger); font-size: 0.8rem;">×</button></td>`;

    tr.innerHTML = html;
    body.appendChild(tr);
}

function addColumn(label = null) {
    const headRow = document.querySelector('#data-head tr');
    const actionCell = headRow.querySelector('.action-cell');

    const newTh = document.createElement('th');
    const index = currentColumnCount;
    const labelVal = label || `Series ${index + 1}`;
    newTh.innerHTML = `<input type="text" class="series-label" value="${labelVal}">`;

    headRow.insertBefore(newTh, actionCell);

    // Add to existing rows
    const rows = document.querySelectorAll('#data-body tr');
    rows.forEach(row => {
        const actionTd = row.querySelector('.action-cell');
        const newTd = document.createElement('td');
        newTd.innerHTML = `<input type="number" class="input-val series-${index}" value="" step="any">`;
        row.insertBefore(newTd, actionTd);
    });

    currentColumnCount++;
}

function clearTable() {
    document.getElementById('data-body').innerHTML = '';
    // Reset to 2 columns
    const headRow = document.querySelector('#data-head tr');
    const labels = headRow.querySelectorAll('.series-label');
    for (let i = labels.length - 1; i >= 2; i--) {
        labels[i].parentElement.remove();
    }
    currentColumnCount = 2;
    // Add 5 empty rows
    for (let i = 0; i < 5; i++) addRow();
}

function handlePaste(e) {
    const clipboardData = e.clipboardData || window.clipboardData;
    const pastedText = clipboardData.getData('text');

    console.log('Paste detected:', pastedText ? pastedText.substring(0, 100) : 'empty');

    if (!pastedText) return;

    // Detect if this looks like Excel/TSV data (has tabs OR multiple lines)
    const hasMultipleLines = pastedText.includes('\n') || pastedText.includes('\r');
    const hasTabs = pastedText.includes('\t');

    // If it's structured data (tabs or multiple lines), process it
    if (hasTabs || (hasMultipleLines && pastedText.split(/\r?\n/).length >= 2)) {
        console.log('Excel/TSV data detected, processing...');
        e.preventDefault();
        e.stopPropagation();
        processPastedData(pastedText);
        return false;
    }

    console.log('Single value paste, allowing default behavior');
}

function processPastedData(text) {
    console.log('Processing pasted data...');
    const lines = text.trim().split(/\r?\n/);
    console.log('Number of lines:', lines.length);

    if (lines.length === 0) return;

    const rawData = lines.map(line => line.split(/\t/));
    console.log('Raw data (first row):', rawData[0]);

    // Check if first row is header
    // Header check: if 2nd or 3rd value in first row is NOT a number, it's a header
    let hasHeader = false;
    if (rawData[0].length > 1) {
        const testVal = rawData[0][1].trim();
        console.log('Testing for header, value:', testVal);
        if (isNaN(parseFloat(testVal)) && testVal !== '') {
            hasHeader = true;
            console.log('Header row detected!');
        }
    }

    let headers = [];
    let dataRows = [];

    if (hasHeader) {
        headers = rawData[0];
        dataRows = rawData.slice(1);
        console.log('Headers:', headers);
    } else {
        dataRows = rawData;
        console.log('No headers, treating all as data');
    }

    console.log('Data rows:', dataRows.length);
    fillTableWithData(dataRows, headers);
}

function fillTableWithData(rows, headers) {
    document.getElementById('data-body').innerHTML = '';

    // Update headers if provided
    if (headers && headers.length > 0) {
        // Reset column count to match headers (min 2)
        const targetColCount = Math.max(2, headers.length - 1);

        // Remove extra columns
        while (currentColumnCount > targetColCount) {
            const headRow = document.querySelector('#data-head tr');
            const labels = headRow.querySelectorAll('.series-label');
            labels[labels.length - 1].parentElement.remove();
            currentColumnCount--;
        }

        // Add needed columns
        while (currentColumnCount < targetColCount) {
            addColumn();
        }

        // Apply header names
        const labelInputs = document.querySelectorAll('.series-label');
        for (let i = 0; i < labelInputs.length; i++) {
            if (headers[i + 1]) {
                labelInputs[i].value = headers[i + 1].trim();
            }
        }
    }

    // Add data rows
    rows.forEach(row => {
        let dateStr = row[0].trim();
        // date cleaning
        const d = new Date(dateStr);
        if (!isNaN(d.getTime())) {
            dateStr = d.toISOString().split('T')[0];
        }

        const values = [dateStr, ...row.slice(1).map(v => v.replace(/[^0-9.-]/g, ''))];

        // Ensure we have enough columns in this row's representation if we aren't adding them globally
        const rowColCount = row.length - 1;
        while (currentColumnCount < rowColCount) {
            addColumn();
        }

        addRow(values);
    });
}

function getTableData() {
    console.log('Gathering table data...');
    const rows = document.querySelectorAll('#data-body tr');
    const labels = Array.from(document.querySelectorAll('.series-label')).map(el => el.value || 'Series');

    console.log('Found rows:', rows.length);
    console.log('Labels:', labels);

    const data = [];
    rows.forEach(row => {
        const date = row.querySelector('.input-date').value;
        if (!date) return;

        const entry = { date };
        let hasValue = false;

        for (let i = 0; i < currentColumnCount; i++) {
            const el = row.querySelector(`.series-${i}`);
            if (el) {
                const val = parseFloat(el.value);
                if (!isNaN(val)) {
                    entry[`series${i + 1}`] = val;
                    hasValue = true;
                }
            }
        }

        if (hasValue) data.push(entry);
    });

    return { data, labels };
}

async function runAnalysis() {
    const { data, labels } = getTableData();
    const method = document.getElementById('method-select').value;

    if (data.length < 2) {
        alert('Please provide at least 2 valid data rows.');
        return;
    }

    try {
        const btn = document.querySelector('.btn-primary');
        console.log('Starting analysis...');
        btn.innerText = 'Analyzing...';
        btn.disabled = true;

        console.log('Sending data to backend:', { data_length: data.length, method });

        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data, method, labels })
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error ${response.status}: ${errorText}`);
        }

        const result = await response.json();
        console.log('Analysis result received:', result);

        btn.innerText = 'Run Analysis';
        btn.disabled = false;

        if (result.error) throw new Error(result.error);

        updateChart(result.data, labels);
        updateCorrelations(result.correlations, labels);
        if (result.insights) {
            renderInsights(result.insights);
        }

        // Scroll to results
        document.querySelector('.output-section').scrollIntoView({ behavior: 'smooth' });

    } catch (err) {
        console.error('Analysis failed:', err);
        alert('Error: ' + err.message);
        const btn = document.querySelector('.btn-primary');
        if (btn) {
            btn.innerText = 'Run Analysis';
            btn.disabled = false;
        }
    }
}

function initChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    trendChart = new Chart(ctx, {
        type: 'line',
        data: { labels: [], datasets: [] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: {
                        color: '#94a3b8',
                        autoSkip: false,
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: { color: '#f8fafc', font: { family: 'Inter', size: 12 } }
                },
                tooltip: {
                    backgroundColor: '#1e293b',
                    titleColor: '#f8fafc',
                    bodyColor: '#94a3b8',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1
                }
            }
        }
    });
}

function updateChart(data, labels) {
    // Ensure chart exists
    if (!trendChart) {
        console.warn('Chart instance not found, re-initializing...');
        initChart();
        if (!trendChart) {
            console.error('Failed to initialize chart');
            return;
        }
    }

    const dates = data.map(d => d.date);
    trendChart.data.labels = dates;

    const datasets = [];
    for (let i = 0; i < labels.length; i++) {
        const key = `series${i + 1}`;
        const color = COLOR_PALETTE[i % COLOR_PALETTE.length];

        datasets.push({
            label: labels[i],
            data: data.map(d => d[key]),
            borderColor: color,
            backgroundColor: `${color}11`,
            borderWidth: 2,
            tension: 0.3,
            fill: true,
            pointRadius: 3,
            pointHoverRadius: 6
        });
    }

    trendChart.data.datasets = datasets;

    // Dynamic resizing for horizontal scroll
    const container = document.querySelector('.chart-container');
    const minWidthPerPoint = 120; // 120px per data point - very wide specifically requested
    const requiredWidth = Math.max(container.parentElement.clientWidth, dates.length * minWidthPerPoint);

    console.log(`Resizing chart to ${requiredWidth}px (Points: ${dates.length})`);
    container.style.width = `${requiredWidth}px`;
    trendChart.resize();

    try {
        trendChart.update();
    } catch (e) {
        console.error('Error updating chart:', e);
        // Fallback: full re-render
        trendChart.destroy();
        initChart();
        updateChart(data, labels);
    }
}

function renderInsights(insights) {
    const container = document.getElementById('dynamic-insights');
    container.innerHTML = '';

    if (!insights || insights.length === 0) {
        container.innerHTML = '<div style="color: var(--text-secondary); font-style: italic;">No insights available.</div>';
        return;
    }

    insights.forEach(insight => {
        const div = document.createElement('div');
        div.className = 'insight-card';
        // Convert simple markdown-like bold syntax to HTML
        const content = insight.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        div.innerHTML = `
            <h4>${insight.title}</h4>
            <p>${content}</p>
        `;
        container.appendChild(div);
    });
}

function updateCorrelations(corrs, labels) {
    const container = document.getElementById('correlation-container');
    container.innerHTML = '';

    const keys = Object.keys(corrs).filter(k => k.startsWith('series'));
    if (keys.length < 2) {
        container.innerHTML = 'Add more series to see correlations.';
        return;
    }

    for (let i = 0; i < keys.length; i++) {
        for (let j = i + 1; j < keys.length; j++) {
            const val = corrs[keys[i]][keys[j]];
            if (val !== undefined) {
                const div = document.createElement('div');
                div.className = 'corr-card';
                div.innerHTML = `
                    <div style="font-size: 0.7rem; color: var(--text-secondary);">${labels[i]} vs ${labels[j]}</div>
                    <div class="corr-value">${val.toFixed(4)}</div>
                `;
                container.appendChild(div);
            }
        }
    }
}
