from flask import Flask, render_template, request
from BuscadorBFS import buscar_por_nombre_o_apellido, encontrar_mejor_coincidencia

app = Flask(__name__)

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
    mejor_coincidencia, max_amigos_comun, mejor_camino = encontrar_mejor_coincidencia(user_id, posibles_ids)
    
    resultado = {
        'datos': f'ID de usuario: {user_id}, Nombre: {user_name}',
        'persona': mejor_coincidencia if mejor_coincidencia else 'No encontrada',
        'amigos_en_comun': max_amigos_comun if mejor_coincidencia else 'N/A',
        'camino': ' -> '.join(mejor_camino) if mejor_camino else 'N/A'
    }
    return render_template('results.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
