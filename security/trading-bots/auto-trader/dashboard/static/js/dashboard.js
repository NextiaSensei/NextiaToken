class NextiaTradingDashboard {
    constructor() {
        this.performanceChart = null;
        this.metricsChart = null;
        this.lastData = null;
        this.init();
    }

    init() {
        this.loadData();
        // Actualizar cada 5 segundos
        setInterval(() => this.loadData(), 5000);
        
        // Animaciones de entrada
        this.animateStats();
    }

    animateStats() {
        const stats = document.querySelectorAll('.stat-value');
        stats.forEach(stat => {
            if (stat.textContent === '--') {
                stat.style.opacity = '0';
                setTimeout(() => {
                    stat.style.transition = 'opacity 0.5s ease';
                    stat.style.opacity = '1';
                }, 100);
            }
        });
    }

    async loadData() {
        try {
            const [dashboardResponse, statusResponse] = await Promise.all([
                fetch('/api/dashboard-data'),
                fetch('/api/system-status')
            ]);

            const dashboardData = await dashboardResponse.json();
            const systemStatus = await statusResponse.json();

            this.updateDashboard(dashboardData, systemStatus);
            this.updateLastUpdate();

        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Error conectando con el servidor');
        }
    }

    updateDashboard(data, status) {
        // Actualizar stats principales
        this.updateStats(data);
        
        // Actualizar gráficos
        this.updatePerformanceChart(data.performance_history || []);
        this.updateMetricsChart(data.metrics || {});
        
        // Actualizar trades
        this.updateTradesTable(data.recent_trades || []);
        
        this.lastData = data;
    }

    updateStats(data) {
        const balance = data.current_balance || 0;
        const metrics = data.metrics || {};
        
        // Balance actual
        document.getElementById('currentBalance').textContent = `$${balance.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        
        // Trades activos (simulado por ahora)
        document.getElementById('activeTrades').textContent = metrics.total_trades || '0';
        
        // P&L del día
        const todayPnl = metrics.total_pnl || 0;
        document.getElementById('todayPnl').textContent = `$${todayPnl.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        document.getElementById('pnlChange').textContent = todayPnl >= 0 ? '📈 Tendencia positiva' : '📉 Tendencia negativa';
        document.getElementById('pnlChange').className = `stat-change ${todayPnl >= 0 ? 'positive' : 'negative'}`;
        
        // Win Rate
        const winRate = metrics.win_rate || 0;
        document.getElementById('winRate').textContent = `${winRate.toFixed(1)}%`;
        
        // Cambio de balance (simulado)
        if (this.lastData && this.lastData.current_balance) {
            const change = balance - this.lastData.current_balance;
            document.getElementById('balanceChange').textContent = 
                `${change >= 0 ? '+' : ''}$${change.toFixed(2)}`;
            document.getElementById('balanceChange').className = 
                `stat-change ${change >= 0 ? 'positive' : 'negative'}`;
        }
    }

    updatePerformanceChart(performanceData) {
        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        if (this.performanceChart) {
            this.performanceChart.destroy();
        }

        const labels = performanceData.map(p => new Date(p.timestamp));
        const data = performanceData.map(p => p.balance);

        this.performanceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Balance (USDT)',
                    data: data,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function(context) {
                                return `Balance: $${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'hour',
                            displayFormats: {
                                hour: 'HH:mm'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Tiempo'
                        }
                    },
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Balance (USDT)'
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'nearest'
                }
            }
        });
    }

    updateMetricsChart(metrics) {
        const ctx = document.getElementById('metricsChart').getContext('2d');
        
        if (this.metricsChart) {
            this.metricsChart.destroy();
        }

        const winRate = metrics.win_rate || 0;
        const totalTrades = metrics.total_trades || 0;
        const winningTrades = metrics.winning_trades || 0;
        const losingTrades = totalTrades - winningTrades;

        this.metricsChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Trades Ganadores', 'Trades Perdedores'],
                datasets: [{
                    data: [winningTrades, losingTrades],
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderColor: ['#ffffff', '#ffffff'],
                    borderWidth: 2,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label;
                                const value = context.raw;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '70%',
            }
        });
    }

    updateTradesTable(trades) {
        const container = document.getElementById('tradesContainer');
        
        if (trades.length === 0) {
            container.innerHTML = '<div class="loading">No hay trades recientes</div>';
            return;
        }

        let html = `
            <div class="trade-item header">
                <div>Símbolo</div>
                <div>Tipo</div>
                <div>Precio</div>
                <div>Cantidad</div>
                <div>P&L</div>
            </div>
        `;

        trades.forEach(trade => {
            const timestamp = new Date(trade.timestamp).toLocaleTimeString();
            const pnl = trade.pnl || 0;
            
            html += `
                <div class="trade-item">
                    <div class="trade-symbol">${trade.symbol}</div>
                    <div class="trade-type ${trade.type.toLowerCase()}">${trade.type}</div>
                    <div>$${parseFloat(trade.price).toFixed(4)}</div>
                    <div>${parseFloat(trade.quantity).toFixed(6)}</div>
                    <div class="trade-pnl ${pnl >= 0 ? 'positive' : 'negative'}">
                        ${pnl >= 0 ? '+' : ''}$${pnl.toFixed(2)}
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    updateLastUpdate() {
        const now = new Date();
        document.getElementById('lastUpdate').textContent = 
            `Última actualización: ${now.toLocaleTimeString()}`;
    }

    showError(message) {
        const container = document.getElementById('tradesContainer');
        container.innerHTML = `<div class="loading error">${message}</div>`;
    }
}

// Inicializar dashboard cuando la página cargue
document.addEventListener('DOMContentLoaded', () => {
    new NextiaTradingDashboard();
});
