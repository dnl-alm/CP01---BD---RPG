from flask import Flask, jsonify
import banco

app = Flask(__name__)

@app.route("/herois", methods=['GET'])
def get_herois():
    herois = banco.listar_herois()
    return {"herois": herois}, 200

@app.route("/dano-nevoa", methods=["PUT"])
def processar():
    banco.dano_nevoa()
    return jsonify({"msg": "Turno processado"})

handler = app