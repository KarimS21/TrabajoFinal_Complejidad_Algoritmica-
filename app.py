from flask import Flask, render_template, request
from BuscadorBFS import buscar_por_nombre_o_apellido, encontrar_mejor_coincidencia
import pandas as pd

app = Flask(__name__)

# Cargar los datos para obtener nombres y apellidos
data = pd.read_csv("ComplejidadAlgoritmicaDF.csv")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    user_id = request.form['user-id']
    user_name = request.form['user-name']

    if not user_id or not user_name:
        error = "Por favor, ingrese tanto el ID de usuario como el nombre o apellido."
        return render_template('results.html', error=error)

    posibles_ids = buscar_por_nombre_o_apellido(user_name)['ID'].astype(str).tolist()
    
    # Obtener las mejores coincidencias
    coincidencias = []
    for _ in range(3):  # Intentar obtener hasta 3 mejores coincidencias
        mejor_coincidencia, max_amigos_comun, mejor_camino = encontrar_mejor_coincidencia(user_id, posibles_ids)
        if mejor_coincidencia:
            # Obtener el nombre y apellido del usuario encontrado 
            usuario = data[data['ID'] == int(mejor_coincidencia)].iloc[0]
            nombre_completo = f"{usuario['Nombre']} {usuario['Apellido']}"
            edad = usuario["Edad"]
            gusto = usuario["Gusto"]
            coincidencias.append((mejor_coincidencia, nombre_completo,edad,gusto, max_amigos_comun, mejor_camino))
            posibles_ids.remove(mejor_coincidencia)  # Remover la mejor coincidencia encontrada para la próxima iteración
        else:
            break  # Si no se encuentran más coincidencias, salir del bucle
    
    resultados = []
    for coincidencia in coincidencias:
        mejor_coincidencia, nombre_completo,edad,gusto, max_amigos_comun, mejor_camino = coincidencia
        resultado = {
            'persona': nombre_completo if mejor_coincidencia else 'No encontrada',
            'id': mejor_coincidencia if mejor_coincidencia else 'N/A',
            'amigos_en_comun': max_amigos_comun if mejor_coincidencia else 'N/A',
            'edad': edad if mejor_coincidencia else 'N/A',
            'gusto': gusto if mejor_coincidencia else 'N/A',
            'camino': ' -> '.join(mejor_camino) if mejor_camino else 'N/A' 
        }
        resultados.append(resultado)

    return render_template('results.html', resultados=resultados, datosUser=f'ID de usuario: {user_id}',inputUser= f'Input del usuario: {user_name}')

if __name__ == '__main__':
    app.run(debug=True)
