"""
CALCULADORA IMPUESTO DE RENTA AÑO GRAVABLE 2024
Personas Naturales Residentes Fiscales - Colombia
Basado en: Estatuto Tributario Colombiano - Ley 2277 de 2022 - Decreto 1625 de 2016
"""

def calcular_cesantias_exentas(cesantias, ingreso_promedio_mensual, uvt_2024):
    """
    Calcula las cesantías exentas según Art. 206 numeral 4 del ET
    
    Tabla de exención según ingreso mensual promedio de los últimos 6 meses:
    - Hasta 350 UVT: 100% exento (totalidad de cesantías)
    - 350 - 410 UVT: 90% exento
    - 410 - 470 UVT: 80% exento
    - 470 - 530 UVT: 60% exento
    - 530 - 590 UVT: 40% exento
    - 590 - 650 UVT: 20% exento
    - Más de 650 UVT: 0% exento (ninguna exención)
    """
    # Si no hay cesantías, retornar 0
    if cesantias == 0:
        return 0
    
    # Si no hay ingreso promedio, no se pueden calcular cesantías exentas
    if ingreso_promedio_mensual == 0:
        return 0
    
    # Calcular ingreso en UVT
    ingreso_uvt = ingreso_promedio_mensual / uvt_2024
    
    # Aplicar tabla del Art. 206 numeral 4
    if ingreso_uvt <= 350:
        # 100% de las cesantías son exentas
        return cesantias
    elif ingreso_uvt <= 410:
        # 90% de las cesantías son exentas
        return cesantias * 0.90
    elif ingreso_uvt <= 470:
        # 80% de las cesantías son exentas
        return cesantias * 0.80
    elif ingreso_uvt <= 530:
        # 60% de las cesantías son exentas
        return cesantias * 0.60
    elif ingreso_uvt <= 590:
        # 40% de las cesantías son exentas
        return cesantias * 0.40
    elif ingreso_uvt <= 650:
        # 20% de las cesantías son exentas
        return cesantias * 0.20
    else:
        # Más de 650 UVT: ninguna exención
        return 0


def aplicar_tabla_articulo_241(base_gravable_uvt, uvt_2024):
    """
    Aplica la tabla del artículo 241 del ET para calcular el impuesto
    """
    if base_gravable_uvt <= 1090:
        return 0
    elif base_gravable_uvt <= 1700:
        return (base_gravable_uvt - 1090) * 0.19 * uvt_2024
    elif base_gravable_uvt <= 4100:
        return ((base_gravable_uvt - 1700) * 0.28 + 116) * uvt_2024
    elif base_gravable_uvt <= 8670:
        return ((base_gravable_uvt - 4100) * 0.33 + 788) * uvt_2024
    elif base_gravable_uvt <= 18970:
        return ((base_gravable_uvt - 8670) * 0.35 + 2296) * uvt_2024
    elif base_gravable_uvt <= 31000:
        return ((base_gravable_uvt - 18970) * 0.37 + 5901) * uvt_2024
    else:
        return ((base_gravable_uvt - 31000) * 0.39 + 10352) * uvt_2024


def calcular_anticipo(impuesto_neto_actual, impuesto_neto_anterior, 
                     retenciones, num_anos_declarando):
    """
    Calcula el anticipo del año siguiente según Art. 807 del ET
    Compara método 1 y método 2, retorna el menor
    """
    # Determinar porcentaje según años declarando
    if num_anos_declarando == 1:
        porcentaje = 0.25
    elif num_anos_declarando == 2:
        porcentaje = 0.50
    else:
        porcentaje = 0.75
    
    # MÉTODO 1
    anticipo_metodo1 = (impuesto_neto_actual * porcentaje) - retenciones
    anticipo_metodo1 = max(anticipo_metodo1, 0)
    
    # MÉTODO 2
    if impuesto_neto_anterior > 0:
        promedio = (impuesto_neto_actual + impuesto_neto_anterior) / 2
        anticipo_metodo2 = (promedio * porcentaje) - retenciones
        anticipo_metodo2 = max(anticipo_metodo2, 0)
    else:
        anticipo_metodo2 = anticipo_metodo1
    
    # Retornar el menor
    anticipo_definitivo = min(anticipo_metodo1, anticipo_metodo2)
    
    return anticipo_metodo1, anticipo_metodo2, anticipo_definitivo


def formatear_moneda(valor):
    """Formatea valores en pesos colombianos"""
    return f"${valor:,.0f}".replace(",", ".")


def capturar_datos():
    """Captura los 19 datos de entrada del usuario"""
    print("\n" + "="*70)
    print(" " * 10 + "CALCULADORA IMPUESTO DE RENTA AÑO GRAVABLE 2024")
    print(" " * 15 + "Personas Naturales Residentes - Colombia")
    print("="*70)
    
    datos = {}
    
    # INFORMACIÓN DEL CONTRIBUYENTE
    print("\n--- INFORMACIÓN DEL CONTRIBUYENTE ---")
    datos['nombre'] = input("Nombres y Apellidos: ")
    datos['nit'] = input("NIT / Cédula: ")
    
    # INGRESOS LABORALES
    print("\n--- INGRESOS LABORALES ---")
    datos['salarios'] = float(input("Salarios: $") or 0)
    datos['cesantias'] = float(input("Cesantías Pagadas o Consignadas: $") or 0)
    datos['prestaciones_sociales'] = float(input("Prestaciones Sociales: $") or 0)
    datos['otros_pagos_laborales'] = float(input("Otros Pagos Laborales: $") or 0)
    datos['ingreso_mensual_promedio'] = float(input("Ingreso Mensual Promedio (últimos 6 meses): $") or 0)
    
    # INGRESOS NO CONSTITUTIVOS DE RENTA
    print("\n--- INGRESOS NO CONSTITUTIVOS DE RENTA (INCR) ---")
    datos['incr_salud'] = float(input("INCR Salud: $") or 0)
    datos['incr_pensiones'] = float(input("INCR Pensiones: $") or 0)
    
    # RENTAS EXENTAS
    print("\n--- RENTAS EXENTAS ---")
    datos['pension_voluntaria'] = float(input("Pensión Voluntaria: $") or 0)
    datos['afc'] = float(input("Cuentas AFC: $") or 0)
    
    # DEDUCCIONES
    print("\n--- DEDUCCIONES ---")
    datos['num_dependientes'] = int(input("Número de Dependientes: ") or 0)
    datos['intereses_vivienda'] = float(input("Intereses de Vivienda: $") or 0)
    datos['medicina_prepagada'] = float(input("Medicina Prepagada: $") or 0)
    
    # OTROS BENEFICIOS
    print("\n--- OTROS BENEFICIOS TRIBUTARIOS ---")
    datos['compras_factura_electronica'] = float(input("Compras con Factura Electrónica: $") or 0)
    datos['gmf'] = float(input("GMF (Gravamen Movimientos Financieros): $") or 0)
    
    # INFORMACIÓN AÑO ANTERIOR
    print("\n--- INFORMACIÓN AÑO ANTERIOR Y RETENCIONES ---")
    datos['impuesto_neto_anterior'] = float(input("Impuesto Neto Año Anterior: $") or 0)
    datos['saldo_favor_anterior'] = float(input("Saldo a Favor Año Anterior (sin solicitud): $") or 0)
    datos['retenciones'] = float(input("Retenciones Practicadas: $") or 0)
    datos['anticipo_anterior'] = float(input("Anticipo Año Anterior: $") or 0)
    datos['num_anos_declarando'] = int(input("Número de Años Declarando (1, 2, o 3+): ") or 1)
    
    return datos


def calcular_impuesto_renta(datos):
    """
    Realiza el cálculo completo del impuesto de renta
    según el Estatuto Tributario Colombiano - Art. 336
    """
    UVT_2024 = 47065
    
    resultados = {}
    
    # 1. INGRESOS TOTALES
    ingresos_totales = (datos['salarios'] + datos['cesantias'] + 
                       datos['prestaciones_sociales'] + datos['otros_pagos_laborales'])
    resultados['ingresos_totales'] = ingresos_totales
    
    # 2. INGRESOS NO CONSTITUTIVOS DE RENTA (INCR)
    incr_total = datos['incr_salud'] + datos['incr_pensiones']
    resultados['incr_total'] = incr_total
    
    # 3. INGRESO NETO
    ingreso_neto = ingresos_totales - incr_total
    resultados['ingreso_neto'] = ingreso_neto
    
    # 4. CESANTÍAS EXENTAS (Art. 206 numeral 4)
    cesantias_exentas = calcular_cesantias_exentas(
        datos['cesantias'], 
        datos['ingreso_mensual_promedio'], 
        UVT_2024
    )
    resultados['cesantias_exentas'] = cesantias_exentas
    
    # 5. DEDUCCIONES
    # Dependientes (máximo 384 UVT)
    limite_384_uvt = 384 * UVT_2024
    deduccion_dependientes = min(datos['num_dependientes'] * (32 * UVT_2024), limite_384_uvt)
    
    # Medicina prepagada (máximo 192 UVT)
    limite_192_uvt = 192 * UVT_2024
    deduccion_medicina = min(datos['medicina_prepagada'], limite_192_uvt)
    
    # Intereses vivienda (máximo 1,200 UVT)
    limite_1200_uvt = 1200 * UVT_2024
    deduccion_intereses = min(datos['intereses_vivienda'], limite_1200_uvt)
    
    deducciones_totales = deduccion_dependientes + deduccion_medicina + deduccion_intereses
    resultados['deduccion_dependientes'] = deduccion_dependientes
    resultados['deduccion_medicina'] = deduccion_medicina
    resultados['deduccion_intereses'] = deduccion_intereses
    resultados['deducciones_totales'] = deducciones_totales
    
    # 6. RENTA EXENTA 25%
    # Fórmula: (Ingresos Totales - INCR - Cesantías Exentas - Deducciones) * 25%
    # Limitada a 790 UVT
    base_renta_exenta_25 = ingresos_totales - incr_total - cesantias_exentas - deducciones_totales
    base_renta_exenta_25 = max(base_renta_exenta_25, 0)  # No puede ser negativa
    renta_exenta_25_calculada = base_renta_exenta_25 * 0.25
    limite_790_uvt = 790 * UVT_2024
    renta_exenta_25 = min(renta_exenta_25_calculada, limite_790_uvt)
    resultados['base_renta_exenta_25'] = base_renta_exenta_25
    
    # 7. OTRAS RENTAS EXENTAS
    # Pensión voluntaria + AFC (máximo 30% ingreso total o 3,800 UVT)
    total_pension_afc = datos['pension_voluntaria'] + datos['afc']
    limite_30_porciento = ingresos_totales * 0.30
    limite_3800_uvt = 3800 * UVT_2024
    pension_afc_limitada = min(total_pension_afc, limite_30_porciento, limite_3800_uvt)
    
    rentas_exentas_totales = cesantias_exentas + renta_exenta_25 + pension_afc_limitada
    resultados['renta_exenta_25'] = renta_exenta_25
    resultados['pension_afc_limitada'] = pension_afc_limitada
    resultados['rentas_exentas_totales'] = rentas_exentas_totales
    
    # 8. LÍMITE DEL 40% - ARTÍCULO 336
    suma_rentas_deducciones = rentas_exentas_totales + deducciones_totales
    limite_40_porciento = ingreso_neto * 0.40
    limite_1340_uvt = 1340 * UVT_2024
    limite_maximo_depuracion = min(limite_40_porciento, limite_1340_uvt)
    
    depuracion_final = min(suma_rentas_deducciones, limite_maximo_depuracion)
    resultados['suma_rentas_deducciones'] = suma_rentas_deducciones
    resultados['limite_maximo_depuracion'] = limite_maximo_depuracion
    resultados['depuracion_final'] = depuracion_final
    
    # 9. RENTA LÍQUIDA ANTES DE OTROS BENEFICIOS
    renta_liquida = ingreso_neto - depuracion_final
    
    # 10. BENEFICIO COMPRAS CON FACTURA ELECTRÓNICA (1% hasta 240 UVT)
    limite_240_uvt = 240 * UVT_2024
    beneficio_factura = min(datos['compras_factura_electronica'] * 0.01, limite_240_uvt)
    renta_liquida -= beneficio_factura
    resultados['beneficio_factura'] = beneficio_factura
    
    # 11. BENEFICIO GMF (50%)
    beneficio_gmf = datos['gmf'] * 0.50
    renta_liquida -= beneficio_gmf
    resultados['beneficio_gmf'] = beneficio_gmf
    
    # 12. BASE GRAVABLE
    base_gravable = max(renta_liquida, 0)
    base_gravable_uvt = base_gravable / UVT_2024
    resultados['base_gravable'] = base_gravable
    resultados['base_gravable_uvt'] = base_gravable_uvt
    
    # 13. APLICAR TABLA ARTÍCULO 241
    impuesto_neto = aplicar_tabla_articulo_241(base_gravable_uvt, UVT_2024)
    resultados['impuesto_neto'] = impuesto_neto
    
    # 14. CÁLCULO DEL ANTICIPO (Artículo 807)
    anticipo_m1, anticipo_m2, anticipo_definitivo = calcular_anticipo(
        impuesto_neto,
        datos['impuesto_neto_anterior'],
        datos['retenciones'],
        datos['num_anos_declarando']
    )
    resultados['anticipo_metodo1'] = anticipo_m1
    resultados['anticipo_metodo2'] = anticipo_m2
    resultados['anticipo_definitivo'] = anticipo_definitivo
    
    # 15. LIQUIDACIÓN FINAL
    # Fórmula correcta: Impuesto Neto - Retenciones - Saldo a Favor Anterior - Anticipo Año Anterior + Anticipo Año Siguiente
    saldo_sin_anticipo = (impuesto_neto - datos['retenciones'] - 
                          datos['saldo_favor_anterior'] - datos['anticipo_anterior'])
    
    # SUMAR el anticipo del año siguiente al saldo
    liquidacion_final = saldo_sin_anticipo + anticipo_definitivo
    
    resultados['saldo_sin_anticipo'] = saldo_sin_anticipo
    resultados['es_saldo_favor'] = liquidacion_final < 0
    resultados['valor_final'] = abs(liquidacion_final)
    
    return resultados


def imprimir_resultados(datos, resultados):
    """Imprime los resultados de forma detallada"""
    print("\n" + "="*70)
    print(" " * 20 + "RESULTADOS DE LA LIQUIDACIÓN")
    print("="*70)
    
    print(f"\nContribuyente: {datos['nombre']}")
    print(f"NIT/Cédula: {datos['nit']}")
    
    print("\n--- DEPURACIÓN DE LA RENTA ---")
    print(f"Ingresos Totales:                    {formatear_moneda(resultados['ingresos_totales'])}")
    print(f"(-) INCR Total:                      {formatear_moneda(resultados['incr_total'])}")
    print(f"Ingreso Neto:                        {formatear_moneda(resultados['ingreso_neto'])}")
    print(f"\n(-) Cesantías Exentas Art. 206:      {formatear_moneda(resultados['cesantias_exentas'])}")
    print(f"(-) Deducciones:                     {formatear_moneda(resultados['deducciones_totales'])}")
    print(f"    (Dependientes:                   {formatear_moneda(resultados['deduccion_dependientes'])})")
    print(f"    (Medicina Prepagada:             {formatear_moneda(resultados['deduccion_medicina'])})")
    print(f"    (Intereses Vivienda:             {formatear_moneda(resultados['deduccion_intereses'])})")
    print(f"\nBase para Renta Exenta 25%:          {formatear_moneda(resultados['base_renta_exenta_25'])}")
    print(f"(-) Renta Exenta 25% (máx 790 UVT):  {formatear_moneda(resultados['renta_exenta_25'])}")
    print(f"(-) Pensión Vol. + AFC:              {formatear_moneda(resultados['pension_afc_limitada'])}")
    print(f"\nTotal Rentas Exentas:                {formatear_moneda(resultados['rentas_exentas_totales'])}")
    print(f"(-) Deducciones:                     {formatear_moneda(resultados['deducciones_totales'])}")
    print(f"\nLímite 40% Art. 336:                 {formatear_moneda(resultados['limite_maximo_depuracion'])}")
    print(f"Depuración Aplicada:                 {formatear_moneda(resultados['depuracion_final'])}")
    print(f"(-) Beneficio Factura Elect. (1%):   {formatear_moneda(resultados['beneficio_factura'])}")
    print(f"(-) Beneficio GMF (50%):             {formatear_moneda(resultados['beneficio_gmf'])}")
    print(f"\n{'='*70}")
    print(f"BASE GRAVABLE:                       {formatear_moneda(resultados['base_gravable'])}")
    print(f"BASE GRAVABLE (UVT):                 {resultados['base_gravable_uvt']:.2f} UVT")
    print(f"{'='*70}")
    
    print("\n--- LIQUIDACIÓN DEL IMPUESTO ---")
    print(f"Impuesto Neto (Art. 241):            {formatear_moneda(resultados['impuesto_neto'])}")
    print(f"(-) Retenciones:                     {formatear_moneda(datos['retenciones'])}")
    print(f"(-) Saldo a Favor Anterior:          {formatear_moneda(datos['saldo_favor_anterior'])}")
    print(f"(-) Anticipo Año Anterior:           {formatear_moneda(datos['anticipo_anterior'])}")
    print(f"Subtotal:                            {formatear_moneda(resultados['saldo_sin_anticipo'])}")
    
    print("\n--- ANTICIPO AÑO SIGUIENTE (Art. 807) ---")
    print(f"Anticipo Método 1:                   {formatear_moneda(resultados['anticipo_metodo1'])}")
    print(f"Anticipo Método 2:                   {formatear_moneda(resultados['anticipo_metodo2'])}")
    print(f"Anticipo Definitivo (menor):         {formatear_moneda(resultados['anticipo_definitivo'])}")
    
    print(f"\n(+) ANTICIPO A PAGAR AÑO SIGUIENTE:  {formatear_moneda(resultados['anticipo_definitivo'])}")
    
    print("\n" + "="*70)
    if resultados['es_saldo_favor']:
        print(" " * 25 + "*** SALDO A FAVOR ***")
    else:
        print(" " * 25 + "*** SALDO A PAGAR ***")
    print(" " * 20 + formatear_moneda(resultados['valor_final']))
    print("="*70)
    
    print("\n" + "-"*70)
    print("UVT 2024: $47,065")
    print("Estatuto Tributario Colombiano | Ley 2277 de 2022 | Decreto 1625/2016")
    print("-"*70)


def main():
    """Función principal del programa"""
    print("\n*** CALCULADORA IMPUESTO DE RENTA 2024 - COLOMBIA ***\n")
    
    # Capturar datos del usuario
    datos = capturar_datos()
    
    # Calcular impuesto
    resultados = calcular_impuesto_renta(datos)
    
    # Mostrar resultados
    imprimir_resultados(datos, resultados)
    
    # Opción para nuevo cálculo
    print("\n")
    continuar = input("¿Desea realizar otro cálculo? (s/n): ")
    if continuar.lower() == 's':
        main()
    else:
        print("\n¡Gracias por usar la calculadora de impuesto de renta!\n")


if __name__ == "__main__":
    main()