# session_scheduler.py
import json
import logging
from datetime import datetime, time, timedelta
import threading
import time as time_lib
from typing import List, Dict, Optional, Tuple

class SessionScheduler:
    def __init__(self, config_path: str = 'config/trading_sessions.json'):
        self.config_path = config_path
        self.trading_sessions: List[Dict] = []
        self.is_trading_time: bool = False
        self.last_state_check: Optional[datetime] = None
        self.state_change_callbacks = []
        
        # Stats tracking
        self.stats = {
            'last_state_change': None,
            'total_uptime_minutes': 0,
            'total_downtime_minutes': 0,
            'state_changes': 0
        }
        
        # PRIMERO configurar logging
        self._setup_logging()
        # LUEGO cargar sesiones
        self.load_sessions()
    
    def _setup_logging(self):
        """Configura logging profesional para el scheduler"""
        # Solo configurar si no hay handlers existentes
        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        self.logger = logging.getLogger('SessionScheduler')
    
    def load_sessions(self) -> bool:
        """Carga las sesiones de trading desde el archivo JSON con manejo robusto de errores"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.trading_sessions = config.get('trading_sessions', [])
            
            self.logger.info(f"✅ Trading sessions loaded: {len(self.trading_sessions)} sessions configured")
            return True
            
        except FileNotFoundError:
            self.logger.error(f"❌ Config file not found: {self.config_path}")
            # Configuración por defecto de emergencia
            self._setup_default_sessions()
            return False
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Invalid JSON in config file: {e}")
            self._setup_default_sessions()
            return False
        except Exception as e:
            self.logger.error(f"❌ Unexpected error loading sessions: {e}")
            self._setup_default_sessions()
            return False
    
    def _setup_default_sessions(self):
        """Configura sesiones por defecto en caso de error"""
        self.trading_sessions = [
            {
                "name": "Weekday Session",
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                "start_time": "09:00",
                "end_time": "17:00"
            },
            {
                "name": "Saturday Session", 
                "days": ["saturday"],
                "start_time": "10:00", 
                "end_time": "14:00"
            }
        ]
        self.logger.warning("⚠️  Using default trading sessions as fallback")
    
    def add_state_change_callback(self, callback: callable):
        """Agrega callback para notificar cambios de estado"""
        self.state_change_callbacks.append(callback)
    
    def _notify_state_change(self, new_state: bool):
        """Notifica a todos los callbacks registrados del cambio de estado"""
        for callback in self.state_change_callbacks:
            try:
                callback(new_state)
            except Exception as e:
                self.logger.error(f"Error in state change callback: {e}")
    
    def is_session_active(self) -> bool:
        """Verifica si estamos en horario de trading activo"""
        now = datetime.now()
        current_time = now.time()
        current_day = now.strftime('%A').lower()
        
        for session in self.trading_sessions:
            session_days = [day.lower() for day in session.get('days', [])]
            start_time = self.parse_time(session.get('start_time', '00:00'))
            end_time = self.parse_time(session.get('end_time', '23:59'))
            
            if current_day in session_days and start_time <= current_time <= end_time:
                return True
        return False
    
    def parse_time(self, time_str: str) -> time:
        """Convierte string de tiempo a objeto time con validación robusta"""
        try:
            if ':' in time_str:
                hour, minute = map(int, time_str.split(':'))
            else:
                hour, minute = int(time_str), 0
            
            # Validación de rangos
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return time(hour, minute)
            else:
                raise ValueError("Invalid time range")
                
        except (ValueError, AttributeError) as e:
            self.logger.warning(f"Invalid time format: {time_str}, using 00:00. Error: {e}")
            return time(0, 0)
    
    def get_next_session_info(self) -> Tuple[Optional[datetime], Optional[timedelta]]:
        """Obtiene información de la próxima sesión y tiempo restante"""
        now = datetime.now()
        current_time = now.time()
        current_day = now.strftime('%A').lower()
        
        # Buscar la próxima sesión válida
        for session in self.trading_sessions:
            session_days = [day.lower() for day in session.get('days', [])]
            start_time = self.parse_time(session.get('start_time', '00:00'))
            
            for day in session_days:
                # Calcular próxima ocurrencia de este día
                days_ahead = (self._get_day_number(day) - now.weekday()) % 7
                next_date = now + timedelta(days=days_ahead)
                session_datetime = datetime.combine(next_date.date(), start_time)
                
                # Si es hoy pero ya pasó la hora, buscar próxima semana
                if days_ahead == 0 and current_time > start_time:
                    session_datetime += timedelta(days=7)
                
                if session_datetime > now:
                    time_until = session_datetime - now
                    return session_datetime, time_until
        
        return None, None
    
    def _get_day_number(self, day_name: str) -> int:
        """Convierte nombre de día a número (0=lunes, 6=domingo)"""
        days = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        return days.get(day_name.lower(), 0)
    
    def should_trade(self) -> Tuple[bool, Optional[int]]:
        """
        Verifica si se puede tradear y devuelve tiempo de espera recomendado
        
        Returns:
            Tuple[bool, Optional[int]]: (puede_tradear, segundos_para_esperar)
        """
        current_state = self.is_session_active()
        now = datetime.now()
        
        # Actualizar stats si hay cambio de estado
        if current_state != self.is_trading_time:
            self._update_state_stats(current_state, now)
            self._notify_state_change(current_state)
            
            if current_state:
                self.logger.info("🟢 TRADING SESSION ACTIVATED - Sistema operativo")
            else:
                self.logger.info("🔴 TRADING SESSION ENDED - Entrando en modo espera")
        
        self.is_trading_time = current_state
        self.last_state_check = now
        
        if current_state:
            return True, 60  # Revisar cada minuto durante sesión activa
        else:
            # Fuera de horario - calcular espera inteligente
            wait_time = self._calculate_optimal_wait_time()
            next_session, time_until = self.get_next_session_info()
            
            if next_session:
                self.logger.info(f"⏰ Modo espera - Próxima sesión: {next_session.strftime('%Y-%m-%d %H:%M')} "
                               f"(en {self._format_timedelta(time_until)})")
            else:
                self.logger.info("⏰ Modo espera - No hay sesiones programadas")
                
            return False, wait_time
    
    def _calculate_optimal_wait_time(self) -> int:
        """Calcula tiempo de espera óptimo basado en proximidad a próxima sesión"""
        next_session, time_until = self.get_next_session_info()
        
        if not next_session:
            return 300  # 5 minutos por defecto
        
        total_seconds = time_until.total_seconds()
        
        # Espera más larga si falta mucho tiempo, más corta cerca de la sesión
        if total_seconds > 3600:  # Más de 1 hora
            return 300  # 5 minutos
        elif total_seconds > 600:  # Más de 10 minutos
            return 120  # 2 minutos
        else:  # Menos de 10 minutos
            return 60   # 1 minuto
    
    def _format_timedelta(self, td: timedelta) -> str:
        """Formatea timedelta a string legible"""
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def _update_state_stats(self, new_state: bool, timestamp: datetime):
        """Actualiza estadísticas del scheduler"""
        if self.stats['last_state_change']:
            time_diff = (timestamp - self.stats['last_state_change']).total_seconds() / 60
            
            if self.is_trading_time:  # Estado anterior era trading
                self.stats['total_uptime_minutes'] += time_diff
            else:  # Estado anterior era no-trading
                self.stats['total_downtime_minutes'] += time_diff
        
        self.stats['last_state_change'] = timestamp
        self.stats['state_changes'] += 1
    
    def get_scheduler_stats(self) -> Dict:
        """Devuelve estadísticas del scheduler"""
        return self.stats.copy()
    
    def start_scheduler(self):
        """Inicia el monitoreo de sesiones en segundo plano"""
        def monitor_sessions():
            self.logger.info("🚀 Session Scheduler iniciado - Monitoreo activo")
            
            while True:
                can_trade, wait_seconds = self.should_trade()
                
                # Solo dormir si no estamos en sesión activa
                if not can_trade:
                    time_lib.sleep(wait_seconds)
                else:
                    # En sesión activa, verificar más frecuentemente
                    time_lib.sleep(60)
        
        scheduler_thread = threading.Thread(target=monitor_sessions, daemon=True)
        scheduler_thread.start()
        
        self.logger.info("✅ Session Scheduler running in background")
