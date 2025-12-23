"""
Google Maps Reviews Scraper
Extrae reseñas de Google Maps para identificar pain points de las clínicas
"""

import time
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
import json


class GoogleMapsReviewsScraper:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.reviews = []

    def setup_driver(self):
        """Configura el navegador Chrome con opciones anti-detección"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless=new')

        # Opciones para evitar detección
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
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

    def extract_reviews_from_place(self, place_name, place_url=None, max_reviews=50, city=None):
        """
        Extrae reseñas de un lugar específico

        Args:
            place_name: Nombre del lugar
            place_url: URL directa del lugar en Google Maps (opcional)
            max_reviews: Número máximo de reseñas a extraer
            city: Ciudad del lugar (opcional, mejora precisión de búsqueda)
        """
        print(f"\n{'='*70}")
        print(f"🔍 Extrayendo reseñas de: {place_name}")
        print(f"{'='*70}")

        if not self.driver:
            if not self.setup_driver():
                return []

        try:
            # Si no hay URL, buscar el lugar
            if not place_url:
                # Incluir ciudad en la búsqueda para mejor precisión
                search_query = f"{place_name}"
                if city:
                    search_query += f" {city}"
                search_query += " Google Maps"
                print(f"🔍 Buscando: {search_query}")
                self.driver.get(f"https://www.google.com/maps/search/{search_query}")
                time.sleep(3)

                # Hacer clic en el primer resultado
                try:
                    first_result = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/maps/place/']"))
                    )
                    first_result.click()
                    time.sleep(3)
                except:
                    print("⚠️  No se encontró el lugar")
                    return []
            else:
                print(f"🌐 Navegando a URL directa...")
                self.driver.get(place_url)
                time.sleep(3)

            # Hacer clic en el botón de reseñas
            try:
                # Buscar el botón que muestra el número de reseñas
                reviews_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label*='reseñas'], button[aria-label*='reviews']"))
                )
                reviews_count_text = reviews_button.get_attribute('aria-label')
                print(f"📊 Reseñas encontradas: {reviews_count_text}")

                # Click en el botón
                self.driver.execute_script("arguments[0].click();", reviews_button)
                time.sleep(2)

            except Exception as e:
                print(f"⚠️  No se pudo hacer clic en reseñas: {str(e)}")
                print("🔄 Intentando método alternativo...")

            # Scroll para cargar más reseñas
            print(f"📜 Cargando reseñas...")
            reviews_loaded = self._scroll_reviews(max_reviews)
            print(f"✅ {reviews_loaded} reseñas cargadas")

            # Extraer datos de las reseñas
            reviews_data = self._extract_reviews_data(place_name, max_reviews)

            print(f"✅ {len(reviews_data)} reseñas extraídas exitosamente")

            return reviews_data

        except Exception as e:
            print(f"❌ Error extrayendo reseñas: {str(e)}")
            return []

    def _scroll_reviews(self, max_reviews):
        """Hace scroll en el panel de reseñas para cargar más"""
        try:
            # Encontrar el contenedor scrollable de reseñas
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, "div[role='main']")

            last_height = 0
            attempts = 0
            max_attempts = 20  # Número máximo de scrolls

            while attempts < max_attempts:
                # Scroll down
                self.driver.execute_script(
                    'arguments[0].scrollTo(0, arguments[0].scrollHeight);',
                    scrollable_div
                )
                time.sleep(1.5)

                # Verificar si hay más reseñas
                current_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, "div[data-review-id]"))

                if current_reviews >= max_reviews:
                    print(f"  ✓ Alcanzado límite de {max_reviews} reseñas")
                    break

                # Verificar si llegamos al final
                new_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight",
                    scrollable_div
                )

                if new_height == last_height:
                    print(f"  ✓ Fin de reseñas alcanzado")
                    break

                last_height = new_height
                attempts += 1

                if attempts % 5 == 0:
                    print(f"  Scroll {attempts}/{max_attempts} - {current_reviews} reseñas cargadas...")

            return current_reviews

        except Exception as e:
            print(f"⚠️  Error en scroll: {str(e)}")
            return 0

    def _extract_reviews_data(self, place_name, max_reviews):
        """Extrae datos de todas las reseñas visibles"""
        reviews = []

        try:
            # Expandir todas las reseñas que tengan "Más" o "More"
            try:
                more_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='Más'], button[aria-label*='More']")
                print(f"  📖 Expandiendo {len(more_buttons)} reseñas...")
                for button in more_buttons[:max_reviews]:
                    try:
                        self.driver.execute_script("arguments[0].click();", button)
                        time.sleep(0.3)
                    except:
                        pass
            except:
                pass

            # Extraer cada reseña
            review_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-review-id]")

            print(f"  📝 Extrayendo datos de {min(len(review_elements), max_reviews)} reseñas...")

            for idx, review_elem in enumerate(review_elements[:max_reviews], 1):
                try:
                    # Nombre del reviewer
                    try:
                        reviewer = review_elem.find_element(By.CSS_SELECTOR, "div.d4r55").text
                    except:
                        reviewer = "Anónimo"

                    # Rating (estrellas)
                    try:
                        rating_elem = review_elem.find_element(By.CSS_SELECTOR, "span[role='img']")
                        rating_text = rating_elem.get_attribute('aria-label')
                        rating = float(re.search(r'(\d+)', rating_text).group(1))
                    except:
                        rating = None

                    # Fecha
                    try:
                        date = review_elem.find_element(By.CSS_SELECTOR, "span.rsqaWe").text
                    except:
                        date = "Desconocida"

                    # Texto de la reseña
                    try:
                        review_text = review_elem.find_element(By.CSS_SELECTOR, "span.wiI7pd").text
                    except:
                        review_text = ""

                    # Respuesta del propietario (si existe)
                    try:
                        owner_response = review_elem.find_element(By.CSS_SELECTOR, "div.wiI7pd").text
                    except:
                        owner_response = ""

                    reviews.append({
                        'place_name': place_name,
                        'reviewer': reviewer,
                        'rating': rating,
                        'date': date,
                        'review_text': review_text,
                        'owner_response': owner_response,
                        'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })

                    if idx % 10 == 0:
                        print(f"    ✓ {idx}/{min(len(review_elements), max_reviews)} reseñas procesadas...")

                except Exception as e:
                    print(f"    ⚠️  Error en reseña {idx}: {str(e)}")
                    continue

            return reviews

        except Exception as e:
            print(f"❌ Error extrayendo datos de reseñas: {str(e)}")
            return reviews

    def analyze_pain_points(self, reviews):
        """
        Analiza las reseñas para identificar pain points comunes
        que pueden resolverse con un chatbot
        """
        print(f"\n{'='*70}")
        print("🔍 ANÁLISIS DE PAIN POINTS")
        print(f"{'='*70}")

        pain_points = {
            'atencion_telefonica': [],
            'demora_respuesta': [],
            'dificultad_agendar': [],
            'horarios_limitados': [],
            'falta_seguimiento': [],
            'informacion_precios': [],
            'otros': []
        }

        # Keywords para detectar pain points
        keywords = {
            'atencion_telefonica': [
                'no contestan', 'no responden el teléfono', 'llamo y no contestan',
                'nunca contestan', 'teléfono ocupado', 'no atienden llamadas',
                'imposible comunicarse', 'no cogen el teléfono'
            ],
            'demora_respuesta': [
                'demoran en responder', 'tardan mucho', 'respuesta lenta',
                'muy demorados', 'esperé mucho', 'sin respuesta', 'no responden whatsapp',
                'demora whatsapp', 'tardan en contestar'
            ],
            'dificultad_agendar': [
                'difícil agendar', 'citas llenas', 'no hay citas', 'sin disponibilidad',
                'imposible conseguir cita', 'muy difícil sacar cita', 'agenda llena'
            ],
            'horarios_limitados': [
                'horarios cortos', 'cierran temprano', 'solo atienden', 'horario limitado',
                'no atienden fines de semana', 'horario reducido'
            ],
            'falta_seguimiento': [
                'no me llamaron', 'sin seguimiento', 'olvidan las citas',
                'no me recordaron', 'falta recordatorio', 'sin confirmación'
            ],
            'informacion_precios': [
                'no informan precios', 'sin precios', 'no dicen cuánto cuesta',
                'precios ocultos', 'no hay información de costos'
            ]
        }

        # Analizar cada reseña
        for review in reviews:
            text = review['review_text'].lower()
            rating = review.get('rating', 5)

            # Solo analizar reseñas negativas (1-3 estrellas)
            if rating and rating <= 3:
                matched = False
                for category, terms in keywords.items():
                    if any(term in text for term in terms):
                        pain_points[category].append({
                            'reviewer': review['reviewer'],
                            'rating': rating,
                            'text': review['review_text'][:200],  # Primeros 200 chars
                            'date': review['date']
                        })
                        matched = True

                if not matched and len(text) > 20:
                    pain_points['otros'].append({
                        'reviewer': review['reviewer'],
                        'rating': rating,
                        'text': review['review_text'][:200],
                        'date': review['date']
                    })

        # Mostrar resumen
        print(f"\n📊 Resumen de Pain Points:\n")
        total_issues = 0
        for category, issues in pain_points.items():
            if issues:
                count = len(issues)
                total_issues += count
                category_name = category.replace('_', ' ').title()
                print(f"  • {category_name}: {count} menciones")

        print(f"\n  Total de quejas identificadas: {total_issues}")

        return pain_points

    def generate_pitch_suggestions(self, pain_points):
        """Genera sugerencias de pitch basadas en los pain points"""
        suggestions = []

        pitch_templates = {
            'atencion_telefonica': (
                "Vi que algunos pacientes mencionan dificultad para comunicarse por teléfono. "
                "Nuestro chatbot puede responder automáticamente el 80% de consultas básicas 24/7, "
                "liberando su línea telefónica solo para casos que realmente necesiten atención humana."
            ),
            'demora_respuesta': (
                "Noté quejas sobre demoras en responder WhatsApp. "
                "El chatbot responde instantáneamente consultas frecuentes sobre servicios, precios y disponibilidad, "
                "mientras su equipo se enfoca en casos más complejos."
            ),
            'dificultad_agendar': (
                "Veo que hay quejas sobre dificultad para conseguir citas. "
                "Nuestro sistema permite agendar citas 24/7 automáticamente, "
                "mostrando disponibilidad en tiempo real y enviando confirmaciones."
            ),
            'horarios_limitados': (
                "Algunos pacientes mencionan horarios limitados de atención. "
                "El chatbot funciona 24/7, permitiendo que los pacientes agenden citas, "
                "consulten información y dejen mensajes incluso fuera de su horario."
            ),
            'falta_seguimiento': (
                "Noté menciones sobre falta de recordatorios. "
                "El chatbot puede enviar recordatorios automáticos de citas, "
                "confirmaciones y seguimientos post-tratamiento, reduciendo ausencias."
            ),
            'informacion_precios': (
                "Algunos pacientes preguntan sobre precios. "
                "El chatbot puede compartir listas de precios, paquetes y promociones "
                "automáticamente, convirtiendo consultas en citas agendadas."
            )
        }

        for category, issues in pain_points.items():
            if issues and category in pitch_templates:
                suggestions.append({
                    'pain_point': category.replace('_', ' ').title(),
                    'mentions': len(issues),
                    'suggested_pitch': pitch_templates[category]
                })

        return suggestions

    def save_to_excel(self, reviews, filename):
        """Guarda las reseñas en un archivo Excel"""
        df = pd.DataFrame(reviews)
        df.to_excel(filename, index=False)
        print(f"\n💾 Reseñas guardadas en: {filename}")

    def save_to_json(self, data, filename):
        """Guarda datos en formato JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 Datos guardados en: {filename}")

    def close(self):
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()


# Función de ayuda para procesar múltiples lugares
def extract_reviews_from_leads_file(leads_file, max_reviews_per_place=30, max_places=10):
    """
    Extrae reseñas de múltiples lugares desde un archivo CSV/Excel de leads

    Args:
        leads_file: Ruta al archivo de leads (CSV o Excel)
        max_reviews_per_place: Máximo de reseñas por lugar
        max_places: Máximo de lugares a procesar
    """
    print(f"📂 Cargando leads desde: {leads_file}")

    # Cargar el archivo
    if leads_file.endswith('.csv'):
        df = pd.read_csv(leads_file)
    else:
        df = pd.read_excel(leads_file)

    print(f"✅ {len(df)} leads cargados")

    # Filtrar solo los que tienen buen rating pero podrían mejorar (4.0-4.5)
    df_filtered = df[(df['rating'] >= 4.0) & (df['rating'] <= 4.5)].head(max_places)

    print(f"🎯 Procesando {len(df_filtered)} clínicas con rating 4.0-4.5")

    scraper = GoogleMapsReviewsScraper(headless=True)

    all_reviews = []
    all_pain_points = {}
    all_pitches = []

    for idx, row in df_filtered.iterrows():
        place_name = row['name']

        # Extraer reseñas
        reviews = scraper.extract_reviews_from_place(
            place_name=place_name,
            max_reviews=max_reviews_per_place
        )

        if reviews:
            all_reviews.extend(reviews)

            # Analizar pain points
            pain_points = scraper.analyze_pain_points(reviews)
            all_pain_points[place_name] = pain_points

            # Generar sugerencias de pitch
            pitches = scraper.generate_pitch_suggestions(pain_points)
            if pitches:
                all_pitches.append({
                    'place_name': place_name,
                    'rating': row['rating'],
                    'reviews_count': row.get('reviews_count', 0),
                    'phone': row.get('phone', ''),
                    'pitches': pitches
                })

        time.sleep(5)  # Pausa entre lugares

    # Guardar resultados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if all_reviews:
        scraper.save_to_excel(all_reviews, f'reviews_extraidas_{timestamp}.xlsx')

    if all_pain_points:
        scraper.save_to_json(all_pain_points, f'pain_points_{timestamp}.json')

    if all_pitches:
        df_pitches = pd.DataFrame(all_pitches)
        df_pitches.to_excel(f'pitch_suggestions_{timestamp}.xlsx', index=False)
        print(f"💾 Sugerencias de pitch guardadas en: pitch_suggestions_{timestamp}.xlsx")

    scraper.close()

    return all_reviews, all_pain_points, all_pitches


if __name__ == "__main__":
    # Ejemplo de uso
    print("="*70)
    print("🤖 Google Maps Reviews Scraper")
    print("="*70)

    # Opción 1: Extraer reseñas de un solo lugar
    scraper = GoogleMapsReviewsScraper(headless=False)

    place_name = "Clínica Odontológica Medellín"  # Cambia por el nombre que quieras
    reviews = scraper.extract_reviews_from_place(place_name, max_reviews=20)

    if reviews:
        # Analizar pain points
        pain_points = scraper.analyze_pain_points(reviews)

        # Generar sugerencias de pitch
        pitches = scraper.generate_pitch_suggestions(pain_points)

        print(f"\n{'='*70}")
        print("💡 SUGERENCIAS DE PITCH")
        print(f"{'='*70}\n")
        for pitch in pitches:
            print(f"📌 {pitch['pain_point']} ({pitch['mentions']} menciones):")
            print(f"   {pitch['suggested_pitch']}\n")

        # Guardar
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        scraper.save_to_excel(reviews, f'reviews_{timestamp}.xlsx')
        scraper.save_to_json({'pain_points': pain_points, 'pitches': pitches}, f'analysis_{timestamp}.json')

    scraper.close()
