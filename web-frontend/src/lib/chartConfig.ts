import type { ChartOptions } from 'chart.js';

// Get CSS variable value
const getCSSVariable = (variable: string): string => {
    if (typeof window === 'undefined') return '';
    return getComputedStyle(document.documentElement).getPropertyValue(variable).trim();
};

const oklchToRgba = (oklch: string, alpha: number = 1): string => {
    const cleanOklch = oklch.replace('oklch(', '').replace(')', '').trim();

    if (cleanOklch) {
        return `oklch(${cleanOklch} / ${alpha})`;
    }

    return `rgba(59, 130, 246, ${alpha})`; // fallback
};

// Get current text color based on theme
const getTextColor = (theme?: string): string => {
    if (theme) {
        return theme === 'dark' ? '#ffffff' : '#000000';
    }
    if (typeof window === 'undefined') return '#000000';
    const saved = localStorage.getItem('theme');
    return saved === 'dark' ? '#ffffff' : '#000000';
};

export const getChartColors = (theme?: string) => {
    const muted = getCSSVariable('--muted-foreground');

    const colors = [
        'oklch(0.60 0.25 250)',
        'oklch(0.65 0.22 145)',
        'oklch(0.70 0.20 50)',
        'oklch(0.60 0.25 290)',
        'oklch(0.65 0.20 195)',
        'oklch(0.65 0.22 340)',
    ];

    return {
        colors: colors.map(c => oklchToRgba(c, 0.85)),
        borderColors: colors.map(c => oklchToRgba(c, 1)),
        textColor: getTextColor(theme),
        gridColor: oklchToRgba(muted, 0.2),
    };
};

// Pie chart options (using doughnut with cutout: 0)
export const getDoughnutOptions = (theme?: string): ChartOptions<'doughnut'> => {
    const colors = getChartColors(theme);

    return {
        responsive: true,
        maintainAspectRatio: true,
        cutout: 0, // Makes it a solid pie chart (no hole in center)
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: colors.textColor,
                    padding: 15,
                    font: {
                        size: 12,
                    },
                    usePointStyle: true,
                    pointStyle: 'circle',
                },
                onClick: (_e, legendItem, legend) => {
                    const chart = legend.chart;
                    const dataIndex = legendItem.index!;

                    // Toggle visibility by updating the dataset
                    chart.toggleDataVisibility(dataIndex);
                    chart.update();
                },
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: colors.borderColors[0],
                borderWidth: 1,
                padding: 12,
                displayColors: true,
                callbacks: {
                    label: function (context) {
                        const label = context.label || '';
                        const value = context.parsed;
                        const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
                        const percentage = ((value / total) * 100).toFixed(1);
                        return `${label}: ${value} (${percentage}%)`;
                    }
                }
            },
            datalabels: {
                color: '#fff',
                font: {
                    weight: 'bold' as const,
                    size: 14,
                },
                formatter: (value: number, context: any) => {
                    const total = context.chart.data.datasets[0].data.reduce((a: number, b: number) => a + b, 0);
                    const percentage = ((value / total) * 100).toFixed(1);
                    return `${percentage}%`;
                },
            },
        },
    };
};

// Bar chart options
export const getBarOptions = (theme?: string): ChartOptions<'bar'> => {
    const colors = getChartColors(theme);

    return {
        responsive: true,
        maintainAspectRatio: true,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            datalabels: {
                display: false, // Disable datalabels for bar chart
            },
            legend: {
                position: 'bottom',
                labels: {
                    color: colors.textColor,
                    padding: 15,
                    font: {
                        size: 12,
                    },
                    usePointStyle: true,
                    pointStyle: 'circle',
                },
                onClick: (_e, legendItem, legend) => {
                    const index = legendItem.datasetIndex!;
                    const chart = legend.chart;
                    const meta = chart.getDatasetMeta(index);

                    // Toggle visibility
                    meta.hidden = !meta.hidden;
                    chart.update();
                },
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: colors.borderColors[0],
                borderWidth: 1,
                padding: 12,
                displayColors: true,
                callbacks: {
                    label: function (context) {
                        const label = context.dataset.label || '';
                        const value = context.parsed.y ?? 0;
                        return `${label}: ${value.toFixed(2)}`;
                    }
                }
            },
        },
        scales: {
            x: {
                grid: {
                    color: colors.gridColor,
                },
                ticks: {
                    color: colors.textColor,
                },
            },
            y: {
                grid: {
                    color: colors.gridColor,
                },
                ticks: {
                    color: colors.textColor,
                },
                beginAtZero: true,
            },
        },
    };
};
