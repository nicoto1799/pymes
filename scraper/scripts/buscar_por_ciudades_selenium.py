"""
Script para buscar en múltiples ciudades usando Selenium
Genera archivos separados por ciudad
"""

import time
from datetime import datetime
from gmaps_scraper_selenium import GoogleMapsScraperSelenium
import pandas as pd


# 🎯 CONFIGURACIÓN
# ================

# Tipo de negocio a buscar
TIPO_NEGOCIO = "clínica odontológica"  # Cambia según necesites

# Ciudades principales de Colombia
CIUDADES = [
    "Medellín",
    "Bogotá",
    "Cali",
    "Barranquilla",
    "Cartagena",
]

# Resultados por ciudad
MAX_RESULTADOS_POR_CIUDAD = 500

# Configuración de scroll (más scrolls = más resultados)
# Para 500 resultados necesitas entre 50-80 scrolls
SCROLL_ATTEMPTS = 60

# Pausa entre ciudades (segundos) - aumentado para evitar bloqueos
PAUSA_ENTRE_BUSQUEDAS = 10


def buscar_por_ciudades():
    """Busca el mismo tipo de negocio en múltiples ciudades"""

    print("="*70)
    print(f"🎯 BÚSQUEDA MULTI-CIUDAD: {TIPO_NEGOCIO.upper()}")
    print("="*70)
    print(f"\n📍 Ciudades: {', '.join(CIUDADES)}")
    print(f"📊 Resultados por ciudad: {MAX_RESULTADOS_POR_CIUDAD}")
    print(f"⏱️  Pausa entre búsquedas: {PAUSA_ENTRE_BUSQUEDAS}s\n")

    todos_los_resultados = []
    resumen_por_ciudad = []

    for i, ciudad in enumerate(CIUDADES, 1):
        print(f"\n{'='*70}")
        print(f"🔍 [{i}/{len(CIUDADES)}] Buscando en {ciudad}")
        print(f"{'='*70}")

        query = f"{TIPO_NEGOCIO} {ciudad}"

        try:
            # Crear scraper para cada ciudad
            scraper = GoogleMapsScraperSelenium(headless=True)

            results = scraper.search_places(
                query=query,
                max_results=MAX_RESULTADOS_POR_CIUDAD,
                scroll_attempts=SCROLL_ATTEMPTS
            )

            # Agregar ciudad a cada resultado
            for result in results:
                result['ciudad_busqueda'] = ciudad

            todos_los_resultados.extend(results)

            # Estadísticas
            with_phone = sum(1 for r in results if r.get('phone'))
            with_website = sum(1 for r in results if r.get('website'))

            resumen_por_ciudad.append({
                'ciudad': ciudad,
                'total': len(results),
                'con_telefono': with_phone,
                'con_website': with_website,
                'con_rating': sum(1 for r in results if r.get('rating')),
            })

            print(f"\n✅ {ciudad}: {len(results)} negocios encontrados")
            print(f"   📞 Con teléfono: {with_phone}")
            print(f"   🌐 Con website: {with_website}")

            # Guardar archivo individual por ciudad
            if results:
                timestamp = datetime.now().strftime('%Y%m%d')
                ciudad_safe = ciudad.replace(' ', '_')

                df_ciudad = pd.DataFrame(results)
                df_ciudad.to_csv(f'{ciudad_safe}_{timestamp}.csv', index=False, encoding='utf-8-sig')
                df_ciudad.to_excel(f'{ciudad_safe}_{timestamp}.xlsx', index=False)
                print(f"   💾 Guardado: {ciudad_safe}_{timestamp}.csv/.xlsx")

        except Exception as e:
            print(f"❌ Error en {ciudad}: {str(e)}")
            resumen_por_ciudad.append({
                'ciudad': ciudad,
                'total': 0,
                'con_telefono': 0,
                'con_website': 0,
                'con_rating': 0,
            })

        # Pausa entre búsquedas (excepto en la última)
        if i < len(CIUDADES):
            print(f"\n⏳ Pausa de {PAUSA_ENTRE_BUSQUEDAS}s antes de siguiente ciudad...")
            time.sleep(PAUSA_ENTRE_BUSQUEDAS)

    # ==========================
    # RESUMEN FINAL Y GUARDADO
    # ==========================

    print("\n" + "="*70)
    print("📊 RESUMEN GENERAL")
    print("="*70)

    # Tabla de resumen
    df_resumen = pd.DataFrame(resumen_por_ciudad)
    print("\n" + df_resumen.to_string(index=False))

    total_general = df_resumen['total'].sum()
    total_con_telefono = df_resumen['con_telefono'].sum()

    print(f"\n{'='*70}")
    print(f"TOTAL GENERAL: {total_general} negocios")
    if total_general > 0:
        print(f"Con teléfono: {total_con_telefono} ({total_con_telefono/total_general*100:.1f}%)")
    else:
        print(f"Con teléfono: 0 (0.0%)")
    print(f"{'='*70}")

    # Guardar archivo consolidado
    if todos_los_resultados:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Todos los resultados
        df_todos = pd.DataFrame(todos_los_resultados)
        df_todos.to_csv(f'CONSOLIDADO_todas_ciudades_{timestamp}.csv', index=False, encoding='utf-8-sig')
        df_todos.to_excel(f'CONSOLIDADO_todas_ciudades_{timestamp}.xlsx', index=False)
        print(f"\n💾 Archivo consolidado: CONSOLIDADO_todas_ciudades_{timestamp}.csv/.xlsx")

        # Solo con teléfono
        leads_telefono = [r for r in todos_los_resultados if r.get('phone')]
        if leads_telefono:
            df_leads = pd.DataFrame(leads_telefono)
            df_leads.to_csv(f'LEADS_con_telefono_{timestamp}.csv', index=False, encoding='utf-8-sig')
            df_leads.to_excel(f'LEADS_con_telefono_{timestamp}.xlsx', index=False)
            print(f"💾 Leads con teléfono: LEADS_con_telefono_{timestamp}.csv/.xlsx")

        # Resumen por ciudad
        df_resumen.to_csv(f'RESUMEN_por_ciudad_{timestamp}.csv', index=False, encoding='utf-8-sig')
        df_resumen.to_excel(f'RESUMEN_por_ciudad_{timestamp}.xlsx', index=False)
        print(f"💾 Resumen: RESUMEN_por_ciudad_{timestamp}.csv/.xlsx")

        print("\n✅ Proceso completado exitosamente!")

        # Siguiente paso
        print(f"\n{'='*70}")
        print("📋 PRÓXIMOS PASOS:")
        print("="*70)
        print("1. Abre el archivo 'LEADS_con_telefono_*.csv' o '.xlsx'")
        print("2. Filtra por ciudad de interés")
        print("3. Revisa manualmente los negocios (rating, reviews)")
        print("4. Prioriza los mejor calificados")
        print("5. Prepara mensaje personalizado por ciudad")
        print("6. Contacta 10-20 por día máximo")
        print("="*70)

    else:
        print("\n⚠️  No se encontraron resultados en ninguna ciudad.")


if __name__ == "__main__":
    buscar_por_ciudades()
