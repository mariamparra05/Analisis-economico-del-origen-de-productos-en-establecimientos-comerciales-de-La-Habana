import json
import os

def cargar_json(ruta):
    archivo = open(ruta, 'r', encoding='utf-8')
    datos = json.load(archivo)
    archivo.close()
    return datos

def cargar_establecimientos(ruta_archivo):
    datos = cargar_json(ruta_archivo)
    
    if isinstance(datos, list):
        return datos
    elif isinstance(datos, dict):
        return [datos]
    else:
        return []

def cargar_tasas_cambio(ruta_archivo):
    datos = cargar_json(ruta_archivo)
    return datos

def extraer_productos(establecimientos):
    productos = []
    
    for est in establecimientos:
        info = est['establishment']
        
        for prod in info['products']:
            nuevo_producto = {}
            nuevo_producto['name'] = prod['name']
            nuevo_producto['category'] = prod['category']
            nuevo_producto['origin'] = prod['origin']
            nuevo_producto['manufacturer'] = prod['manufacturer']
            nuevo_producto['price_cup'] = prod['price_cup']
            nuevo_producto['establishment'] = info['name']
            nuevo_producto['municipality'] = info['location']['municipality']
            
            productos.append(nuevo_producto)
    
    return productos

def combinar_productos(lista_productos):
    todos = []
    for productos in lista_productos:
        for prod in productos:
            todos.append(prod)
    return todos

def obtener_tasa(tasas, moneda):
    if tasas == None:
        return None
    
    for tasa in tasas['purchase_rates']:
        if tasa['currency'] == moneda:
            return float(tasa['purchase'])
    
    return None

def convertir_precio(precio_cup, tasas, moneda_destino):
    tasa = obtener_tasa(tasas, moneda_destino)
    
    if tasa == None or tasa == 0:
        return None
    
    return round(precio_cup / tasa, 2)

def contar_por_origen(productos):
    total = len(productos)
    nacional = 0
    
    for producto in productos:
        if producto['origin'] == 'CU':
            nacional = nacional + 1
    
    importado = total - nacional
    porcentaje_nacional = 0
    porcentaje_importado = 0
    
    if total > 0:
        porcentaje_nacional = (nacional / total) * 100
        porcentaje_importado = (importado / total) * 100
    
    resultado = {
        'total': total,
        'nacional': nacional,
        'importado': importado,
        'porcentaje_nacional': round(porcentaje_nacional, 2),
        'porcentaje_importado': round(porcentaje_importado, 2)
    }
    
    return resultado

def agrupar_por_campo(productos, campo):
    grupos = {}
    
    for producto in productos:
        valor = producto[campo]
        
        if valor not in grupos:
            grupos[valor] = []
        
        grupos[valor].append(producto)
    
    return grupos

def contar_por_categoria(productos):
    categorias = agrupar_por_campo(productos, 'category')
    resultado = {}
    
    for categoria in categorias:
        productos_cat = categorias[categoria]
        total = len(productos_cat)
        nacional = 0
        
        for producto in productos_cat:
            if producto['origin'] == 'CU':
                nacional = nacional + 1
        
        importado = total - nacional
        porcentaje_nacional = (nacional / total) * 100 if total > 0 else 0
        
        resultado[categoria] = {
            'total': total,
            'nacional': nacional,
            'importado': importado,
            'porcentaje_nacional': round(porcentaje_nacional, 2)
        }
    
    return resultado

def contar_productos_importados(productos):
    paises = {}
    
    for producto in productos:
        if producto['origin'] != 'CU':
            pais = producto['origin']
            if pais == '' or pais == None:
                pais = 'No especificado'
            
            if pais not in paises:
                paises[pais] = 0
            
            paises[pais] = paises[pais] + 1
    
    paises_lista = []
    for pais in paises:
        paises_lista.append({'pais': pais, 'cantidad': paises[pais]})
    
    paises_ordenados = ordenar_por_cantidad(paises_lista)
    
    return paises_ordenados

def ordenar_por_cantidad(lista):
    n = len(lista)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j]['cantidad'] < lista[j + 1]['cantidad']:
                temporal = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = temporal
    
    return lista

def calcular_promedio_precios(productos):
    if len(productos) == 0:
        return 0
    
    suma = 0
    for producto in productos:
        suma = suma + producto['price_cup']
    
    promedio = suma / len(productos)
    return round(promedio, 2)

def calcular_minimo(productos):
    if len(productos) == 0:
        return 0
    
    minimo = productos[0]['price_cup']
    
    for producto in productos:
        if producto['price_cup'] < minimo:
            minimo = producto['price_cup']
    
    return round(minimo, 2)

def calcular_maximo(productos):
    if len(productos) == 0:
        return 0
    
    maximo = productos[0]['price_cup']
    
    for producto in productos:
        if producto['price_cup'] > maximo:
            maximo = producto['price_cup']
    
    return round(maximo, 2)

def comparar_precios(productos):
    nacionales = []
    importados = []
    
    for producto in productos:
        if producto['origin'] == 'CU':
            nacionales.append(producto)
        else:
            importados.append(producto)
    
    promedio_nacional = calcular_promedio_precios(nacionales)
    promedio_importado = calcular_promedio_precios(importados)
    
    diferencia = promedio_importado - promedio_nacional
    porcentaje = 0
    
    if promedio_nacional > 0:
        porcentaje = (diferencia / promedio_nacional) * 100
    
    resultado = {
        'promedio_nacional': promedio_nacional,
        'promedio_importado': promedio_importado,
        'diferencia': round(diferencia, 2),
        'porcentaje_diferencia': round(porcentaje, 2)
    }
    
    return resultado

def comparar_precios_sin_lujos(productos):
    nacionales = []
    importados = []
    
    for producto in productos:
        categoria = producto['category']
        if categoria != 'Tabacos' and categoria != 'Bebidas Alcohólicas':
            if producto['origin'] == 'CU':
                nacionales.append(producto)
            else:
                importados.append(producto)
    
    promedio_nacional = calcular_promedio_precios(nacionales)
    promedio_importado = calcular_promedio_precios(importados)
    
    diferencia = promedio_importado - promedio_nacional
    porcentaje = 0
    
    if promedio_nacional > 0:
        porcentaje = (diferencia / promedio_nacional) * 100
    
    resultado = {
        'promedio_nacional': promedio_nacional,
        'promedio_importado': promedio_importado,
        'diferencia': round(diferencia, 2),
        'porcentaje_diferencia': round(porcentaje, 2),
        'cantidad_nacional': len(nacionales),
        'cantidad_importado': len(importados)
    }
    
    return resultado

def calcular_mediana(productos):
    if len(productos) == 0:
        return 0
    
    precios = []
    for producto in productos:
        precios.append(producto['price_cup'])
    
    n = len(precios)
    for i in range(n):
        for j in range(0, n - i - 1):
            if precios[j] > precios[j + 1]:
                temp = precios[j]
                precios[j] = precios[j + 1]
                precios[j + 1] = temp
    
    if n % 2 == 0:
        mediana = (precios[n // 2 - 1] + precios[n // 2]) / 2
    else:
        mediana = precios[n // 2]
    
    return round(mediana, 2)

def calcular_moda(productos):
    if len(productos) == 0:
        return 0
    
    precios = {}
    for producto in productos:
        precio = producto['price_cup']
        if precio not in precios:
            precios[precio] = 0
        precios[precio] = precios[precio] + 1
    
    max_frecuencia = 0
    moda = 0
    
    for precio in precios:
        if precios[precio] > max_frecuencia:
            max_frecuencia = precios[precio]
            moda = precio
    
    return round(moda, 2)

def calcular_media(productos):
    if len(productos) == 0:
        return 0
    
    suma = 0
    for producto in productos:
        suma = suma + producto['price_cup']
    
    media = suma / len(productos)
    return round(media, 2)

def analizar_estadisticas_precios(productos):
    nacionales = []
    importados = []
    
    for producto in productos:
        if producto['origin'] == 'CU':
            nacionales.append(producto)
        else:
            importados.append(producto)
    
    resultado = {
        'nacional': {
            'media': calcular_media(nacionales),
            'mediana': calcular_mediana(nacionales),
            'moda': calcular_moda(nacionales),
            'minimo': calcular_minimo(nacionales),
            'maximo': calcular_maximo(nacionales)
        },
        'importado': {
            'media': calcular_media(importados),
            'mediana': calcular_mediana(importados),
            'moda': calcular_moda(importados),
            'minimo': calcular_minimo(importados),
            'maximo': calcular_maximo(importados)
        }
    }
    
    return resultado


def analizar_precios_por_categoria(productos):
    categorias = agrupar_por_campo(productos, 'category')
    resultado = {}
    
    for categoria in categorias:
        productos_cat = categorias[categoria]
        nacionales = []
        importados = []
        
        for producto in productos_cat:
            if producto['origin'] == 'CU':
                nacionales.append(producto)
            else:
                importados.append(producto)
        
        resultado[categoria] = {
            'nacional': {
                'promedio': calcular_promedio_precios(nacionales),
                'minimo': calcular_minimo(nacionales),
                'maximo': calcular_maximo(nacionales),
                'cantidad': len(nacionales)
            },
            'importado': {
                'promedio': calcular_promedio_precios(importados),
                'minimo': calcular_minimo(importados),
                'maximo': calcular_maximo(importados),
                'cantidad': len(importados)
            }
        }
    
    return resultado

def productos_mas_caros(productos, cantidad):
    n = len(productos)
    productos_copia = []
    
    for producto in productos:
        productos_copia.append(producto)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if productos_copia[j]['price_cup'] < productos_copia[j + 1]['price_cup']:
                temporal = productos_copia[j]
                productos_copia[j] = productos_copia[j + 1]
                productos_copia[j + 1] = temporal
    
    resultado = []
    limite = min(cantidad, len(productos_copia))
    
    for i in range(limite):
        producto = productos_copia[i]
        origen = 'Nacional' if producto['origin'] == 'CU' else 'Importado'
        
        resultado.append({
            'nombre': producto['name'],
            'precio': producto['price_cup'],
            'origen': origen,
            'categoria': producto['category']
        })
    
    return resultado

def contar_fabricantes(productos, origen_filtro):
    fabricantes = {}
    
    for producto in productos:
        es_nacional = producto['origin'] == 'CU'
        
        if origen_filtro == 'nacional' and es_nacional:
            fab = producto['manufacturer']
            if fab not in fabricantes:
                fabricantes[fab] = 0
            fabricantes[fab] = fabricantes[fab] + 1
        elif origen_filtro == 'importado' and not es_nacional:
            fab = producto['manufacturer']
            if fab not in fabricantes:
                fabricantes[fab] = 0
            fabricantes[fab] = fabricantes[fab] + 1
    
    fabricantes_lista = []
    for fab in fabricantes:
        fabricantes_lista.append({'fabricante': fab, 'cantidad': fabricantes[fab]})
    
    fabricantes_ordenados = ordenar_por_cantidad(fabricantes_lista)
    
    return fabricantes_ordenados

def top_fabricantes_nacionales(productos, cantidad):
    fabricantes = contar_fabricantes(productos, 'nacional')
    limite = min(cantidad, len(fabricantes))
    return fabricantes[:limite]

def top_fabricantes_importados(productos, cantidad):
    fabricantes = contar_fabricantes(productos, 'importado')
    limite = min(cantidad, len(fabricantes))
    return fabricantes[:limite]

def contar_establecimientos_por_tipo(establecimientos):
    tipos = {}
    
    for est in establecimientos:
        tipo = est['establishment']['type']
        
        if tipo not in tipos:
            tipos[tipo] = 0
        
        tipos[tipo] = tipos[tipo] + 1
    
    return tipos

def distribucion_municipios(productos):
    municipios = {}
    
    for producto in productos:
        municipio = producto['municipality']
        
        if municipio not in municipios:
            municipios[municipio] = {'nacional': 0, 'importado': 0}
        
        if producto['origin'] == 'CU':
            municipios[municipio]['nacional'] = municipios[municipio]['nacional'] + 1
        else:
            municipios[municipio]['importado'] = municipios[municipio]['importado'] + 1
    
    resultado = {}
    for municipio in municipios:
        nacional = municipios[municipio]['nacional']
        importado = municipios[municipio]['importado']
        total = nacional + importado
        porcentaje = (nacional / total) * 100 if total > 0 else 0
        
        resultado[municipio] = {
            'total': total,
            'nacional': nacional,
            'importado': importado,
            'porcentaje_nacional': round(porcentaje, 2)
        }
    
    return resultado

def buscar_por_nombre(productos, palabras):
    encontrados = []
    
    for producto in productos:
        nombre = producto['name'].lower()
        encontrado = False
        
        for palabra in palabras:
            if palabra.lower() in nombre:
                encontrado = True
                break
        
        if encontrado:
            encontrados.append(producto)
    
    return encontrados

def analizar_producto_especifico(productos, palabras):
    encontrados = buscar_por_nombre(productos, palabras)
    
    if len(encontrados) == 0:
        return None
    
    total = len(encontrados)
    nacional = 0
    
    for producto in encontrados:
        if producto['origin'] == 'CU':
            nacional = nacional + 1
    
    importado = total - nacional
    porcentaje = (nacional / total) * 100 if total > 0 else 0
    
    resultado = {
        'total': total,
        'nacional': nacional,
        'importado': importado,
        'porcentaje_nacional': round(porcentaje, 2)
    }
    
    return resultado

def analizar_productos_estrategicos(productos):
    azucar = analizar_producto_especifico(productos, ['azucar', 'azúcar', 'sugar'])
    cafe = analizar_producto_especifico(productos, ['cafe', 'café', 'coffee'])
    ron = analizar_producto_especifico(productos, ['ron', 'rum'])
    tabaco = analizar_producto_especifico(productos, ['tabaco', 'cigarro', 'habano'])
    
    resultado = {}
    
    if azucar:
        resultado['azucar'] = azucar
    if cafe:
        resultado['cafe'] = cafe
    if ron:
        resultado['ron'] = ron
    if tabaco:
        resultado['tabaco'] = tabaco
    
    return resultado

def analizar_primera_necesidad(productos):
    arroz = analizar_producto_especifico(productos, ['arroz', 'rice'])
    pollo = analizar_producto_especifico(productos, ['pollo', 'chicken'])
    aceite = analizar_producto_especifico(productos, ['aceite', 'oil'])
    frijol = analizar_producto_especifico(productos, ['frijol', 'bean'])
    
    resultado = {}
    
    if arroz:
        resultado['arroz'] = arroz
    if pollo:
        resultado['pollo'] = pollo
    if aceite:
        resultado['aceite'] = aceite
    if frijol:
        resultado['frijol'] = frijol
    
    return resultado

def guardar_json(datos, ruta):
    archivo = open(ruta, 'w', encoding='utf-8')
    json.dump(datos, archivo, ensure_ascii=False, indent=2)
    archivo.close()

def generar_reporte(establecimientos, productos, ruta):
    reporte = {
        'resumen': {
            'total_establecimientos': len(establecimientos),
            'total_productos': len(productos),
            'tipos_establecimientos': contar_establecimientos_por_tipo(establecimientos)
        },
        'analisis_origen': {
            'general': contar_por_origen(productos),
            'por_categoria': contar_por_categoria(productos),
            'paises_importacion': contar_productos_importados(productos)
        },
        'analisis_precios': {
            'comparacion': comparar_precios(productos),
            'por_categoria': analizar_precios_por_categoria(productos),
            'mas_caros': productos_mas_caros(productos, 10)
        },
        'analisis_especifico': {
            'productos_estrategicos': analizar_productos_estrategicos(productos),
            'primera_necesidad': analizar_primera_necesidad(productos)
        },
        'analisis_geografico': {
            'distribucion_municipios': distribucion_municipios(productos)
        },
        'top_fabricantes': {
            'nacionales': top_fabricantes_nacionales(productos, 10),
            'importados': top_fabricantes_importados(productos, 10)
        }
    }
    
    guardar_json(reporte, ruta)
    return reporte