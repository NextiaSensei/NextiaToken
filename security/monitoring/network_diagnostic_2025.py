#!/usr/bin/env python3
"""
Nextia Network Diagnostic 2025 - Diagnóstico completo de red y APIs
Herramienta oficial del ecosistema Nextia Token
"""
import requests
import socket
import ssl
import json
import time
from datetime import datetime

def test_dns_resolution():
    """Probar resolución DNS de APIs críticas"""
    print("1. 🔍 PROBANDO RESOLUCIÓN DNS...")
    hosts = [
        'google.com',
        'binance.com',
        'etherscan.io', 
        'ethgasstation.info',
        'beaconcha.in',
        'cloudflare-eth.com',
        'rpc.ankr.com'
    ]
    
    for host in hosts:
        try:
            ip = socket.gethostbyname(host)
            print(f"   ✅ {host:.<25} -> {ip}")
        except Exception as e:
            print(f"   ❌ {host:.<25} -> ERROR: {e}")

def test_ssl_connections():
    """Probar conexiones SSL/TLS a APIs"""
    print("\n2. 🔐 PROBANDO CONEXIONES SSL/TLS...")
    urls = [
        'https://api.binance.com',
        'https://api.etherscan.io',
        'https://ethgasstation.info',
        'https://beaconcha.in',
        'https://cloudflare-eth.com'
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            ssl_info = f"SSL {response.connection.ssl_version if hasattr(response.connection, 'ssl_version') else 'OK'}"
            print(f"   ✅ {url:.<30} Status: {response.status_code} | {ssl_info}")
        except Exception as e:
            print(f"   ❌ {url:.<30} ERROR: {e}")

def test_gas_apis_2025():
    """Probar APIs de gas específicas 2025"""
    print("\n3. ⛽ PROBANDO APIS DE GAS 2025...")
    
    apis = [
        {
            "name": "Etherscan V2",
            "url": "https://api.etherscan.io/v2/gas/now",
            "method": "GET"
        },
        {
            "name": "EthGasStation", 
            "url": "https://ethgasstation.info/api/ethgasAPI.json",
            "method": "GET"
        },
        {
            "name": "BeaconChain Gas",
            "url": "https://beaconcha.in/api/v1/execution/gasnow",
            "method": "GET"
        },
        {
            "name": "Web3 RPC (Cloudflare)",
            "url": "https://cloudflare-eth.com",
            "method": "POST",
            "data": {"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}
        },
        {
            "name": "Web3 RPC (Ankr)",
            "url": "https://rpc.ankr.com/eth", 
            "method": "POST",
            "data": {"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}
        }
    ]
    
    for api in apis:
        try:
            print(f"   🔍 {api['name']:.<25}", end="")
            
            if api['method'] == 'GET':
                response = requests.get(api['url'], timeout=15)
            else:
                response = requests.post(api['url'], json=api['data'], timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f" ✅ Status: {response.status_code}")
                
                # Mostrar datos relevantes si existen
                if 'result' in data:
                    print(f"      📦 Result: {str(data['result'])[:50]}...")
                elif 'data' in data:
                    print(f"      📦 Data: {str(data['data'])[:50]}...")
                else:
                    print(f"      📦 Response: {str(data)[:50]}...")
            else:
                print(f" ❌ Status: {response.status_code}")
                print(f"      💬 Error: {response.text[:100]}")
                
        except Exception as e:
            print(f" ❌ ERROR: {str(e)[:50]}")

def test_market_data_apis():
    """Probar APIs de datos de mercado"""
    print("\n4. 📊 PROBANDO APIS DE DATOS DE MERCADO...")
    
    market_apis = [
        {
            "name": "Binance API",
            "url": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
            "method": "GET"
        },
        {
            "name": "CoinGecko API",
            "url": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            "method": "GET" 
        }
    ]
    
    for api in market_apis:
        try:
            print(f"   🔍 {api['name']:.<25}", end="")
            response = requests.get(api['url'], timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f" ✅ Status: {response.status_code}")
                
                # Mostrar precio si está disponible
                if 'price' in str(data) or 'usd' in str(data):
                    print(f"      💰 Datos de precio recibidos")
                else:
                    print(f"      📦 {str(data)[:50]}...")
            else:
                print(f" ❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f" ❌ ERROR: {str(e)[:50]}")

def test_network_config():
    """Probar configuración de red general"""
    print("\n5. 🌐 PROBANDO CONFIGURACIÓN DE RED...")
    
    try:
        # Test de conectividad general
        ip_test = requests.get('https://httpbin.org/ip', timeout=10).json()
        print(f"   ✅ IP Pública: {ip_test['origin']}")
        
        # Test de velocidad básico
        start_time = time.time()
        speed_test = requests.get('https://httpbin.org/bytes/1024', timeout=10)
        download_time = time.time() - start_time
        speed_kbps = (1024 / download_time) / 1024
        
        print(f"   ✅ Velocidad descarga: {speed_kbps:.2f} MB/s")
        print(f"   ✅ Latencia: {download_time:.2f} segundos")
        
    except Exception as e:
        print(f"   ❌ Configuración red: {e}")

def main():
    print("🔧 NEXTIA NETWORK DIAGNOSTIC 2025")
    print("💡 Diagnóstico completo de conectividad y APIs")
    print("=" * 60)
    
    # Ejecutar todas las pruebas
    test_dns_resolution()
    test_ssl_connections() 
    test_gas_apis_2025()
    test_market_data_apis()
    test_network_config()
    
    print("\n" + "=" * 60)
    print("🧪 DIAGNÓSTICO COMPLETADO")
    print("💡 RECOMENDACIONES:")
    print("   • Si fallan APIs, prueba con VPN")
    print("   • Verifica firewall de Kali Linux")
    print("   • Usa DNS 1.1.1.1 o 8.8.8.8 si hay problemas DNS")
    print("   • Considera API keys para endpoints rate-limited")
    print(f"⏰ Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
