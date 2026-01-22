"""
Google Maps Scraper para PYMEs en Colombia
Extrae información pública de negocios de Google Maps
"""

import asyncio
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import pandas as pd
import re


class GoogleMapsScraper:
    def __init__(self):
        self.results = []
        self.base_url = "https://www.google.com/maps/search/"

    def clean_phone(self, phone):
        """Limpia y formatea números de teléfono"""
        if not phone:
            return ""
        # Elimina caracteres especiales excepto + y números
        cleaned = re.sub(r'[^\d+]', '', phone)
        return cleaned

    def clean_text(self, text):
        """Limpia texto de espacios y caracteres extraños"""
        if not text:
            return ""
        return " ".join(text.split())

    async def search_places(self, query, max_results=50, scroll_attempts=10):
        """
        Busca lugares en Google Maps

        Args:
            query: Término de búsqueda (ej: "clínica odontológica Medellín")
            max_results: Máximo número de resultados a extraer
            scroll_attempts: Intentos de scroll para cargar más resultados
        """
        print(f"\n🔍 Buscando: {query}")
        print(f"📊 Meta: {max_results} resultados")

        async with async_playwright() as p:
            # Lanzar navegador con configuración anti-detección
            browser = await p.chromium.launch(
                headless=False,  # headless=True para background
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                ]
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='es-CO',
                timezone_id='America/Bogota'
            )

            # Ocultar webdriver
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            page = await context.new_page()

            try:
                # Navegar a Google Maps
                search_url = f"{self.base_url}{query.replace(' ', '+')}"
                print(f"🌐 Navegando a Google Maps...")
                await page.goto(search_url, wait_until='networkidle', timeout=60000)

                # Esperar a que carguen los resultados
                print(f"⏳ Esperando resultados...")
                await asyncio.sleep(5)

                # Scroll para cargar más resultados
                print(f"📜 Cargando resultados...")
                await self._scroll_results(page, scroll_attempts)

                # Extraer datos
                print(f"📦 Extrayendo información...")
                await self._extract_data(page, max_results)

                print(f"✅ Extraídos {len(self.results)} resultados")

            except Exception as e:
                print(f"❌ Error durante el scraping: {str(e)}")

            finally:
                await browser.close()

        return self.results

    async def _scroll_results(self, page, attempts):
        """Hace scroll en el panel de resultados para cargar más lugares"""
        for i in range(attempts):
            try:
                # Buscar el contenedor de resultados
                scrollable = await page.query_selector('div[role="feed"]')

                if scrollable:
                    # Scroll hasta el final del contenedor
                    await page.evaluate('''
                        () => {
                            const feed = document.querySelector('div[role="feed"]');
                            if (feed) {
                                feed.scrollTop = feed.scrollHeight;
                            }
                        }
                    ''')
                    await asyncio.sleep(2)

                    # Verificar si llegamos al final
                    end_text = await page.query_selector('text="Has llegado al final de la lista"')
                    if end_text:
                        print(f"✓ Llegamos al final de los resultados")
                        break

                print(f"  Scroll {i+1}/{attempts}", end='\r')

            except Exception as e:
                print(f"\n⚠ Error en scroll: {str(e)}")
                break

    async def _extract_data(self, page, max_results):
        """Extrae datos de los lugares en la lista"""

        # Obtener todos los enlaces de lugares
        place_links = await page.query_selector_all('a[href*="/maps/place/"]')

        count = 0
        for link in place_links[:max_results]:
            if count >= max_results:
                break

            try:
                # Click en el lugar
                await link.click()
                await asyncio.sleep(2)

                # Extraer información
                place_data = await self._extract_place_details(page)

                if place_data and place_data.get('name'):
                    self.results.append(place_data)
                    count += 1
                    print(f"  ✓ {count}/{max_results}: {place_data['name'][:40]}...", end='\r')

            except Exception as e:
                print(f"\n⚠ Error extrayendo lugar: {str(e)}")
                continue

    async def _extract_place_details(self, page):
        """Extrae detalles de un lugar específico"""
        data = {
            'name': '',
            'rating': '',
            'reviews_count': '',
            'category': '',
            'address': '',
            'phone': '',
            'website': '',
            'hours': '',
            'plus_code': '',
            'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            # Nombre
            name_elem = await page.query_selector('h1')
            if name_elem:
                data['name'] = self.clean_text(await name_elem.inner_text())

            # Rating
            try:
                rating_elem = await page.query_selector('div[role="img"][aria-label*="estrellas"]')
                if rating_elem:
                    aria_label = await rating_elem.get_attribute('aria-label')
                    rating_match = re.search(r'([\d,\.]+)\s*estrellas', aria_label)
                    if rating_match:
                        data['rating'] = rating_match.group(1)
            except:
                pass

            # Número de reseñas
            try:
                reviews_elem = await page.query_selector('button[aria-label*="reseña"]')
                if reviews_elem:
                    aria_label = await reviews_elem.get_attribute('aria-label')
                    reviews_match = re.search(r'([\d\.]+)\s*reseña', aria_label)
                    if reviews_match:
                        data['reviews_count'] = reviews_match.group(1)
            except:
                pass

            # Categoría
            try:
                category_elem = await page.query_selector('button[jsaction*="category"]')
                if category_elem:
                    data['category'] = self.clean_text(await category_elem.inner_text())
            except:
                pass

            # Dirección
            try:
                address_elem = await page.query_selector('button[data-item-id="address"]')
                if address_elem:
                    aria_label = await address_elem.get_attribute('aria-label')
                    if aria_label and 'Dirección:' in aria_label:
                        data['address'] = aria_label.replace('Dirección:', '').strip()
            except:
                pass

            # Teléfono
            try:
                phone_elem = await page.query_selector('button[data-item-id*="phone"]')
                if phone_elem:
                    aria_label = await phone_elem.get_attribute('aria-label')
                    if aria_label:
                        # Extraer el número del aria-label
                        phone_match = re.search(r'[\d\s\+\(\)\-]+', aria_label)
                        if phone_match:
                            data['phone'] = self.clean_phone(phone_match.group(0))
            except:
                pass

            # Sitio web
            try:
                website_elem = await page.query_selector('a[data-item-id="authority"]')
                if website_elem:
                    data['website'] = await website_elem.get_attribute('href')
            except:
                pass

            # Horarios
            try:
                hours_elem = await page.query_selector('button[data-item-id*="oh"]')
                if hours_elem:
                    aria_label = await hours_elem.get_attribute('aria-label')
                    if aria_label:
                        data['hours'] = self.clean_text(aria_label)
            except:
                pass

        except Exception as e:
            print(f"\n⚠ Error en detalles: {str(e)}")

        return data

    def save_to_csv(self, filename='results.csv'):
        """Guarda resultados en CSV"""
        if not self.results:
            print("⚠ No hay resultados para guardar")
            return

        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 Guardado en: {filename}")
        return filename

    def save_to_excel(self, filename='results.xlsx'):
        """Guarda resultados en Excel"""
        if not self.results:
            print("⚠ No hay resultados para guardar")
            return

        df = pd.DataFrame(self.results)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"\n💾 Guardado en: {filename}")
        return filename

    def save_to_json(self, filename='results.json'):
        """Guarda resultados en JSON"""
        if not self.results:
            print("⚠ No hay resultados para guardar")
            return

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Guardado en: {filename}")
        return filename

    def print_summary(self):
        """Imprime resumen de resultados"""
        if not self.results:
            print("\n📊 No hay resultados")
            return

        print(f"\n{'='*60}")
        print(f"📊 RESUMEN DE RESULTADOS")
        print(f"{'='*60}")
        print(f"Total de negocios encontrados: {len(self.results)}")

        with_phone = sum(1 for r in self.results if r.get('phone'))
        with_website = sum(1 for r in self.results if r.get('website'))

        print(f"Con teléfono: {with_phone} ({with_phone/len(self.results)*100:.1f}%)")
        print(f"Con sitio web: {with_website} ({with_website/len(self.results)*100:.1f}%)")
        print(f"{'='*60}\n")


async def main():
    """Función principal de ejemplo"""
    scraper = GoogleMapsScraper()

    # Ejemplos de búsquedas
    queries = [
        "clínica odontológica Medellín",
        # "consultorio estética Bogotá",
        # "clínica oftalmología Cali",
    ]

    for query in queries:
        results = await scraper.search_places(
            query=query,
            max_results=20,  # Ajusta según necesites
            scroll_attempts=5
        )

        # Mostrar resumen
        scraper.print_summary()

        # Guardar resultados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        scraper.save_to_excel(f'pymes_{timestamp}.xlsx')
        scraper.save_to_json(f'pymes_{timestamp}.json')

        # Limpiar para la siguiente búsqueda
        scraper.results = []


if __name__ == "__main__":
    asyncio.run(main())
