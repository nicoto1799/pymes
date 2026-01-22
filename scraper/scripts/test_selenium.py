"""
Script de prueba con Selenium - Extrae solo 5 resultados
"""

from gmaps_scraper_selenium import GoogleMapsScraperSelenium
from datetime import datetime


def test():
    print("🧪 Probando el scraper con Selenium...")
    print("Búsqueda: clínica odontológica Medellín")
    print("Resultados: 5 (prueba)\n")

    scraper = GoogleMapsScraperSelenium(headless=False)

    results = scraper.search_places(
        query="clínica odontológica Medellín",
        max_results=5,
        scroll_attempts=3
    )

    scraper.print_summary()

    if results:
        scraper.save_to_csv('test_selenium_resultados.csv')
        scraper.save_to_excel('test_selenium_resultados.xlsx')
        print("\n✅ ¡Funciona! Ya puedes usar los scripts completos.")
    else:
        print("\n⚠️ No se encontraron resultados. Verifica tu conexión.")


if __name__ == "__main__":
    test()
