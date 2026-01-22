"""
Procesamiento masivo de leads con extracción de reseñas y análisis de pain points
Genera archivo final con mensajes personalizados para cada lead
"""

import pandas as pd
import time
from datetime import datetime
from gmaps_reviews_scraper import GoogleMapsReviewsScraper


# 🎯 CONFIGURACIÓN
# ================

# Archivo de entrada (tus leads)
LEADS_FILE = "LEADS_con_telefono_20251222_162340.xlsx"

# Filtros para seleccionar leads a procesar
FILTROS = {
    'ciudad': None,  # None = todas las ciudades, o "Medellín", "Bogotá", etc
    'rating_min': 3.5,  # Rating mínimo
    'rating_max': 4.5,  # Rating máximo (4.0-4.5 = pueden mejorar)
    'reviews_min': 0,  # Mínimo de reseñas (0 = sin filtro)
}

# Cantidad de leads a procesar
MAX_LEADS = 100  # Cambia según cuántos quieras procesar (100 = ~8 horas)

# Reseñas por lead
MAX_REVIEWS_PER_LEAD = 30  # 30 reseñas por clínica

# Modo de navegador
HEADLESS = True  # True = oculto (más rápido), False = visible (para debug)

# Pausa entre leads (segundos)
PAUSE_BETWEEN_LEADS = 8  # Pausa para evitar bloqueos de Google


def load_and_filter_leads(leads_file, filtros, max_leads):
    """Carga y filtra los leads según criterios"""
    print("="*70)
    print("📂 CARGANDO Y FILTRANDO LEADS")
    print("="*70)

    # Cargar archivo
    print(f"\n📁 Archivo: {leads_file}")
    df = pd.read_excel(leads_file)
    print(f"✅ {len(df)} leads cargados")

    # Aplicar filtros
    df_filtered = df.copy()

    # Filtro por ciudad
    if filtros['ciudad']:
        df_filtered = df_filtered[df_filtered['ciudad_busqueda'] == filtros['ciudad']]
        print(f"📍 Filtrado por ciudad '{filtros['ciudad']}': {len(df_filtered)} leads")

    # Filtro por rating
    df_filtered = df_filtered[
        (df_filtered['rating'] >= filtros['rating_min']) &
        (df_filtered['rating'] <= filtros['rating_max'])
    ]
    print(f"⭐ Filtrado por rating {filtros['rating_min']}-{filtros['rating_max']}: {len(df_filtered)} leads")

    # Filtro por mínimo de reseñas (solo si reviews_min > 0 y la columna existe)
    if filtros['reviews_min'] > 0 and 'reviews_count' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['reviews_count'] >= filtros['reviews_min']]
        print(f"📊 Filtrado por mín {filtros['reviews_min']} reseñas: {len(df_filtered)} leads")

    # Ordenar por rating (mejor primero)
    df_filtered = df_filtered.sort_values('rating', ascending=False)

    # Limitar cantidad
    df_filtered = df_filtered.head(max_leads)

    print(f"\n🎯 TOTAL A PROCESAR: {len(df_filtered)} leads")
    print("\n📋 Muestra:")
    print(df_filtered[['name', 'ciudad_busqueda', 'rating', 'reviews_count', 'phone']].head(10).to_string(index=False))

    return df_filtered


def process_leads_batch(df_leads, max_reviews_per_lead, headless, pause):
    """Procesa un lote de leads extrayendo reseñas y analizando pain points"""
    print("\n" + "="*70)
    print("🚀 INICIANDO PROCESAMIENTO MASIVO")
    print("="*70)

    total = len(df_leads)
    print(f"\n📊 Procesando {total} leads")
    print(f"⏱️  Tiempo estimado: {total * 3} - {total * 5} minutos")
    print(f"🕐 Inicio: {datetime.now().strftime('%H:%M:%S')}\n")

    # Crear scraper
    scraper = GoogleMapsReviewsScraper(headless=headless)

    # Resultados
    results = []
    failed = []

    for idx, row in df_leads.iterrows():
        lead_num = len(results) + len(failed) + 1
        print(f"\n{'='*70}")
        print(f"🔍 [{lead_num}/{total}] {row['name']}")
        print(f"{'='*70}")
        print(f"📍 {row['ciudad_busqueda']} | ⭐ {row['rating']} | 📊 {row.get('reviews_count', '?')} reseñas")

        try:
            # Extraer reseñas
            reviews = scraper.extract_reviews_from_place(
                place_name=row['name'],
                city=row.get('ciudad_busqueda', ''),
                max_reviews=max_reviews_per_lead
            )

            if not reviews:
                print("⚠️  No se pudieron extraer reseñas")
                failed.append({
                    'name': row['name'],
                    'reason': 'No reviews extracted'
                })
                continue

            # Analizar pain points
            pain_points = scraper.analyze_pain_points(reviews)

            # Contar pain points por categoría
            pain_counts = {k: len(v) for k, v in pain_points.items() if v}
            total_pain_points = sum(pain_counts.values())

            # Generar sugerencias de pitch
            pitches = scraper.generate_pitch_suggestions(pain_points)

            # Determinar el pain point principal
            top_pain_point = ""
            top_pain_count = 0
            suggested_message = ""

            if pain_counts:
                top_pain_point = max(pain_counts, key=pain_counts.get)
                top_pain_count = pain_counts[top_pain_point]

            if pitches:
                suggested_message = pitches[0]['suggested_pitch']

            # Guardar resultado
            result = {
                # Datos originales
                'nombre': row['name'],
                'ciudad': row['ciudad_busqueda'],
                'telefono': row['phone'],
                'rating': row['rating'],
                'reviews_count': row.get('reviews_count', 0),
                'direccion': row.get('address', ''),
                'website': row.get('website', ''),

                # Análisis de reseñas
                'reviews_analizadas': len(reviews),
                'total_pain_points': total_pain_points,
                'pain_atencion_telefonica': pain_counts.get('atencion_telefonica', 0),
                'pain_demora_respuesta': pain_counts.get('demora_respuesta', 0),
                'pain_dificultad_agendar': pain_counts.get('dificultad_agendar', 0),
                'pain_horarios_limitados': pain_counts.get('horarios_limitados', 0),
                'pain_falta_seguimiento': pain_counts.get('falta_seguimiento', 0),
                'pain_info_precios': pain_counts.get('informacion_precios', 0),

                # Priorización
                'pain_point_principal': top_pain_point.replace('_', ' ').title(),
                'menciones_principal': top_pain_count,
                'prioridad': 'Alta' if total_pain_points >= 5 else 'Media' if total_pain_points >= 2 else 'Baja',

                # Pitch personalizado
                'mensaje_sugerido': suggested_message,

                # Metadata
                'fecha_analisis': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            results.append(result)

            # Mostrar resumen
            print(f"\n✅ Análisis completado:")
            print(f"   • Reseñas analizadas: {len(reviews)}")
            print(f"   • Pain points encontrados: {total_pain_points}")
            if top_pain_point:
                print(f"   • Problema principal: {top_pain_point.replace('_', ' ').title()} ({top_pain_count} menciones)")
            print(f"   • Prioridad: {result['prioridad']}")

            # Progreso
            progress = (lead_num / total) * 100
            remaining = total - lead_num
            print(f"\n📊 Progreso: {lead_num}/{total} ({progress:.1f}%) - Quedan {remaining}")

        except Exception as e:
            print(f"\n❌ Error procesando {row['name']}: {str(e)}")
            failed.append({
                'name': row['name'],
                'reason': str(e)
            })

        # Pausa entre leads
        if lead_num < total:
            print(f"\n⏳ Pausa de {pause}s antes del siguiente...")
            time.sleep(pause)

    # Cerrar scraper
    scraper.close()

    return results, failed


def save_results(results, failed):
    """Guarda los resultados en archivos Excel"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    print("\n" + "="*70)
    print("💾 GUARDANDO RESULTADOS")
    print("="*70)

    if results:
        # Crear DataFrame
        df_results = pd.DataFrame(results)

        # Archivo completo
        filename_full = f'leads_con_analisis_{timestamp}.xlsx'
        df_results.to_excel(filename_full, index=False)
        print(f"\n✅ Archivo completo: {filename_full}")
        print(f"   ({len(results)} leads procesados)")

        # Archivo solo alta prioridad
        df_high_priority = df_results[df_results['prioridad'] == 'Alta']
        if not df_high_priority.empty:
            filename_priority = f'leads_ALTA_PRIORIDAD_{timestamp}.xlsx'
            df_high_priority.to_excel(filename_priority, index=False)
            print(f"\n✅ Alta prioridad: {filename_priority}")
            print(f"   ({len(df_high_priority)} leads con 5+ pain points)")

        # Archivo por pain point
        pain_categories = ['atencion_telefonica', 'demora_respuesta', 'dificultad_agendar']
        for category in pain_categories:
            col_name = f'pain_{category}'
            df_category = df_results[df_results[col_name] > 0].sort_values(col_name, ascending=False)
            if not df_category.empty:
                cat_name = category.replace('_', ' ').title()
                filename_cat = f'leads_pain_{category}_{timestamp}.xlsx'
                df_category.to_excel(filename_cat, index=False)
                print(f"\n✅ Pain: {cat_name}: {filename_cat}")
                print(f"   ({len(df_category)} leads)")

        # Estadísticas
        print("\n" + "="*70)
        print("📊 ESTADÍSTICAS")
        print("="*70)
        print(f"\nTotal procesado: {len(results)}")
        print(f"Alta prioridad (5+ pain points): {len(df_results[df_results['prioridad'] == 'Alta'])}")
        print(f"Media prioridad (2-4 pain points): {len(df_results[df_results['prioridad'] == 'Media'])}")
        print(f"Baja prioridad (0-1 pain points): {len(df_results[df_results['prioridad'] == 'Baja'])}")

        print("\nPain points más comunes:")
        for col in ['pain_atencion_telefonica', 'pain_demora_respuesta', 'pain_dificultad_agendar',
                    'pain_horarios_limitados', 'pain_falta_seguimiento', 'pain_info_precios']:
            total = df_results[col].sum()
            if total > 0:
                name = col.replace('pain_', '').replace('_', ' ').title()
                print(f"  • {name}: {int(total)} menciones")

        print("\nTop 10 leads con más pain points:")
        top10 = df_results.nlargest(10, 'total_pain_points')[['nombre', 'ciudad', 'total_pain_points', 'pain_point_principal', 'prioridad']]
        print(top10.to_string(index=False))

    if failed:
        df_failed = pd.DataFrame(failed)
        filename_failed = f'leads_fallidos_{timestamp}.xlsx'
        df_failed.to_excel(filename_failed, index=False)
        print(f"\n⚠️  Leads fallidos: {filename_failed}")
        print(f"   ({len(failed)} leads)")

    return timestamp


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🤖 PROCESAMIENTO MASIVO DE LEADS")
    print("="*70)
    print("\n📋 Configuración:")
    print(f"  • Archivo: {LEADS_FILE}")
    print(f"  • Ciudad: {FILTROS['ciudad'] or 'Todas'}")
    print(f"  • Rating: {FILTROS['rating_min']} - {FILTROS['rating_max']}")
    print(f"  • Min reviews: {FILTROS['reviews_min']}")
    print(f"  • Max leads: {MAX_LEADS}")
    print(f"  • Reviews por lead: {MAX_REVIEWS_PER_LEAD}")
    print(f"  • Navegador oculto: {HEADLESS}")

    # Auto-continuar (sin confirmación)
    print("\n" + "="*70)
    print("✅ Iniciando procesamiento automático...")
    # response = input("¿Continuar con este procesamiento? (si/no): ").strip().lower()
    # if response != 'si':
    #     print("\n❌ Proceso cancelado")
    #     return

    # Cargar y filtrar leads
    df_leads = load_and_filter_leads(LEADS_FILE, FILTROS, MAX_LEADS)

    if df_leads.empty:
        print("\n❌ No hay leads que procesar con estos filtros")
        return

    # Auto-continuar (sin confirmación)
    print("\n" + "="*70)
    tiempo_estimado_min = len(df_leads) * 3
    tiempo_estimado_max = len(df_leads) * 5
    print(f"⏱️  Tiempo estimado: {tiempo_estimado_min}-{tiempo_estimado_max} minutos")
    print(f"🕐 Hora de inicio: {datetime.now().strftime('%H:%M:%S')}")
    print(f"\n🚀 Iniciando procesamiento de {len(df_leads)} leads...")
    # response2 = input(f"\n¿Iniciar procesamiento de {len(df_leads)} leads? (si/no): ").strip().lower()
    # if response2 != 'si':
    #     print("\n❌ Proceso cancelado")
    #     return

    # Procesar
    start_time = time.time()
    results, failed = process_leads_batch(
        df_leads,
        MAX_REVIEWS_PER_LEAD,
        HEADLESS,
        PAUSE_BETWEEN_LEADS
    )

    # Guardar resultados
    timestamp = save_results(results, failed)

    # Resumen final
    elapsed_time = (time.time() - start_time) / 60
    print("\n" + "="*70)
    print("🎉 PROCESO COMPLETADO")
    print("="*70)
    print(f"\n⏱️  Tiempo total: {elapsed_time:.1f} minutos")
    print(f"✅ Exitosos: {len(results)}")
    print(f"❌ Fallidos: {len(failed)}")
    print(f"\n📁 Archivos generados en la carpeta actual")
    print(f"📅 Timestamp: {timestamp}")

    print("\n" + "="*70)
    print("📋 PRÓXIMOS PASOS:")
    print("="*70)
    print("\n1. Abre: leads_ALTA_PRIORIDAD_*.xlsx")
    print("2. Estos leads tienen 5+ quejas identificadas")
    print("3. Revisa la columna 'mensaje_sugerido'")
    print("4. Personaliza y envía por WhatsApp")
    print("5. Empieza con 10-15 por día")
    print("\n✅ ¡Listo para prospectar!")


if __name__ == "__main__":
    main()
