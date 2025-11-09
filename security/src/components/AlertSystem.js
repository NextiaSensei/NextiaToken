import React, { useState, useEffect } from 'react';
import AlertForm from './AlertForm';
import { getAlerts, deleteAlert, checkAlerts, requestNotificationPermission } from '../services/alertService';

const AlertSystem = ({ portfolioData }) => {
  const [alerts, setAlerts] = useState([]);
  const [triggeredAlerts, setTriggeredAlerts] = useState([]);

  // Cargar alertas al iniciar
  useEffect(() => {
    const savedAlerts = getAlerts();
    setAlerts(savedAlerts);
    requestNotificationPermission();
  }, []);

  // Verificar alertas cada 30 segundos
  useEffect(() => {
    const interval = setInterval(() => {
      if (Object.keys(portfolioData).length > 0) {
        const triggered = checkAlerts(alerts, portfolioData);
        if (triggered.length > 0) {
          setTriggeredAlerts(prev => [...triggered, ...prev]);
        }
      }
    }, 30000); // 30 segundos

    return () => clearInterval(interval);
  }, [alerts, portfolioData]);

  const handleAlertCreate = (newAlert) => {
    const updatedAlerts = [...alerts, newAlert];
    setAlerts(updatedAlerts);
  };

  const handleDeleteAlert = (alertId) => {
    const updatedAlerts = deleteAlert(alertId);
    setAlerts(updatedAlerts);
  };

  return (
    <div className="alert-system">
      <h3>🔔 Sistema de Alertas</h3>
      
      <div className="alert-system-content">
        {/* Formulario para crear alertas */}
        <div className="alert-form-section">
          <AlertForm onAlertCreate={handleAlertCreate} />
        </div>
        
        {/* Alertas activas */}
        <div className="active-alerts-section">
          <h4>Alertas Activas ({alerts.filter(a => !a.triggered).length})</h4>
          {alerts.filter(alert => !alert.triggered).map(alert => (
            <div key={alert.id} className="alert-item">
              <div className="alert-info">
                <strong>{alert.asset}</strong> - {alert.type} {alert.condition} {alert.value}
                {alert.message && <div className="alert-message">"{alert.message}"</div>}
              </div>
              <button 
                onClick={() => handleDeleteAlert(alert.id)}
                className="btn-delete"
              >
                Eliminar
              </button>
            </div>
          ))}
        </div>

        {/* Alertas disparadas */}
        <div className="triggered-alerts-section">
          <h4>🔴 Alertas Recientes</h4>
          {triggeredAlerts.slice(0, 5).map(alert => (
            <div key={alert.id + alert.triggeredAt} className="triggered-alert">
              <div className="triggered-content">
                <strong>{alert.asset}</strong> - {alert.message || `Alerta disparada!`}
                <div className="triggered-time">
                  {new Date(alert.triggeredAt).toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AlertSystem;
