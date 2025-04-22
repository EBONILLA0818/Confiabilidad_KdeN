from flask import Flask, render_template, request
import itertools
import math

app = Flask(__name__)

def confiabilidad_individual(lambda_i, t):
    return math.exp(-lambda_i * t)

def confiabilidad_sistema(tasas_falla, k, t):
    n = len(tasas_falla)
    confiabilidad_total = 0

    for i in range(k, n + 1):
        for indices_on in itertools.combinations(range(n), i):
            prob = 1
            for j in range(n):
                if j in indices_on:
                    prob *= confiabilidad_individual(tasas_falla[j], t)
                else:
                    prob *= (1 - confiabilidad_individual(tasas_falla[j], t))
            confiabilidad_total += prob

    return confiabilidad_total

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        tasas_texto = request.form["tasas"]
        tasas = list(map(float, tasas_texto.strip().split(",")))
        k = int(request.form["k"])
        t = float(request.form["t"])
        resultado = confiabilidad_sistema(tasas, k, t)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
