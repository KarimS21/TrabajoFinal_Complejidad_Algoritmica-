from flask import Flask, redirect, url_for, render_template, request, session
from BuscadorBFS import buscar_por_nombre_o_apellido, encontrar_mejor_coincidencia, data
app = Flask(__name__)
app.secret_key = "hello"

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        usuario_id = request.form["id_user"]

        nombre_o_apellido = request.form["nombre_Apellido"]

        resultados = buscar_por_nombre_o_apellido(nombre_o_apellido)
        ##hasta aqui deberia funcionar todo bien,
        #de aqui para abajo se debe pensar como representar el resultado en el html
        #para ver que todo funciona, miren la terminal, ahi sale el resultado del algoritmo

        if resultados.empty:
            print("No se encontraron resultados.")
        else:
            print("Resultados encontrados:")
            print(resultados[['ID', 'Nombre', 'Apellido']])
            posibles_ids = resultados['ID'].astype(str).tolist()
    
            mejor_coincidencia, num_amigos_comun, mejor_camino = encontrar_mejor_coincidencia(usuario_id, posibles_ids)
    
        mejor_persona = data[data['ID'] == int(mejor_coincidencia)]
        print("\nLa persona con más amigos en común es:")
        print(mejor_persona[['ID', 'Nombre', 'Apellido']])
        print(f"Cantidad de amigos en común: {num_amigos_comun}")
        print(f"Camino BFS: {mejor_camino}")


        return render_template("index.html")
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)