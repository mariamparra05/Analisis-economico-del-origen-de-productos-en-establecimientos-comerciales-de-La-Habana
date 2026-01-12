import plotly.graph_objects as go
import plotly.express as px

def grafica_pastel_origen(productos):
    nacional = 0
    importado = 0
    
    for producto in productos:
        if producto['origin'] == 'CU':
            nacional = nacional + 1
        else:
            importado = importado + 1
    
    fig = go.Figure(data=[go.Pie(
        labels=['Nacional', 'Importado'],
        values=[nacional, importado],
        marker=dict(colors=['#2E7D32', '#1976D2'])
    )])
    
    fig.update_layout(
        title='Distribución de Productos por Origen',
        font=dict(size=14)
    )
    
    return fig

def grafica_barras_categoria(productos):
    categorias = {}
    
    for producto in productos:
        cat = producto['category']
        if cat not in categorias:
            categorias[cat] = {'Nacional': 0, 'Importado': 0}
        
        if producto['origin'] == 'CU':
            categorias[cat]['Nacional'] = categorias[cat]['Nacional'] + 1
        else:
            categorias[cat]['Importado'] = categorias[cat]['Importado'] + 1
    
    nombres = list(categorias.keys())
    nacionales = []
    importados = []
    
    for cat in nombres:
        nacionales.append(categorias[cat]['Nacional'])
        importados.append(categorias[cat]['Importado'])
    
    fig = go.Figure(data=[
        go.Bar(name='Nacional', x=nombres, y=nacionales, marker_color='#2E7D32'),
        go.Bar(name='Importado', x=nombres, y=importados, marker_color='#1976D2')
    ])
    
    fig.update_layout(
        title='Productos Nacionales vs Importados por Categoría',
        xaxis_title='Categoría',
        yaxis_title='Cantidad de Productos',
        barmode='group',
        font=dict(size=12)
    )
    
    return fig

def grafica_precios_categoria(productos):
    categorias = {}
    
    for producto in productos:
        cat = producto['category']
        if cat not in categorias:
            categorias[cat] = {'Nacional': [], 'Importado': []}
        
        precio = producto['price_cup']
        if producto['origin'] == 'CU':
            categorias[cat]['Nacional'].append(precio)
        else:
            categorias[cat]['Importado'].append(precio)
    
    nombres = list(categorias.keys())
    promedios_nac = []
    promedios_imp = []
    
    for cat in nombres:
        if len(categorias[cat]['Nacional']) > 0:
            promedio = sum(categorias[cat]['Nacional']) / len(categorias[cat]['Nacional'])
            promedios_nac.append(promedio)
        else:
            promedios_nac.append(0)
        
        if len(categorias[cat]['Importado']) > 0:
            promedio = sum(categorias[cat]['Importado']) / len(categorias[cat]['Importado'])
            promedios_imp.append(promedio)
        else:
            promedios_imp.append(0)
    
    fig = go.Figure(data=[
        go.Bar(name='Nacional', x=nombres, y=promedios_nac, marker_color='#2E7D32'),
        go.Bar(name='Importado', x=nombres, y=promedios_imp, marker_color='#1976D2')
    ])
    
    fig.update_layout(
        title='Comparación de Precios Promedio por Categoría',
        xaxis_title='Categoría',
        yaxis_title='Precio Promedio (CUP)',
        barmode='group',
        font=dict(size=12)
    )
    
    return fig

def grafica_paises(productos, top=10):
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
    
    n = len(paises_lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if paises_lista[j]['cantidad'] < paises_lista[j + 1]['cantidad']:
                temp = paises_lista[j]
                paises_lista[j] = paises_lista[j + 1]
                paises_lista[j + 1] = temp
    
    paises_top = paises_lista[:top]
    nombres = []
    valores = []
    
    for p in paises_top:
        nombres.append(p['pais'])
        valores.append(p['cantidad'])
    
    fig = go.Figure(data=[
        go.Bar(x=nombres, y=valores, marker_color='#1976D2')
    ])
    
    fig.update_layout(
        title=f'Top {top} Países de Origen de Productos Importados',
        xaxis_title='País',
        yaxis_title='Cantidad de Productos',
        font=dict(size=12)
    )
    
    return fig

def grafica_municipios(productos):
    municipios = {}
    
    for producto in productos:
        mun = producto['municipality']
        if mun not in municipios:
            municipios[mun] = {'Nacional': 0, 'Importado': 0}
        
        if producto['origin'] == 'CU':
            municipios[mun]['Nacional'] = municipios[mun]['Nacional'] + 1
        else:
            municipios[mun]['Importado'] = municipios[mun]['Importado'] + 1
    
    nombres = list(municipios.keys())
    nacionales = []
    importados = []
    
    for mun in nombres:
        nacionales.append(municipios[mun]['Nacional'])
        importados.append(municipios[mun]['Importado'])
    
    fig = go.Figure(data=[
        go.Bar(name='Nacional', x=nombres, y=nacionales, marker_color='#2E7D32'),
        go.Bar(name='Importado', x=nombres, y=importados, marker_color='#1976D2')
    ])
    
    fig.update_layout(
        title='Distribución de Productos por Municipio',
        xaxis_title='Municipio',
        yaxis_title='Cantidad de Productos',
        barmode='stack',
        font=dict(size=12)
    )
    
    return fig

def grafica_fabricantes(productos, top=10):
    fabricantes = {}
    
    for producto in productos:
        if producto['origin'] == 'CU':
            fab = producto['manufacturer']
            if fab not in fabricantes:
                fabricantes[fab] = 0
            fabricantes[fab] = fabricantes[fab] + 1
    
    fab_lista = []
    for fab in fabricantes:
        fab_lista.append({'nombre': fab, 'cantidad': fabricantes[fab]})
    
    n = len(fab_lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if fab_lista[j]['cantidad'] < fab_lista[j + 1]['cantidad']:
                temp = fab_lista[j]
                fab_lista[j] = fab_lista[j + 1]
                fab_lista[j + 1] = temp
    
    fab_top = fab_lista[:top]
    nombres = []
    valores = []
    
    for f in fab_top:
        nombres.append(f['nombre'])
        valores.append(f['cantidad'])
    
    fig = go.Figure(data=[
        go.Bar(x=valores, y=nombres, orientation='h', marker_color='#2E7D32')
    ])
    
    fig.update_layout(
        title=f'Top {top} Fabricantes Nacionales',
        xaxis_title='Cantidad de Productos',
        yaxis_title='Fabricante',
        font=dict(size=12)
    )
    
    return fig

def grafica_dispersion_precios(productos):
    precios_nac = []
    precios_imp = []
    categorias_nac = []
    categorias_imp = []
    
    for producto in productos:
        if producto['origin'] == 'CU':
            precios_nac.append(producto['price_cup'])
            categorias_nac.append(producto['category'])
        else:
            precios_imp.append(producto['price_cup'])
            categorias_imp.append(producto['category'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=categorias_nac,
        y=precios_nac,
        mode='markers',
        name='Nacional',
        marker=dict(color='#2E7D32', size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=categorias_imp,
        y=precios_imp,
        mode='markers',
        name='Importado',
        marker=dict(color='#1976D2', size=8)
    ))
    
    fig.update_layout(
        title='Distribución de Precios por Categoría y Origen',
        xaxis_title='Categoría',
        yaxis_title='Precio (CUP)',
        font=dict(size=12)
    )
    
    return fig

def grafica_linea_tendencia(productos):
    categorias = {}
    
    for producto in productos:
        cat = producto['category']
        if cat not in categorias:
            categorias[cat] = {'Nacional': 0, 'Importado': 0}
        
        if producto['origin'] == 'CU':
            categorias[cat]['Nacional'] = categorias[cat]['Nacional'] + 1
        else:
            categorias[cat]['Importado'] = categorias[cat]['Importado'] + 1
    
    nombres = list(categorias.keys())
    porcentajes_nacionales = []
    
    for cat in nombres:
        total = categorias[cat]['Nacional'] + categorias[cat]['Importado']
        if total > 0:
            porcentaje = (categorias[cat]['Nacional'] / total) * 100
            porcentajes_nacionales.append(porcentaje)
        else:
            porcentajes_nacionales.append(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=nombres,
        y=porcentajes_nacionales,
        mode='lines+markers',
        name='% Nacional',
        line=dict(color='#2E7D32', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_hline(y=50, line_dash="dash", line_color="gray", 
                  annotation_text="50% (Equilibrio)")
    
    fig.update_layout(
        title='Porcentaje de Productos Nacionales por Categoría',
        xaxis_title='Categoría',
        yaxis_title='Porcentaje Nacional (%)',
        font=dict(size=12),
        yaxis=dict(range=[0, 100])
    )
    
    return fig

def guardar_grafica(figura, ruta):
    figura.write_html(ruta)

def guardar_imagen(figura, ruta):
    figura.write_image(ruta)

def grafica_barras_horizontales_paises(productos, top=10):
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
    
    n = len(paises_lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if paises_lista[j]['cantidad'] < paises_lista[j + 1]['cantidad']:
                temp = paises_lista[j]
                paises_lista[j] = paises_lista[j + 1]
                paises_lista[j + 1] = temp
    
    paises_top = paises_lista[:top]
    nombres = []
    valores = []
    
    for p in paises_top:
        nombres.append(p['pais'])
        valores.append(p['cantidad'])
    
    fig = go.Figure(data=[
        go.Bar(y=nombres, x=valores, orientation='h', marker_color='#FF6B35')
    ])
    
    fig.update_layout(
        title=f'Top {top} Países Exportadores a Cuba',
        xaxis_title='Cantidad de Productos',
        yaxis_title='País',
        font=dict(size=12)
    )
    
    return fig

def grafica_dona_categorias(productos):
    categorias = {}
    
    for producto in productos:
        cat = producto['category']
        if cat not in categorias:
            categorias[cat] = 0
        categorias[cat] = categorias[cat] + 1
    
    nombres = list(categorias.keys())
    valores = list(categorias.values())
    
    fig = go.Figure(data=[go.Pie(
        labels=nombres,
        values=valores,
        hole=0.4,
        marker=dict(colors=px.colors.qualitative.Set3)
    )])
    
    fig.update_layout(
        title='Distribución de Productos por Categoría',
        font=dict(size=14)
    )
    
    return fig

def grafica_area_precios_comparacion(productos):
    categorias = {}
    
    for producto in productos:
        cat = producto['category']
        if cat not in categorias:
            categorias[cat] = {'Nacional': [], 'Importado': []}
        
        precio = producto['price_cup']
        if producto['origin'] == 'CU':
            categorias[cat]['Nacional'].append(precio)
        else:
            categorias[cat]['Importado'].append(precio)
    
    nombres = list(categorias.keys())
    promedios_nac = []
    promedios_imp = []
    
    for cat in nombres:
        if len(categorias[cat]['Nacional']) > 0:
            promedio = sum(categorias[cat]['Nacional']) / len(categorias[cat]['Nacional'])
            promedios_nac.append(promedio)
        else:
            promedios_nac.append(0)
        
        if len(categorias[cat]['Importado']) > 0:
            promedio = sum(categorias[cat]['Importado']) / len(categorias[cat]['Importado'])
            promedios_imp.append(promedio)
        else:
            promedios_imp.append(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=nombres,
        y=promedios_nac,
        fill='tozeroy',
        name='Nacional',
        line=dict(color='#2E7D32')
    ))
    
    fig.add_trace(go.Scatter(
        x=nombres,
        y=promedios_imp,
        fill='tonexty',
        name='Importado',
        line=dict(color='#1976D2')
    ))
    
    fig.update_layout(
        title='Comparación de Precios Promedio (Áreas)',
        xaxis_title='Categoría',
        yaxis_title='Precio Promedio (CUP)',
        font=dict(size=12)
    )
    
    return fig

def mostrar_grafica(figura):
    figura.show()