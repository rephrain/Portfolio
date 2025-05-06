// Initialize chart data
let currentCategory = 'programming'; // Default category
let activeChart = null;
let tooltipTimeout = null;
let skillsData = {};
const skillDetail = document.querySelector('.skill-detail');

// Fetch skills data from Django backend
async function fetchSkillsData() {
    try {
        const response = await fetch('/');
        skillsData = await response.json();
        // Initialize with the first category
        createChart(currentCategory);
        
        // Set up event listeners
        document.querySelectorAll('.category-btn').forEach(button => {
            button.addEventListener('click', function() {
                const category = this.dataset.category;
                document.querySelectorAll('.category-btn').forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                currentCategory = category;
                createChart(category);
            });
        });
        
        // Set the first button as active
        document.querySelector('.category-btn[data-category="programming"]').classList.add('active');
    } catch (error) {
        console.error("Error fetching skills data:", error);
    }
}

// Create the radar chart
function createChart(category) {
    const chartColors = {
        programming: {
            light: {
                bg: 'rgba(59, 130, 246, 0.2)',
                border: '#3b82f6',
                point: '#3b82f6',
                hover: '#2dd4bf'
            },
            dark: {
                bg: 'rgba(2, 132, 199, 0.2)',
                border: '#0284c7',
                point: '#0284c7',
                hover: '#2dd4bf'
            }
        },
        science: {
            light: {
                bg: 'rgba(191, 219, 254, 0.2)',
                border: '#60a5fa',
                point: '#60a5fa',
                hover: '#2563eb'
            },
            dark: {
                bg: 'rgba(37, 99, 235, 0.2)',
                border: '#2563eb',
                point: '#2563eb',
                hover: '#3b82f6'
            }
        },
        engineer: {
            light: {
                bg: 'rgba(199, 210, 254, 0.2)',
                border: '#818cf8',
                point: '#6366f1',
                hover: '#4338ca'
            },
            dark: {
                bg: 'rgba(99, 102, 241, 0.2)',
                border: '#4f46e5',
                point: '#4f46e5',
                hover: '#c4b5fd'
            }
        },
        web: {
            light: {
                bg: 'rgba(220, 252, 231, 0.2)',
                border: '#34d399',
                point: '#22c55e',
                hover: '#166534'
            },
            dark: {
                bg: 'rgba(34, 197, 94, 0.2)',
                border: '#22c55e',
                point: '#22c55e',
                hover: '#86efac'
            }
        },
        tools: {
            light: {
                bg: 'rgba(253, 230, 138, 0.2)',
                border: '#facc15',
                point: '#eab308',
                hover: '#78350f'
            },
            dark: {
                bg: 'rgba(234, 179, 8, 0.2)',
                border: '#d97706',
                point: '#d97706',
                hover: '#fde68a'
            }
        }
    };

    const skills = skillsData[category] || [];
    const ctx = document.getElementById('skillsRadar').getContext('2d');

    if (activeChart) {
        activeChart.destroy();
    }

    const isDarkMode = document.documentElement.classList.contains('dark');
    const theme = isDarkMode ? 'dark' : 'light';
    const colors = chartColors[category]?.[theme] || chartColors.programming.light; // fallback

    const textColor = isDarkMode ? '#e5e7eb' : '#374151';
    const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';

    activeChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: skills.map(skill => skill.name),
            datasets: [{
                label: 'Skill Level',
                data: skills.map(skill => skill.level),
                backgroundColor: colors.bg,
                borderColor: colors.border,
                borderWidth: 2,
                pointBackgroundColor: colors.point,
                pointHoverBackgroundColor: colors.hover,
                pointHoverBorderColor: colors.hover,
                pointHoverRadius: 7,
                pointRadius: 5
            }]
        },
        options: {
            scales: {
                r: {
                    angleLines: {
                        color: gridColor
                    },
                    grid: {
                        color: gridColor
                    },
                    pointLabels: {
                        color: textColor,
                        font: {
                            size: 14,
                            weight: '500'
                        }
                    },
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: textColor,
                        backdropColor: 'transparent'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false,
                    external: function(context) {
                        clearTimeout(tooltipTimeout);
                        
                        if (context.tooltip.opacity === 0) {
                            tooltipTimeout = setTimeout(() => {
                                skillDetail.classList.remove('active');
                            }, 100);
                            return;
                        }
                        
                        const index = context.tooltip.dataPoints[0].dataIndex;
                        const skill = skills[index];
                        
                        document.querySelector('.skill-name').textContent = skill.name;
                        document.querySelector('.skill-level').textContent = skill.level + '%';
                        document.querySelector('.skill-description').textContent = skill.description;
                        
                        skillDetail.classList.add('active');
                    }
                }
            },
            maintainAspectRatio: false,
            responsive: true
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', fetchSkillsData);

// Handle dark mode toggle
document.addEventListener('themeChanged', function() {
    if (currentCategory) {
        createChart(currentCategory);
    }
});