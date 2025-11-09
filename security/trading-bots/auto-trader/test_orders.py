#!/usr/bin/env python3
"""
Prueba de órdenes reales en Binance Testnet
"""

import logging
from trade_engine import TradeEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_real_orders():
    """Probar órdenes reales de compra/venta"""
    logger.info("🚀 PROBANDO ÓRDENES REALES EN TESTNET")
    
    engine = TradeEngine()
    
    if not engine.initialized:
        logger.error("❌ Trade Engine no inicializado")
        return
    
    # Obtener precio de ADA (barato para testing)
    ada_price = engine.get_current_price('ADAUSDT')
    logger.info(f"📊 Precio ADAUSDT: ${ada_price}")
    
    # Calcular cantidad pequeña para prueba (aprox $1)
    test_quantity = 1.5  # ~$1 USD
    
    # Probar orden de COMPRA
    logger.info("🧪 Probando orden de COMPRA...")
    buy_result = engine.execute_buy_order('ADAUSDT', test_quantity)
    
    if buy_result['success']:
        logger.info(f"✅ COMPRA EXITOSA: {buy_result['executed_quantity']} ADA @ ${buy_result['executed_price']}")
        
        # Probar orden de VENTA
        logger.info("🧪 Probando orden de VENTA...")
        sell_result = engine.execute_sell_order('ADAUSDT', buy_result['executed_quantity'])
        
        if sell_result['success']:
            logger.info(f"✅ VENTA EXITOSA: {sell_result['executed_quantity']} ADA @ ${sell_result['executed_price']}")
        else:
            logger.error(f"❌ VENTA FALLIDA: {sell_result['error']}")
    else:
        logger.error(f"❌ COMPRA FALLIDA: {buy_result['error']}")
    
    # Mostrar reporte final
    report = engine.get_performance_report()
    logger.info("📊 REPORTE FINAL:")
    logger.info(f"   Órdenes totales: {report['total_orders']}")
    logger.info(f"   Órdenes exitosas: {report['successful_orders']}")
    logger.info(f"   Tasa de éxito: {report['success_rate']:.1f}%")

if __name__ == "__main__":
    test_real_orders()
