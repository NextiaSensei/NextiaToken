# session_scheduler.py
import json
import logging
from datetime import datetime, time
import threading
import time as time_lib

class SessionScheduler:
    def __init__(self, config_path='config/trading_sessions.json'):
        self.config_path = config_path
        self.trading_sessions = []
        self.is_trading_time = False
        self.load_sessions()
        
    def load_sessions(self):
        """Carga las sesiones de trading desde el archivo JSON"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.trading_sessions = config.get('trading_sessions', [])
            logging.info("Trading sessions loaded successfully")
        except Exception as e:
            logging.error(f"Error loading trading sessions: {e}")
    
    def is_session_active(self):
        """Verifica si estamos en horario de trading"""
        now = datetime.now()
        current_time = now.time()
        current_day = now.strftime('%A').lower()
        
        for session in self.trading_sessions:
            session_days = session.get('days', [])
            start_time = self.parse_time(session.get('start_time', '00:00'))
            end_time = self.parse_time(session.get('end_time', '23:59'))
            
            if current_day in session_days and start_time <= current_time <= end_time:
                return True
        return False
    
    def parse_time(self, time_str):
        """Convierte string de tiempo a objeto time"""
        try:
            hour, minute = map(int, time_str.split(':'))
            return time(hour, minute)
        except:
            return time(0, 0)
    
    def start_scheduler(self):
        """Inicia el monitoreo de sesiones en segundo plano"""
        def monitor_sessions():
            while True:
                self.is_trading_time = self.is_session_active()
                time_lib.sleep(60)  # Verificar cada minuto
        
        scheduler_thread = threading.Thread(target=monitor_sessions, daemon=True)
        scheduler_thread.start()
        logging.info("Session scheduler started")
