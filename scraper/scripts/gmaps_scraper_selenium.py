"""
Google Maps Scraper usando Selenium (más estable)
Extrae información pública de negocios de Google Maps
"""

import time
import json
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


class GoogleMapsScraperSelenium:
    def __init__(self, headless=False):
        self.results = []
        self.base_url = "https://www.google.com/maps/search/"
        self.headless = headless
        self.driver = None

    def setup_driver(self):
        """Configura el driver de Chrome"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # Ocultar webdriver
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        try:
            # Instalar chromedriver automáticamente
            driver_path = ChromeDriverManager().install()

            # Fix para Mac ARM - el driver está en un subdirectorio
            import os
            import stat
            if 'THIRD_PARTY' in driver_path or not driver_path.endswith('chromedriver'):
                # Buscar el chromedriver real
                driver_dir = os.path.dirname(driver_path)
                actual_driver = os.path.join(driver_dir, 'chromedriver')
                if os.path.exists(actual_driver):
                    driver_path = actual_driver

            # Asegurar permisos de ejecución
            if os.path.exists(driver_path):
                os.chmod(driver_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"❌ Error al iniciar Chrome: {str(e)}")
            print("\n💡 Verifica que Chrome esté instalado")
            return False

    def clean_phone(self, phone):
        """Limpia y formatea números de teléfono"""
        if not phone:
            return ""
        cleaned = re.sub(r'[^\d+]', '', phone)
        return cleaned

    def clean_text(self, text):
        """Limpia texto de espacios y caracteres extraños"""
        if not text:
            return ""
        return " ".join(text.split())

    def search_places(self, query, max_results=50, scroll_attempts=10):
        """
        Busca lugares en Google Maps

        Args:
            query: Término de búsqueda (ej: "clínica odontológica Medellín")
            max_results: Máximo número de resultados a extraer
            scroll_attempts: Intentos de scroll para cargar más resultados
        """
        print(f"\n🔍 Buscando: {query}")
        print(f"📊 Meta: {max_results} resultados")

        if not self.setup_driver():
            return []

        try:
            # Navegar a Google Maps
            search_url = f"{self.base_url}{query.replace(' ', '+')}"
            print(f"🌐 Navegando a Google Maps...")
            self.driver.get(search_url)

            # Esperar a que carguen los resultados
            print(f"⏳ Esperando resultados...")
            time.sleep(5)

            # Scroll para cargar más resultados
            print(f"📜 Cargando más resultados...")
            self._scroll_results(scroll_attempts)

            # Extraer datos
            print(f"📦 Extrayendo información...")
            self._extract_data(max_results)

            print(f"✅ Extraídos {len(self.results)} resultados")

        except Exception as e:
            print(f"❌ Error durante el scraping: {str(e)}")

        finally:
            if self.driver:
                self.driver.quit()

        return self.results

    def _scroll_results(self, attempts):
        """Hace scroll en el panel de resultados para cargar más lugares"""
        try:
            # Buscar el contenedor scrollable
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

            for i in range(attempts):
                # Scroll hasta el final
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight',
                    scrollable_div
                )
                time.sleep(2)

                # Verificar si llegamos al final
                try:
                    end_text = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Has llegado al final')]")
                    if end_text:
                        print(f"✓ Llegamos al final de los resultados")
                        break
                except NoSuchElementException:
                    pass

                print(f"  Scroll {i+1}/{attempts}", end='\r')

        except Exception as e:
            print(f"\n⚠ Error en scroll: {str(e)}")

    def _extract_data(self, max_results):
        """Extrae datos de los lugares en la lista"""
        try:
            # Obtener todos los enlaces de lugares
            place_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')

            count = 0
            for i, link in enumerate(place_links[:max_results]):
                if count >= max_results:
                    break

                try:
                    # Click en el lugar
                    self.driver.execute_script("arguments[0].click();", link)
                    time.sleep(3)

                    # Extraer información
                    place_data = self._extract_place_details()

                    if place_data and place_data.get('name'):
                        self.results.append(place_data)
                        count += 1
                        print(f"  ✓ {count}/{max_results}: {place_data['name'][:40]}...", end='\r')

                except Exception as e:
                    print(f"\n⚠ Error extrayendo lugar {i}: {str(e)}")
                    continue

        except Exception as e:
            print(f"\n❌ Error en extracción: {str(e)}")

    def _extract_place_details(self):
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
            'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            # Nombre - intentar múltiples selectores
            try:
                # Opción 1: h1 principal
                try:
                    name_elem = self.driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf')
                    data['name'] = self.clean_text(name_elem.text)
                except:
                    # Opción 2: cualquier h1
                    try:
                        name_elem = self.driver.find_element(By.CSS_SELECTOR, 'h1')
                        data['name'] = self.clean_text(name_elem.text)
                    except:
                        # Opción 3: aria-label del título
                        name_elem = self.driver.find_element(By.CSS_SELECTOR, '[role="main"] h1')
                        data['name'] = self.clean_text(name_elem.text)
            except Exception as e:
                print(f"\n⚠️ No se pudo extraer nombre: {str(e)}")
                pass

            # Rating
            try:
                rating_elem = self.driver.find_element(By.CSS_SELECTOR, 'div[role="img"][aria-label*="estrellas"]')
                aria_label = rating_elem.get_attribute('aria-label')
                rating_match = re.search(r'([\d,\.]+)\s*estrellas', aria_label)
                if rating_match:
                    data['rating'] = rating_match.group(1)
            except:
                pass

            # Número de reseñas
            try:
                reviews_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="reseña"]')
                aria_label = reviews_elem.get_attribute('aria-label')
                reviews_match = re.search(r'([\d\.]+)\s*reseña', aria_label)
                if reviews_match:
                    data['reviews_count'] = reviews_match.group(1)
            except:
                pass

            # Categoría
            try:
                category_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[jsaction*="category"]')
                data['category'] = self.clean_text(category_elem.text)
            except:
                pass

            # Dirección
            try:
                address_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="address"]')
                aria_label = address_elem.get_attribute('aria-label')
                if aria_label and 'Dirección:' in aria_label:
                    data['address'] = aria_label.replace('Dirección:', '').strip()
            except:
                pass

            # Teléfono
            try:
                phone_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[data-item-id*="phone"]')
                aria_label = phone_elem.get_attribute('aria-label')
                if aria_label:
                    phone_match = re.search(r'[\d\s\+\(\)\-]+', aria_label)
                    if phone_match:
                        data['phone'] = self.clean_phone(phone_match.group(0))
            except:
                pass

            # Sitio web
            try:
                website_elem = self.driver.find_element(By.CSS_SELECTOR, 'a[data-item-id="authority"]')
                data['website'] = website_elem.get_attribute('href')
            except:
                pass

            # Horarios
            try:
                hours_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[data-item-id*="oh"]')
                aria_label = hours_elem.get_attribute('aria-label')
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


def main():
    """Función principal de ejemplo"""
    scraper = GoogleMapsScraperSelenium(headless=False)

    # Ejemplo de búsqueda
    query = "clínica odontológica Medellín"

    results = scraper.search_places(
        query=query,
        max_results=20,
        scroll_attempts=5
    )

    # Mostrar resumen
    scraper.print_summary()

    # Guardar resultados
    if results:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        scraper.save_to_csv(f'pymes_{timestamp}.csv')
        scraper.save_to_excel(f'pymes_{timestamp}.xlsx')
        scraper.save_to_json(f'pymes_{timestamp}.json')


if __name__ == "__main__":
    main()
