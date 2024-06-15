from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    user_id = request.form['user-id']
    user_name = request.form['user-name']
    # Aquí puedes llamar a la función del algoritmo con user_id y user_name
    # resultado = tu_funcion_del_algoritmo(user_id, user_name)
    # Simulando un resultado
    resultado = {
        'datos': f'ID de usuario: {user_id}, Nombre: {user_name}',
        'persona': 'Ejemplo Persona',
        'amigos_en_comun': 5,
        'camino': 'Camino Ejemplo'
    }
    return render_template('results.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
