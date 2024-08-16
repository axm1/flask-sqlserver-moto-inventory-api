from flask import Flask, Blueprint, jsonify, request, abort
from flask_cors import CORS
import pyodbc
from dotenv import load_dotenv
import os


# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Configuración del Blueprint
main = Blueprint('main', __name__)

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=prueba_xumtech;'
        'UID=DESKTOP-1PQRS96/Personal;'
        'Trusted_Connection=yes;'
    )
    return conn

# Verifica el token de acceso
def check_token():
    token = request.headers.get('Authorization')
    expected_token = os.getenv('AUTH_TOKEN')
    print (token, expected_token)
    if token != f'{expected_token}':
        abort(403)  # Forbidden


@main.route('/preguntas_iniciales', methods=['GET'])
def get_preguntas():
    check_token()  # Verifica el token antes de continuar

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id_pregunta, pregunta FROM preguntas_principales')
    preguntas = cursor.fetchall()
    conn.close()

    preguntas_list = [{'id_pregunta': row.id_pregunta, 'pregunta': row.pregunta} for row in preguntas]
    return jsonify(preguntas_list)
    
@main.route('/marcas', methods=['GET'])
def get_marcas():
    check_token()  # Verifica el token antes de continuar
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM marcas')
    marcas = cursor.fetchall()
    conn.close()

    marcas_list = [{'id_marca': row.id_marca, 'marca': row.marca} for row in marcas]
    return jsonify(marcas_list)

@main.route('/ubicaciones', methods=['GET'])
def get_all_ubications ():
    check_token()  # Verifica el token antes de continuar
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ubicaciones ')
    ubicaciones = cursor.fetchall()
    conn.close()

    ubicaciones_list = [{'id_ubicacion': row.id_ubicacion, 'ubicacion': row.ubicacion} for row in ubicaciones]
    return jsonify(ubicaciones_list)


@main.route('/modelos_por_marcas', methods=['GET'])
def get_modelos_por_marcas():
    check_token()  # Verifica el token antes de continuar
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Modelos WHERE id_marca = ?', request.args.get('id_marca'))
    modelos = cursor.fetchall()
    conn.close()

    modelos_list = [{'id_modelo': row.id_modelo, 'modelos': row.modelos, 'precio': row.precio} for row in modelos]
    return jsonify(modelos_list)

@main.route('/disponibilidad_modelo_por_ubicacion', methods=['GET'])
def get_disponibilidad_modelo_por_ubicacion():
    check_token()  # Verifica el token antes de continuar
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT 
                            u.ubicacion,
                            COUNT(d_p_u.id_ubicacion) AS cantidad_disponible
                        FROM 
                            disponibilidad_producto_por_ubicacion d_p_u
                        JOIN 
                            Ubicaciones u ON d_p_u.id_ubicacion = u.id_ubicacion
                        WHERE 
                            d_p_u.id_modelo = ''' + request.args.get('id_modelo') + '''
                        GROUP BY
                            u.ubicacion''')
    disponibilidad = cursor.fetchall()
    conn.close()

    disponibilidad_list = [{'ubicacion': row.ubicacion, 'cantidad_disponible': row.cantidad_disponible} for row in disponibilidad]
    return jsonify(disponibilidad_list)



# Función para crear la aplicación Flask
def create_app():
    app = Flask(__name__)

    # Habilitar CORS con configuración personalizada
    CORS(app)  # Permite todas las solicitudes a este endpoint

    # Registra el Blueprint
    app.register_blueprint(main)
    
    return app

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
