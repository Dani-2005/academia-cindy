# from flask import Flask, jsonify
# from flask_cors import CORS
# import requests

# app = Flask(__name__)
# CORS(app)

# @app.route('/api/tasa', methods=['GET'])
# def obtener_tasa():
#     # Pusimos la internacional de primera por estabilidad
#     fuentes = [
#         "https://open.er-api.com/v6/latest/USD",
#         "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/page?page=bcv",
#         "https://ve.dolarapi.com/v1/dolares/bcv"
#     ]

#     # El margen que cobran los dueños (20 puntos = 20 Bs)
#     MARGEN_ACADEMIA = 20.00

#     for url in fuentes:
#         try:
#             response = requests.get(url, timeout=10)
#             if response.status_code == 200:
#                 data = response.json()
                
#                 tasa_base = 0
                
#                 if 'rates' in data: # Internacional
#                     tasa_base = data['rates']['VES']
#                 elif 'monitors' in data: # PyDolar
#                     tasa_base = data['monitors']['usd']['price']
#                 elif 'promedio' in data: # DolarAPI
#                     tasa_base = data['promedio']

#                 if tasa_base > 0:
#                     # APLICAMOS EL AJUSTE DE LA ACADEMIA AQUÍ
#                     tasa_final = round(tasa_base + MARGEN_ACADEMIA, 2)
                    
#                     return jsonify({
#                         "status": "success",
#                         "tasa": tasa_final,
#                         "tasa_base": round(tasa_base, 2),
#                         "fecha": "Ajustada (+20)"
#                     })

#         except Exception as e:
#             continue

#     # Fallback si todo falla (Tasa base estimada + 20)
#     return jsonify({
#         "status": "fallback",
#         "tasa": 45.00 + MARGEN_ACADEMIA, 
#         "fecha": "Manual + Margen"
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

import json
import requests

def handler(event, context):
    # Configuración de los dueños
    MARGEN_ACADEMIA = 20.00
    
    # Fuentes de respaldo
    fuentes = [
        "https://open.er-api.com/v6/latest/USD",
        "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/page?page=bcv"
    ]

    tasa_final = 45.00 + MARGEN_ACADEMIA # Tasa de seguridad
    status = "fallback"

    for url in fuentes:
        try:
            # Timeout corto para que la función sea rápida
            response = requests.get(url, timeout=4)
            if response.status_code == 200:
                data = response.json()
                tasa_base = 0
                
                if 'rates' in data: # Caso API Internacional
                    tasa_base = data['rates']['VES']
                elif 'monitors' in data: # Caso PyDolar
                    tasa_base = data['monitors']['usd']['price']
                
                if tasa_base > 0:
                    tasa_final = round(tasa_base + MARGEN_ACADEMIA, 2)
                    status = "success"
                    break
        except:
            continue

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*" # Permite que el HTML la lea
        },
        "body": json.dumps({
            "tasa": tasa_final,
            "status": status
        })
    }