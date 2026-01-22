"""
Script de prueba rápido - Extrae solo 5 resultados
"""

import asyncio
from gmaps_scraper import GoogleMapsScraper


async def test():
    print("🧪 Probando el scraper...")
    print("Búsqueda: clínica odontológica Medellín")
    print("Resultados: 5 (prueba)\n")

    scraper = GoogleMapsScraper()

    results = await scraper.search_places(
        query="clínica odontológica Medellín",
        max_results=5,
        scroll_attempts=3
    )

    scraper.print_summary()

    if scraper.results:
        scraper.save_to_excel('test_resultados.xlsx')
        print("\n✅ ¡Funciona! Ya puedes usar los scripts completos.")
    else:
        print("\n⚠️ No se encontraron resultados. Verifica tu conexión.")


if __name__ == "__main__":
    asyncio.run(test())
