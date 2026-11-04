from pathlib import Path
import duckdb

DATA_PATH = Path(__file__).parent / "data"
# skapar mappen om den inte existerar och skapar inte den igen om vi kör om skriptet
DATA_PATH.mkdir(exist_ok=True)


def query_duckdb(sql_code: str, parameters = None):
    # Funktionen tar emot en SQL-sträng och valfria parametrar
    # (parameters är t.ex. en lista med värden som ersätter ? i frågan)

    with duckdb.connect(DATA_PATH / "movies.duckdb") as conn:
        # Öppnar en anslutning till databasfilen "movies.duckdb" i mappen DATA_PATH. "with" ser till att anslutningen
        # stängs automatiskt när blocket är klart, även vid fel.

        cursor = conn.execute(sql_code, parameters=parameters)
        # Kör SQL-frågan på anslutningen. Om parametrar skickas med sätts de in säkert i frågan (skyddar mot SQL-injektion).
        # Resultatet hamnar i "cursor", som man kan hämta rader från.

        if sql_code.strip().casefold().startswith(("select", "from", "desc", "pragma")):
            return cursor.df()


