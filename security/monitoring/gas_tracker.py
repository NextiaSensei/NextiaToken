
#!/usr/bin/env python3
"""
Nextia Gas Tracker - Monitoreo de gas prices para Ethereum
Herramienta oficial del ecosistema Nextia Token
"""

import requests
import time
import json
from datetime import datetime

class NextiaGasTracker:
    def __init__(self):
        print("🚀 Nextia Gas Tracker Iniciado...")
    
    def get_gas_prices(self):
        try:
            url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
            response = requests.get(url)
            data = response.json()
            
            if data['status'] == '1':
                return {
                    'timestamp': datetime.now().isoformat(),
                    'safe': data['result']['SafeGasPrice'],
                    'standard': data['result']['ProposeGasPrice'],
                    'fast': data['result']['FastGasPrice']
                }
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def run(self):
        while True:
            gas_data = self.get_gas_prices()
            if gas_data:
                print(f"⛽ Gas Prices - Safe: {gas_data['safe']} | Standard: {gas_data['standard']} | Fast: {gas_data['fast']}")
            
            time.sleep(30)

if __name__ == "__main__":
    tracker = NextiaGasTracker()
    tracker.run()
