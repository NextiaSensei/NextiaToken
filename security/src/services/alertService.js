// Servicio para manejar la lógica de alertas
export const checkAlerts = (alerts, marketData) => {
  const triggered = [];
  
  alerts.forEach(alert => {
    if (!alert.active || alert.triggered) return;
    
    const currentData = marketData[alert.asset];
    if (!currentData) return;
    
    let shouldTrigger = false;
    
    switch(alert.type) {
      case 'price':
        if (alert.condition === 'above' && currentData.price >= alert.value) {
          shouldTrigger = true;
        } else if (alert.condition === 'below' && currentData.price <= alert.value) {
          shouldTrigger = true;
        }
        break;
        
      case 'percentage':
        const change = Math.abs(currentData.changePercent);
        if (change >= alert.value) {
          shouldTrigger = true;
        }
        break;
        
      case 'volume':
        if (currentData.volume > alert.value) {
          shouldTrigger = true;
        }
        break;
        
      default:
        break;
    }
    
    if (shouldTrigger) {
      const triggeredAlert = {
        ...alert,
        triggeredAt: new Date(),
        currentValue: currentData.price
      };
      triggered.push(triggeredAlert);
      
      // Mostrar notificación del navegador
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(`🔔 Alerta: ${alert.asset}`, {
          body: `${alert.asset} ${alert.condition} ${alert.value}`,
          icon: '/favicon.ico'
        });
      }
    }
  });
  
  return triggered;
};

// Crear nueva alerta
export const createAlert = (alertData) => {
  const newAlert = {
    id: Date.now(),
    ...alertData,
    active: true,
    triggered: false,
    createdAt: new Date()
  };
  
  // Guardar en localStorage
  const existingAlerts = JSON.parse(localStorage.getItem('portfolioAlerts') || '[]');
  existingAlerts.push(newAlert);
  localStorage.setItem('portfolioAlerts', JSON.stringify(existingAlerts));
  
  return newAlert;
};

// Obtener alertas existentes
export const getAlerts = () => {
  return JSON.parse(localStorage.getItem('portfolioAlerts') || '[]');
};

// Eliminar alerta
export const deleteAlert = (alertId) => {
  const alerts = getAlerts();
  const filteredAlerts = alerts.filter(alert => alert.id !== alertId);
  localStorage.setItem('portfolioAlerts', JSON.stringify(filteredAlerts));
  return filteredAlerts;
};

// Solicitar permisos para notificaciones
export const requestNotificationPermission = () => {
  if ('Notification' in window) {
    Notification.requestPermission();
  }
};
