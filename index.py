from flask import Flask, jsonify, render_template, redirect, url_for
import oracledb
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

def get_connection():
    
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn_string = os.getenv("DB_DSN")

    conn = oracledb.connect(
        user=user,
        password=password,
        dsn=dsn_string
    )

    return conn

def listar_herois():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_heroi, nome, classe, hp_atual, hp_max, status
        FROM TB_HEROIS
        ORDER BY id_heroi
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    herois = []

    for h in dados:
        herois.append({
            "id_heroi": h[0],
            "nome": h[1],
            "classe": h[2],
            "hp_atual": h[3],
            "hp_max": h[4],
            "status": h[5]
        })

    return herois

def dano_nevoa():
    with get_connection() as con:
        with con.cursor() as cur:  
            sql = """
                DECLARE

                    v_dano TB_HEROIS.hp_atual%TYPE := 10;
                    v_novo_hp TB_HEROIS.hp_atual%TYPE;

                BEGIN 

                    FOR i IN (
                        SELECT id_heroi, hp_atual
                        FROM TB_HEROIS
                        WHERE status = 'ATIVO'
                    ) 

                    LOOP

                        v_novo_hp := i.hp_atual - v_dano;

                        IF v_novo_hp <= 0 THEN

                            UPDATE TB_HEROIS
                            SET hp_atual = 0,
                            status = 'CAIDO'
                            WHERE id_heroi = i.id_heroi;

                        ELSE

                            UPDATE TB_HEROIS
                            SET hp_atual = v_novo_hp
                            WHERE id_heroi = i.id_heroi;

                        END IF;

                    END LOOP;

                END;
            """
            cur.execute(sql)
        con.commit()

@app.route("/")
def home():
    herois = listar_herois()
    return render_template("index.html", herois=herois)

@app.route("/herois")
def get_herois():
    return jsonify({"herois": listar_herois()})

@app.route("/dano-nevoa", methods=["POST"])
def processar():
    dano_nevoa()
    return jsonify({"msg": "Turno processado"})

if __name__ == "__main__":
    app.run(debug=True)