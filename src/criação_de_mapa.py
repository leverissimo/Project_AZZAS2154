import json
import folium
from geopy.geocoders import Nominatim

path = "analises/dados/filiais_UF_SP.json"
with open(path, "r", encoding="utf-8") as f:
    dados = json.load(f)

# --- Detectar automaticamente o formato ---
if isinstance(dados, list):
    # Formato 2: já é lista
    lista_filiais = dados
elif isinstance(dados, dict):
    # Formato 1: pegar a primeira chave e acessar a lista
    chave_principal = list(dados.keys())[0]
    lista_filiais = dados[chave_principal]
else:
    raise ValueError("Formato de JSON não reconhecido")

# Inicializar geolocalizador
geolocator = Nominatim(user_agent="mapa_filiais")

# Criar mapa centralizado em São Paulo
mapa = folium.Map(location=[-23.55, -46.63], zoom_start=11)

for filial in lista_filiais:
    endereco_completo = f"{filial['ENDERECO']}, {filial['BAIRRO']}, {filial['CIDADE']}, {filial['UF']}, Brasil"
    print(endereco_completo)
    try:
        local = geolocator.geocode(endereco_completo)
        if local:
            folium.Marker(
                [local.latitude, local.longitude],
                popup=f"{filial['FILIAL']} ({filial['COD_FILIAL']})",
                tooltip=filial['FILIAL']
            ).add_to(mapa)
    except Exception as e:
        print(f"Erro ao localizar {filial['FILIAL']}: {e}")

# Salvar mapa em HTML
mapa.save("mapa_filiais_sp.html")
print("Mapa gerado: mapa_filiais_sp.html")
