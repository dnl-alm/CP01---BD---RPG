from flask import Flask, jsonify, render_template
import banco
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/herois", methods=['GET'])
@cross_origin()
def get_herois():
    herois = banco.listar_herois()
    return {"herois": herois}, 200

@app.route("/dano-nevoa", methods=["PUT"])
def processar():
    banco.dano_nevoa()
    return jsonify({"msg": "Turno processado"})

if __name__ == "__main__":
    app.run(debug=True)