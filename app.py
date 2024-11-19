from flask import Flask, request, render_template
from lark import Lark, Transformer, v_args

# Define la gramática independiente del contexto
GRAMATICA = """
    start: expr
    expr: expr "+" term  -> suma
        | expr "-" term  -> resta
        | term
    term: term "*" factor -> multiplicacion
        | term "/" factor -> division
        | factor
    factor: NUMBER        -> numero
        | "(" expr ")"    -> agrupacion
    %import common.NUMBER  // Importa números decimales
    %import common.WS      // Importa espacios en blanco
    %ignore WS             // Ignora espacios en blanco
"""

# Transformador para procesar y evaluar las expresiones
@v_args(inline=True)
class CalculadoraTransformer(Transformer):
    def suma(self, a, b):
        return self._convert_to_float(a) + self._convert_to_float(b)

    def resta(self, a, b):
        return self._convert_to_float(a) - self._convert_to_float(b)

    def multiplicacion(self, a, b):
        return self._convert_to_float(a) * self._convert_to_float(b)

    def division(self, a, b):
        return self._convert_to_float(a) / self._convert_to_float(b)

    def numero(self, n):
        return float(n)

    def agrupacion(self, a):
        return self._convert_to_float(a)  # Convierte el valor agrupado

    def _convert_to_float(self, value):
        # Si el valor es un nodo Tree, extrae el valor; de lo contrario, conviértelo a float
        if isinstance(value, list):
            # Extraer el primer elemento si es una lista (como en agrupaciones)
            value = value[0]
        if hasattr(value, 'children'):
            # Si tiene hijos, extraer el primer hijo (valor del nodo)
            return float(value.children[0])
        return float(value)

# Crea el analizador sintáctico
analizador = Lark(GRAMATICA, parser='lalr', transformer=CalculadoraTransformer())

def evaluar_expresion(expresion):
    try:
        resultado = analizador.parse(expresion)
        # Si el resultado es un árbol, extraemos el valor
        if hasattr(resultado, 'children') and len(resultado.children) == 1:
            return resultado.children[0]
        return resultado
    except Exception as e:
        return f"Error en la expresión: {e}"

# Configuración de Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculadora():
    resultado = None
    if request.method == 'POST':
        expresion = request.form.get('expresion')
        resultado = evaluar_expresion(expresion)
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
