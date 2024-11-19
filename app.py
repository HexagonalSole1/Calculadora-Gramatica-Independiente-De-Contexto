from flask import Flask, request, render_template
import re

app = Flask(__name__)

# Gramática independiente del contexto para expresiones matemáticas básicas.
def evaluar_expresion(expresion):
    try:
        # Asegúrate de validar la expresión antes de evaluarla
        # Aquí usamos una expresión regular simple para filtrar solo números y operadores básicos
        if not re.fullmatch(r'[0-9+\-*/(). ]+', expresion):
            return "Expresión inválida"
        resultado = eval(expresion)
        return resultado
    except Exception as e:
        return f"Error: {e}"

@app.route('/', methods=['GET', 'POST'])
def calculadora():
    resultado = None
    if request.method == 'POST':
        expresion = request.form.get('expresion')
        resultado = evaluar_expresion(expresion)
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
