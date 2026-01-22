"""
Google Maps Scraper TODO-EN-UNO
Extrae clínicas + reseñas + pain points en una sola pasada
Optimizado para rating 3.0-4.2 (clínicas con problemas identificables)
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
import os
import stat


# 🎯 CONFIGURACIÓN
# ================

TIPO_NEGOCIO = "clínica odontológica"

CIUDADES = [
    "Cali",
    "Barranquilla",
    "Cartagena"
]

# Filtros de rating - DESACTIVADO: traer TODOS los ratings
RATING_MIN = 0.0  # Sin filtro mínimo
RATING_MAX = 5.0  # Sin filtro máximo

# Cantidad - PRODUCCIÓN COMPLETA
MAX_RESULTADOS_POR_CIUDAD = 120  # Extracción completa
SCROLL_ATTEMPTS = 60  # Suficiente para 120 resultados

# Reseñas por clínica
MAX_REVIEWS_PER_PLACE = 25  # 25 reseñas por clínica

# Pausa entre búsquedas (segundos)
PAUSA_ENTRE_BUSQUEDAS = 10

# Modo navegador - OCULTO PARA PRODUCCIÓN
HEADLESS = True  # True = Modo oculto (mejor rendimiento)


# Pain points a detectar
PAIN_POINTS = {
    'atencion_telefonica': [
        'no contestan', 'no responden el teléfono', 'no contestan el telefono',
        'teléfono nunca contestan', 'telefono nunca contestan',
        'llamar y no contestan', 'llamo y no responden', 'nunca atienden llamadas',
        'imposible comunicarse por teléfono', 'imposible comunicarse por telefono'
    ],
    'demora_respuesta': [
        'demoran en responder', 'tardan mucho en responder', 'respuesta lenta',
        'no responden rápido', 'no responden rapido', 'demora respuesta',
        'tardan días en responder', 'tardan dias en responder'
    ],
    'dificultad_agendar': [
        'difícil agendar', 'dificil agendar', 'imposible agendar',
        'no hay citas', 'citas llenas', 'agenda llena',
        'difícil conseguir cita', 'dificil conseguir cita'
    ],
    'horarios_limitados': [
        'horarios limitados', 'poco horario', 'horario reducido',
        'cierran temprano', 'no atienden fines de semana',
        'horario inconveniente'
    ],
    'falta_seguimiento': [
        'no hacen seguimiento', 'falta seguimiento', 'no llaman para recordar',
        'olvidan las citas', 'no confirman cita'
    ],
    'informacion_precios': [
        'no informan precios', 'precios no claros', 'falta información de precios',
        'falta informacion de precios', 'no dicen cuánto cuesta', 'no dicen cuanto cuesta'
    ]
}


class GoogleMapsScraperCompleto:
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

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        try:
            driver_path = ChromeDriverManager().install()

            # Fix para Mac ARM
            if 'THIRD_PARTY' in driver_path or not driver_path.endswith('chromedriver'):
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
            return False

    def clean_phone(self, phone):
        """Limpia y formatea números de teléfono"""
        if not phone:
            return ""
        return re.sub(r'[^\d+]', '', phone)

    def clean_text(self, text):
        """Limpia texto de espacios y caracteres extraños"""
        if not text:
            return ""
        return " ".join(text.split())

    def analyze_reviews_for_pain_points(self, reviews):
        """Analiza reseñas y detecta pain points"""
        pain_points_found = {category: [] for category in PAIN_POINTS.keys()}

        for review in reviews:
            text = review.get('text', '').lower()

            for category, keywords in PAIN_POINTS.items():
                for keyword in keywords:
                    if keyword.lower() in text:
                        pain_points_found[category].append({
                            'keyword': keyword,
                            'review_text': review.get('text', '')[:200],
                            'rating': review.get('rating', 0)
                        })
                        break

        return pain_points_found

    def generate_pitch_message(self, place_name, pain_points):
        """Genera mensaje de venta personalizado basado en pain points"""

        # Contar pain points
        pain_counts = {k: len(v) for k, v in pain_points.items() if v}

        if not pain_counts:
            return "Hola! Vi su clínica en Google Maps. Ofrecemos chatbots de WhatsApp para automatizar atención 24/7 y agendamiento de citas. ¿Le interesa una demo de 15 min?"

        # Encontrar el pain point principal
        top_pain = max(pain_counts, key=pain_counts.get)
        top_count = pain_counts[top_pain]

        # Mensajes personalizados por pain point
        messages = {
            'atencion_telefonica': f"Hola! Revisé las reseñas de {place_name} y vi que {top_count} pacientes mencionan dificultad para contactarlos por teléfono. Tengo un chatbot que responde WhatsApp 24/7 automáticamente. ¿Te interesa una demo de 15 min?",

            'demora_respuesta': f"Hola! Vi que varios pacientes de {place_name} mencionan demoras en respuestas. Tengo un chatbot que responde instantáneamente en WhatsApp y agenda citas automáticamente. ¿Te sirve una demo rápida de 15 min?",

            'dificultad_agendar': f"Hola! Noté en las reseñas de {place_name} que {top_count} pacientes comentan dificultad para agendar citas. Tengo un sistema que automatiza el agendamiento por WhatsApp 24/7. ¿Te interesa verlo en 15 min?",

            'horarios_limitados': f"Hola! Vi que pacientes de {place_name} mencionan horarios limitados. Un chatbot podría atender consultas y agendar citas 24/7, incluso fuera de horario. ¿Te sirve una demo de 15 min?",

            'falta_seguimiento': f"Hola! Noté en reseñas de {place_name} que mencionan falta de seguimiento. Tengo un chatbot que envía recordatorios automáticos y confirma citas por WhatsApp. ¿Te interesa verlo en 15 min?",

            'informacion_precios': f"Hola! Vi que pacientes preguntan por info de precios en reseñas de {place_name}. Un chatbot puede responder precios y servicios automáticamente por WhatsApp. ¿Te sirve una demo de 15 min?"
        }

        return messages.get(top_pain, "Mensaje personalizado no disponible")

    def extract_reviews(self, max_reviews=25):
        """Extrae reseñas del lugar actual"""
        try:
            # NUEVA INTERFAZ: Buscar tab "Opiniones"
            try:
                # Buscar el tab que contiene "Opiniones" o "Reviews"
                reviews_tab = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Opiniones') or contains(., 'Reviews')]"))
                )
                # Usar execute_script es más confiable que click()
                self.driver.execute_script("arguments[0].click();", reviews_tab)
                time.sleep(3)
                print("    ✓ Clic en tab Opiniones")
            except Exception as e:
                print(f"  ⚠️  No se encontró tab de Opiniones: {str(e)}")
                # Intentar método antiguo como fallback
                try:
                    reviews_button = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label*='reseña'], button[aria-label*='reviews']"))
                    )
                    self.driver.execute_script("arguments[0].click();", reviews_button)
                    time.sleep(3)
                    print("    ✓ Clic en botón de reseñas (método antiguo)")
                except:
                    print(f"  ⚠️  No se pudo abrir sección de reseñas")
                    return []

            # Scroll para cargar más reseñas
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, "div[role='main']")
            last_height = 0
            attempts = 0
            max_scroll_attempts = 15

            while attempts < max_scroll_attempts:
                self.driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight);', scrollable_div)
                time.sleep(1)

                current_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, "div[data-review-id]"))
                if current_reviews >= max_reviews:
                    break

                new_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
                if new_height == last_height:
                    break

                last_height = new_height
                attempts += 1

            # Expandir reseñas con "Más"
            try:
                more_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='Más']")
                for btn in more_buttons[:5]:  # Solo expandir primeras 5
                    try:
                        btn.click()
                        time.sleep(0.3)
                    except:
                        pass
            except:
                pass

            # Extraer datos de reseñas
            reviews_data = []
            review_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-review-id]")

            for elem in review_elements[:max_reviews]:
                try:
                    review = {}

                    # Rating
                    try:
                        rating_elem = elem.find_element(By.CSS_SELECTOR, "span[role='img']")
                        aria_label = rating_elem.get_attribute('aria-label')
                        rating_match = re.search(r'(\d+)', aria_label)
                        if rating_match:
                            review['rating'] = int(rating_match.group(1))
                    except:
                        review['rating'] = 0

                    # Texto de la reseña
                    try:
                        text_elem = elem.find_element(By.CSS_SELECTOR, "span.wiI7pd")
                        review['text'] = self.clean_text(text_elem.text)
                    except:
                        review['text'] = ""

                    # Autor
                    try:
                        author_elem = elem.find_element(By.CSS_SELECTOR, "div.d4r55")
                        review['author'] = self.clean_text(author_elem.text)
                    except:
                        review['author'] = ""

                    # Fecha de la reseña
                    try:
                        # La fecha suele estar en un span con clase específica
                        date_elem = elem.find_element(By.CSS_SELECTOR, "span.rsqaWe")
                        review['date'] = self.clean_text(date_elem.text)
                    except:
                        # Intentar método alternativo
                        try:
                            # Buscar por aria-label que contiene "hace"
                            date_spans = elem.find_elements(By.TAG_NAME, "span")
                            for span in date_spans:
                                text = span.text.strip()
                                if 'hace' in text.lower() or 'ago' in text.lower() or 'mes' in text.lower() or 'semana' in text.lower() or 'día' in text.lower():
                                    review['date'] = text
                                    break
                            if 'date' not in review:
                                review['date'] = ""
                        except:
                            review['date'] = ""

                    if review['text']:
                        reviews_data.append(review)

                except Exception as e:
                    continue

            return reviews_data

        except Exception as e:
            print(f"  ❌ Error extrayendo reseñas: {str(e)}")
            return []

    def extract_place_with_reviews(self, link_element, ciudad):
        """Extrae datos del lugar + reseñas en una sola pasada"""
        try:
            # Click en el lugar
            self.driver.execute_script("arguments[0].click();", link_element)
            time.sleep(3)

            # Extraer datos básicos
            data = {
                'name': '',
                'rating': 0,
                'reviews_count': '',
                'category': '',
                'address': '',
                'phone': '',
                'website': '',
                'hours': '',
                'ciudad_busqueda': ciudad,
                'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'reviews': [],
                'pain_points': {},
                'total_pain_points': 0,
                'pain_point_principal': '',
                'mensaje_sugerido': '',
                'prioridad': 'Baja'
            }

            # Nombre - Extraer desde URL (más confiable)
            try:
                current_url = self.driver.current_url
                if '/maps/place/' in current_url:
                    # Extraer nombre de la URL
                    name_from_url = current_url.split('/maps/place/')[1].split('/')[0]
                    # Decodificar URL encoding
                    import urllib.parse
                    name_decoded = urllib.parse.unquote(name_from_url)
                    name_clean = name_decoded.replace('+', ' ').strip()
                    if name_clean and len(name_clean) > 2:
                        data['name'] = name_clean
            except:
                # Fallback: intentar desde h1
                try:
                    time.sleep(1)  # Pequeña pausa para que cargue
                    name_elem = self.driver.find_element(By.CSS_SELECTOR, 'h1')
                    name_text = self.clean_text(name_elem.text)
                    if name_text and name_text not in ['Resultados', 'Results', '']:
                        data['name'] = name_text
                except:
                    pass

            # Rating
            try:
                rating_elem = self.driver.find_element(By.CSS_SELECTOR, 'div[role="img"][aria-label*="estrellas"]')
                aria_label = rating_elem.get_attribute('aria-label')
                rating_match = re.search(r'([\d,\.]+)\s*estrellas', aria_label)
                if rating_match:
                    data['rating'] = float(rating_match.group(1).replace(',', '.'))
            except:
                pass

            # Filtrar por rating ANTES de continuar
            if data['rating'] < RATING_MIN or data['rating'] > RATING_MAX:
                return None

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

            # Solo continuar si tiene teléfono
            if not data['phone']:
                return None

            # EXTRAER RESEÑAS
            print(f"    📖 Extrayendo reseñas de {data['name'][:40]}...")
            reviews = self.extract_reviews(MAX_REVIEWS_PER_PLACE)
            data['reviews'] = reviews
            data['reviews_count_extracted'] = len(reviews)

            # ANALIZAR PAIN POINTS
            if reviews:
                pain_points = self.analyze_reviews_for_pain_points(reviews)
                data['pain_points'] = pain_points

                # Contar pain points
                pain_counts = {k: len(v) for k, v in pain_points.items() if v}
                data['total_pain_points'] = sum(pain_counts.values())

                # Pain point principal
                if pain_counts:
                    top_pain = max(pain_counts, key=pain_counts.get)
                    data['pain_point_principal'] = top_pain.replace('_', ' ').title()

                # Prioridad
                if data['total_pain_points'] >= 5:
                    data['prioridad'] = 'Alta'
                elif data['total_pain_points'] >= 2:
                    data['prioridad'] = 'Media'

                # Generar mensaje personalizado
                data['mensaje_sugerido'] = self.generate_pitch_message(data['name'], pain_points)

                print(f"    ✓ {len(reviews)} reseñas | {data['total_pain_points']} pain points | {data['prioridad']}")
            else:
                print(f"    ⚠️  Sin reseñas")

            return data

        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            return None

    def search_city(self, ciudad, max_results):
        """Busca y extrae clínicas de una ciudad"""
        print(f"\n{'='*70}")
        print(f"🔍 Buscando en {ciudad}")
        print(f"{'='*70}")

        query = f"{TIPO_NEGOCIO} {ciudad}"
        search_url = f"{self.base_url}{query.replace(' ', '+')}"

        print(f"🌐 Navegando a Google Maps...")
        self.driver.get(search_url)
        time.sleep(5)

        # Scroll para cargar más resultados
        print(f"📜 Cargando resultados (scroll {SCROLL_ATTEMPTS} veces)...")
        try:
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
            for i in range(SCROLL_ATTEMPTS):
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                time.sleep(1.5)

                if (i + 1) % 10 == 0:
                    print(f"  Scroll {i+1}/{SCROLL_ATTEMPTS}")
        except:
            print("  ⚠️  Error en scroll")

        # Obtener enlaces de lugares
        print(f"📦 Extrayendo lugares...")
        place_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')
        print(f"  Encontrados {len(place_links)} lugares")

        # Extraer datos de cada lugar
        city_results = []
        count = 0

        for i, link in enumerate(place_links):
            if count >= max_results:
                break

            try:
                place_data = self.extract_place_with_reviews(link, ciudad)

                if place_data:
                    city_results.append(place_data)
                    count += 1
                    print(f"  ✓ {count}/{max_results}: {place_data['name'][:40]} | Rating: {place_data['rating']} | Pain: {place_data['total_pain_points']}")
                else:
                    # Filtrado por rating o sin teléfono
                    pass

            except Exception as e:
                print(f"  ⚠️  Error en lugar {i}: {str(e)}")
                continue

        print(f"\n✅ {ciudad}: {len(city_results)} lugares extraídos (rating {RATING_MIN}-{RATING_MAX})")
        return city_results

    def run(self):
        """Ejecuta el scraper completo"""
        print(f"\n{'='*70}")
        print(f"🤖 SCRAPER TODO-EN-UNO: CLÍNICAS + RESEÑAS + PAIN POINTS")
        print(f"{'='*70}")
        print(f"\n📋 Configuración:")
        print(f"  • Tipo de negocio: {TIPO_NEGOCIO}")
        print(f"  • Ciudades: {', '.join(CIUDADES)}")
        print(f"  • Rating objetivo: {RATING_MIN} - {RATING_MAX}")
        print(f"  • Max por ciudad: {MAX_RESULTADOS_POR_CIUDAD}")
        print(f"  • Reseñas por lugar: {MAX_REVIEWS_PER_PLACE}")
        print(f"  • Navegador oculto: {HEADLESS}")

        if not self.setup_driver():
            return

        all_results = []

        try:
            for i, ciudad in enumerate(CIUDADES):
                print(f"\n[{i+1}/{len(CIUDADES)}] Procesando {ciudad}...")

                city_results = self.search_city(ciudad, MAX_RESULTADOS_POR_CIUDAD)
                all_results.extend(city_results)

                # Guardar archivo por ciudad
                if city_results:
                    timestamp = datetime.now().strftime('%Y%m%d')
                    city_file = f"{ciudad}_{timestamp}_con_reviews.xlsx"
                    df_city = pd.DataFrame(city_results)
                    df_city.to_excel(city_file, index=False)
                    print(f"  💾 Guardado: {city_file}")

                # Pausa entre ciudades
                if i < len(CIUDADES) - 1:
                    print(f"\n⏳ Pausa de {PAUSA_ENTRE_BUSQUEDAS}s antes de siguiente ciudad...")
                    time.sleep(PAUSA_ENTRE_BUSQUEDAS)

            self.results = all_results

        finally:
            if self.driver:
                self.driver.quit()

        return self.results

    def save_results(self, output_folder):
        """Guarda resultados organizados en carpeta"""
        if not self.results:
            print("\n⚠️  No hay resultados para guardar")
            return

        # Crear carpeta de salida
        os.makedirs(output_folder, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        print(f"\n{'='*70}")
        print(f"💾 GUARDANDO RESULTADOS EN: {output_folder}/")
        print(f"{'='*70}")

        # DataFrame completo
        df = pd.DataFrame(self.results)

        # 1. Archivo completo
        full_file = os.path.join(output_folder, f'TODOS_LOS_LEADS_{timestamp}.xlsx')
        df.to_excel(full_file, index=False)
        print(f"\n✅ Todos los leads: {full_file}")
        print(f"   ({len(df)} leads)")

        # 2. Alta prioridad (5+ pain points)
        df_high = df[df['total_pain_points'] >= 5]
        if not df_high.empty:
            high_file = os.path.join(output_folder, f'ALTA_PRIORIDAD_{timestamp}.xlsx')
            df_high.to_excel(high_file, index=False)
            print(f"\n✅ Alta prioridad: {high_file}")
            print(f"   ({len(df_high)} leads con 5+ pain points)")

        # 3. Media prioridad (2-4 pain points)
        df_medium = df[(df['total_pain_points'] >= 2) & (df['total_pain_points'] < 5)]
        if not df_medium.empty:
            medium_file = os.path.join(output_folder, f'MEDIA_PRIORIDAD_{timestamp}.xlsx')
            df_medium.to_excel(medium_file, index=False)
            print(f"\n✅ Media prioridad: {medium_file}")
            print(f"   ({len(df_medium)} leads con 2-4 pain points)")

        # 4. Por ciudad
        for ciudad in df['ciudad_busqueda'].unique():
            df_city = df[df['ciudad_busqueda'] == ciudad]
            city_file = os.path.join(output_folder, f'{ciudad}_{timestamp}.xlsx')
            df_city.to_excel(city_file, index=False)
            print(f"\n✅ {ciudad}: {city_file}")
            print(f"   ({len(df_city)} leads)")

        # 5. Resumen estadístico
        print(f"\n{'='*70}")
        print(f"📊 ESTADÍSTICAS FINALES")
        print(f"{'='*70}")
        print(f"\nTotal extraído: {len(df)} leads")
        print(f"Rating promedio: {df['rating'].mean():.2f}")
        print(f"Con reseñas: {len(df[df['reviews_count_extracted'] > 0])}")
        print(f"\nPrioridad:")
        print(f"  • Alta (5+ pain points): {len(df[df['prioridad'] == 'Alta'])}")
        print(f"  • Media (2-4 pain points): {len(df[df['prioridad'] == 'Media'])}")
        print(f"  • Baja (0-1 pain points): {len(df[df['prioridad'] == 'Baja'])}")

        print(f"\nPor ciudad:")
        for ciudad in df['ciudad_busqueda'].value_counts().items():
            print(f"  • {ciudad[0]}: {ciudad[1]} leads")

        print(f"\nPain points más comunes:")
        all_pain_counts = {
            'Atención Telefónica': sum(1 for r in self.results if r.get('pain_points', {}).get('atencion_telefonica')),
            'Demora Respuesta': sum(1 for r in self.results if r.get('pain_points', {}).get('demora_respuesta')),
            'Dificultad Agendar': sum(1 for r in self.results if r.get('pain_points', {}).get('dificultad_agendar')),
            'Horarios Limitados': sum(1 for r in self.results if r.get('pain_points', {}).get('horarios_limitados')),
            'Falta Seguimiento': sum(1 for r in self.results if r.get('pain_points', {}).get('falta_seguimiento')),
            'Info Precios': sum(1 for r in self.results if r.get('pain_points', {}).get('informacion_precios'))
        }

        for pain, count in sorted(all_pain_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"  • {pain}: {count} leads")

        print(f"\n{'='*70}")
        print(f"✅ Archivos guardados en: {output_folder}/")
        print(f"{'='*70}")


def main():
    """Función principal"""
    # Crear carpeta de resultados con timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    output_folder = f"resultados/extraccion_completa_{timestamp}"

    print(f"\n🎯 Carpeta de salida: {output_folder}/")

    # Crear y ejecutar scraper
    scraper = GoogleMapsScraperCompleto(headless=HEADLESS)
    results = scraper.run()

    # Guardar resultados organizados
    if results:
        scraper.save_results(output_folder)

        print(f"\n🎉 ¡Proceso completado!")
        print(f"\n📂 Revisa los archivos en: {output_folder}/")
        print(f"\n💡 Próximos pasos:")
        print(f"   1. Abre: {output_folder}/ALTA_PRIORIDAD_*.xlsx")
        print(f"   2. Revisa columna 'mensaje_sugerido'")
        print(f"   3. Personaliza y envía por WhatsApp")
        print(f"   4. Empieza con 10-15 contactos por día")
    else:
        print(f"\n⚠️  No se extrajeron resultados")


if __name__ == "__main__":
    main()
