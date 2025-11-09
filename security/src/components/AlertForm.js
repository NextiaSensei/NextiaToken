import React, { useState } from 'react';
import { createAlert } from '../services/alertService';

const AlertForm = ({ onAlertCreate }) => {
  const [formData, setFormData] = useState({
    asset: '',
    type: 'price',
    condition: 'above',
    value: '',
    message: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const newAlert = createAlert({
      ...formData,
      value: parseFloat(formData.value)
    });
    
    onAlertCreate(newAlert);
    
    // Reset form
    setFormData({
      asset: '',
      type: 'price',
      condition: 'above',
      value: '',
      message: ''
    });
    
    alert('Alerta creada exitosamente! 🚨');
  };

  return (
    <form onSubmit={handleSubmit} className="alert-form">
      <h4>Crear Nueva Alerta</h4>
      
      <div className="form-group">
        <label>Activo (Ej: AAPL, BTC):</label>
        <input
          type="text"
          name="asset"
          value={formData.asset}
          onChange={handleChange}
          placeholder="Ingresa el símbolo"
          required
        />
      </div>
      
      <div className="form-group">
        <label>Tipo de Alerta:</label>
        <select name="type" value={formData.type} onChange={handleChange}>
          <option value="price">Precio</option>
          <option value="percentage">Cambio Porcentual</option>
          <option value="volume">Volumen</option>
        </select>
      </div>
      
      <div className="form-group">
        <label>Condición:</label>
        <select name="condition" value={formData.condition} onChange={handleChange}>
          <option value="above">Por encima de</option>
          <option value="below">Por debajo de</option>
        </select>
      </div>
      
      <div className="form-group">
        <label>Valor Objetivo:</label>
        <input
          type="number"
          name="value"
          value={formData.value}
          onChange={handleChange}
          placeholder="Ej: 150.50"
          step="0.01"
          required
        />
      </div>
      
      <div className="form-group">
        <label>Mensaje Personalizado (opcional):</label>
        <input
          type="text"
          name="message"
          value={formData.message}
          onChange={handleChange}
          placeholder="Ej: Bitcoin superó resistencia"
        />
      </div>
      
      <button type="submit" className="btn-primary">
        Crear Alerta
      </button>
    </form>
  );
};

export default AlertForm;
