#!/usr/bin/env python3
"""
Nextia Gas Tracker 2025 - APIs actualizadas para el año 2025
"""
import requests
import time
import json
from datetime import datetime

def get_gas_prices_etherscan_v2():
    """Etherscan API V2 - Endpoint actualizado 2025"""
    try:
        print("🔍 Consultando Etherscan API V2...")
        # Endpoint V2 según documentación actual
        url = "https://api.etherscan.io/v2/gas/now"
        response = requests.get(url, timeout=15)
        data = response.json()
        
        print(f"📦 Respuesta Etherscan V2: {data}")  # DEBUG
        
        if data.get('status') == '1' and 'result' in data:
            result = data['result']
            return {
                'safe': int(result.get('SafeGasPrice', 0)),
                'standard': int(result.get('ProposeGasPrice', 0)),
                'fast': int(result.get('FastGasPrice', 0)),
                'source': 'Etherscan V2',
                'timestamp': datetime.now().isoformat(),
                'real_data': True
            }
        return None
    except Exception as e:
        print(f"❌ Error Etherscan V2: {e}")
        return None

def get_gas_prices_ethgasstation_v2():
    """EthGasStation API actualizada 2025"""
    try:
        print("🔍 Consultando EthGasStation V2...")
        response = requests.get('https://ethgasstation.info/api/ethgasAPI.json', timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"📦 EthGasStation V2: {data}")  # DEBUG
            
            # EthGasStation devuelve precios en decenas de Gwei
            return {
                'safe': data.get('safeLow', 0) / 10,
                'standard': data.get('average', 0) / 10,
                'fast': data.get('fast', 0) / 10,
                'source': 'EthGasStation V2',
                'timestamp': datetime.now().isoformat(),
                'real_data': True
            }
        return None
    except Exception as e:
        print(f"❌ Error EthGasStation V2: {e}")
        return None

def get_gas_prices_beaconchain():
    """Beacon Chain API - Fuente oficial de Ethereum"""
    try:
        print("🔍 Consultando Beacon Chain API...")
        url = "https://beaconcha.in/api/v1/execution/gasnow"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"📦 BeaconChain: {data}")  # DEBUG
            
            if data.get('code') == 200 and 'data' in data:
                gas_data = data['data']
                # Convertir de wei a gwei
                return {
                    'safe': gas_data.get('slow', 0) / 1000000000,
                    'standard': gas_data.get('standard', 0) / 1000000000,
                    'fast': gas_data.get('fast', 0) / 1000000000,
                    'source': 'BeaconChain',
                    'timestamp': datetime.now().isoformat(),
                    'real_data': True
                }
        return None
    except Exception as e:
        print(f"❌ Error BeaconChain: {e}")
        return None

def get_gas_prices_web3():
    """Web3 RPC directo - Fuente más confiable"""
    try:
        print("🔍 Consultando via Web3 RPC...")
        # Usar RPC público de Ethereum
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_gasPrice",
            "params": [],
            "id": 1
        }
        
        rpc_urls = [
            "https://cloudflare-eth.com",
            "https://rpc.ankr.com/eth",
            "https://eth-mainnet.public.blastapi.io"
        ]
        
        for rpc_url in rpc_urls:
            try:
                response = requests.post(rpc_url, json=payload, timeout=15)
                data = response.json()
                
                if 'result' in data:
                    gas_price_wei = int(data['result'], 16)
                    gas_price_gwei = gas_price_wei / 1000000000
                    
                    return {
                        'safe': gas_price_gwei * 0.8,
                        'standard': gas_price_gwei,
                        'fast': gas_price_gwei * 1.2,
                        'source': f'Web3 RPC - {rpc_url.split("//")[1].split("/")[0]}',
                        'timestamp': datetime.now().isoformat(),
                        'real_data': True
                    }
            except:
                continue
                
        return None
    except Exception as e:
        print(f"❌ Error Web3 RPC: {e}")
        return None

def get_gas_prices_2025():
    """Obtener precios de fuentes actualizadas 2025"""
    sources = [
        get_gas_prices_web3,           # Más confiable
        get_gas_prices_beaconchain,    # Oficial de Ethereum
        get_gas_prices_ethgasstation_v2,
        get_gas_prices_etherscan_v2
    ]
    
    for source in sources:
        gas_data = source()
        if gas_data and gas_data.get('safe', 0) > 0:
            return gas_data
    
    return None

def main():
    print("🚀 NEXTIA GAS TRACKER 2025 - APIS ACTUALIZADAS")
    print("💡 Monitoreo en tiempo real con APIs modernas")
    print("⏰ Actualizando cada 45 segundos...")
    print("📍 Presiona CTRL + C para detener\n")
    
    real_data_count = 0
    total_attempts = 0
    
    try:
        while True:
            total_attempts += 1
            print(f"🔄 Intento #{total_attempts}")
            
            gas_data = get_gas_prices_2025()
            
            if gas_data and gas_data.get('real_data', False):
                real_data_count += 1
                print(f"✅ DATOS REALES 2025 - Fuente: {gas_data['source']}")
                print(f"⛽ 🟢 SAFE: {gas_data['safe']:.1f} Gwei")
                print(f"⛽ 🟡 STANDARD: {gas_data['standard']:.1f} Gwei") 
                print(f"⛽ 🔴 FAST: {gas_data['fast']:.1f} Gwei")
                
                success_rate = (real_data_count / total_attempts) * 100
                print(f"📊 Tasa de éxito: {success_rate:.1f}% ({real_data_count}/{total_attempts})")
                print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("=" * 60)
                
                # Guardar datos reales
                with open('security/logs/gas_prices_2025.log', 'a') as f:
                    f.write(json.dumps(gas_data) + '\n')
                    
            else:
                print(f"❌ No se pudieron obtener datos reales")
                print(f"💡 Estado: {real_data_count} exitosos de {total_attempts} intentos")
                print(f"🔧 Soluciones:")
                print(f"   • Verificar conexión a internet")
                print(f"   • Las APIs pueden estar temporalmente offline")
                print(f"   • Considerar usar VPN si hay bloqueos regionales")
                print("=" * 60)
            
            time.sleep(45)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Nextia Gas Tracker 2025 detenido")
        if real_data_count > 0:
            success_rate = (real_data_count / total_attempts) * 100
            print(f"📊 Final: {success_rate:.1f}% de datos reales")
            print("🎉 ¡Herramienta funcionando con APIs 2025!")
        else:
            print("⚠️ Se necesitan ajustes de red o APIs")

if __name__ == "__main__":
    main()
