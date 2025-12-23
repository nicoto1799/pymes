"""
Script simple para buscar clínicas en Colombia
Personaliza las búsquedas según tu necesidad
"""

import asyncio
from datetime import datetime
from gmaps_scraper import GoogleMapsScraper


async def buscar_clinicas():
    """Busca clínicas en ciudades principales de Colombia"""

    scraper = GoogleMapsScraper()

    # 🎯 CONFIGURA TUS BÚSQUEDAS AQUÍ
    # ================================

    # Opción 1: Búsqueda simple
    query = "clínica odontológica Medellín"
    max_results = 30

    # Opción 2: Múltiples búsquedas (descomenta para usar)
    # queries = [
    #     "clínica odontológica Medellín",
    #     "clínica odontológica Bogotá",
    #     "clínica odontológica Cali",
    # ]

    print("="*60)
    print("🎯 SCRAPER DE GOOGLE MAPS - PYMES COLOMBIA")
    print("="*60)

    # Realizar búsqueda
    results = await scraper.search_places(
        query=query,
        max_results=max_results,
        scroll_attempts=10
    )

    # Si usas múltiples búsquedas, descomenta esto:
    # for query in queries:
    #     results = await scraper.search_places(
    #         query=query,
    #         max_results=30,
    #         scroll_attempts=8
    #     )
    #     await asyncio.sleep(5)  # Pausa entre búsquedas

    # Mostrar resumen
    scraper.print_summary()

    # Filtrar los que tienen teléfono (importante para WhatsApp)
    with_phone = [r for r in scraper.results if r.get('phone')]
    print(f"💬 Negocios con teléfono (potencial WhatsApp): {len(with_phone)}")

    # Guardar resultados
    if scraper.results:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Guardar todos
        scraper.save_to_csv(f'resultados_{timestamp}.csv')
        scraper.save_to_excel(f'resultados_{timestamp}.xlsx')

        # Guardar solo los que tienen teléfono
        if with_phone:
            import pandas as pd
            df = pd.DataFrame(with_phone)
            df.to_csv(f'leads_con_telefono_{timestamp}.csv', index=False, encoding='utf-8-sig')
            df.to_excel(f'leads_con_telefono_{timestamp}.xlsx', index=False)
            print(f"💾 Leads con teléfono guardados en: leads_con_telefono_{timestamp}.csv/.xlsx")

        print("\n✅ Proceso completado exitosamente!")
        print(f"\n📋 Próximo paso:")
        print(f"   1. Abre el archivo Excel generado")
        print(f"   2. Revisa manualmente los negocios")
        print(f"   3. Prepara tu mensaje personalizado")
        print(f"   4. Contacta 10-20 por día máximo")

    else:
        print("⚠️  No se encontraron resultados. Intenta con otra búsqueda.")


if __name__ == "__main__":
    asyncio.run(buscar_clinicas())
