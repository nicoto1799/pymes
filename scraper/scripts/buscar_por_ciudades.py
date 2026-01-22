"""
Script avanzado para buscar en múltiples ciudades de Colombia
Genera archivos separados por ciudad
"""

import asyncio
from datetime import datetime
from gmaps_scraper import GoogleMapsScraper
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
    # Agrega más ciudades según necesites:
    # "Bucaramanga",
    # "Pereira",
    # "Manizales",
    # "Cúcuta",
    # "Ibagué",
]

# Resultados por ciudad
MAX_RESULTADOS_POR_CIUDAD = 30

# Pausa entre ciudades (segundos) - para no saturar
PAUSA_ENTRE_BUSQUEDAS = 8


async def buscar_por_ciudades():
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

        scraper = GoogleMapsScraper()

        query = f"{TIPO_NEGOCIO} {ciudad}"

        try:
            results = await scraper.search_places(
                query=query,
                max_results=MAX_RESULTADOS_POR_CIUDAD,
                scroll_attempts=10
            )

            # Agregar ciudad a cada resultado
            for result in scraper.results:
                result['ciudad_busqueda'] = ciudad

            todos_los_resultados.extend(scraper.results)

            # Estadísticas
            with_phone = sum(1 for r in scraper.results if r.get('phone'))
            with_website = sum(1 for r in scraper.results if r.get('website'))

            resumen_por_ciudad.append({
                'ciudad': ciudad,
                'total': len(scraper.results),
                'con_telefono': with_phone,
                'con_website': with_website,
                'con_rating': sum(1 for r in scraper.results if r.get('rating')),
            })

            print(f"\n✅ {ciudad}: {len(scraper.results)} negocios encontrados")
            print(f"   📞 Con teléfono: {with_phone}")
            print(f"   🌐 Con website: {with_website}")

            # Guardar archivo individual por ciudad
            if scraper.results:
                timestamp = datetime.now().strftime('%Y%m%d')
                ciudad_safe = ciudad.replace(' ', '_')
                scraper.save_to_csv(f'{ciudad_safe}_{timestamp}.csv')
                scraper.save_to_excel(f'{ciudad_safe}_{timestamp}.xlsx')

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
            await asyncio.sleep(PAUSA_ENTRE_BUSQUEDAS)

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
    print(f"Con teléfono: {total_con_telefono} ({total_con_telefono/total_general*100 if total_general > 0 else 0:.1f}%)")
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
        print("1. Abre el archivo 'LEADS_con_telefono_*.xlsx'")
        print("2. Filtra por ciudad de interés")
        print("3. Revisa manualmente los negocios (rating, reviews)")
        print("4. Prioriza los mejor calificados")
        print("5. Prepara mensaje personalizado por ciudad")
        print("6. Contacta 10-20 por día máximo")
        print("="*70)

    else:
        print("\n⚠️  No se encontraron resultados en ninguna ciudad.")


if __name__ == "__main__":
    asyncio.run(buscar_por_ciudades())
