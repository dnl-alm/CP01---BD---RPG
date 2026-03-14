import oracledb
import os

def get_conexao():
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=os.getenv("DB_DSN")
    )

def insere_heroi(heroi):
    with get_conexao() as con:
        with con.cursor() as cur:
            sql = """
                insert into TB_HEROIS(nome, classe, hp_atual, hp_max, status)
                values(:nome, :classe, :hp_atual, :hp_max, :status)
                returning id_heroi into :id
            """

            new_var = cur.var(oracledb.NUMBER)
            heroi['id'] = new_var

            cur.execute(sql, heroi)
            heroi['id'] = new_var.getvalue()[0]

        con.commit()

def atualiza_heroi(heroi):
    with get_conexao() as con:
        with con.cursor() as cur:
            sql = """
                UPDATE TB_HEROIS
                SET nome = :nome,
                    classe = :classe,
                    hp_atual = :hp_atual,
                    hp_max = :hp_max,
                    status = :status
                WHERE id_heroi = :id
            """
            cur.execute(sql, heroi)

def deleta_heroi(id_heroi):
    with get_conexao() as con:
        with con.cursor() as cur:
            sql = "DELETE FROM TB_HEROIS WHERE id_heroi = :id"
            cur.execute(sql, {"id": id_heroi})

        con.commit()

def dano_nevoa():
    with get_conexao() as con:
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

def listar_herois():
    with get_conexao() as con:
        with con.cursor() as cur:
            sql = """
                SELECT id_heroi, nome, classe, hp_atual, hp_max, status
                FROM TB_HEROIS
                ORDER BY id_heroi
            """
            cur.execute(sql)
            dados = cur.fetchall()

            colunas = [d[0].lower() for d in cur.description]

            return [dict(zip(colunas, linha)) for linha in dados]