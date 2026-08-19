"""SQLite de documentos (acopio, calidad, pesaje). No es el almacén de sensores."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS recoleccion (
  id INTEGER PRIMARY KEY,
  fecha TEXT NOT NULL,
  codigo_productor TEXT,
  ruta TEXT,
  medida_tanque REAL,
  litros REAL,
  conductor TEXT,
  compartimiento TEXT,
  raw TEXT,
  UNIQUE (fecha, codigo_productor, compartimiento)
);
CREATE TABLE IF NOT EXISTS calidad (
  id INTEGER PRIMARY KEY,
  periodo_desde TEXT,
  periodo_hasta TEXT,
  codigo_productor TEXT,
  precio_litro REAL,
  proteina_pct REAL,
  grasa_pct REAL,
  solidos_pct REAL,
  ufc_x1000 REAL,
  frio_c REAL,
  precio_final_litro REAL,
  total_litros REAL,
  total_pagar REAL,
  raw TEXT,
  UNIQUE (periodo_desde, periodo_hasta)
);
CREATE TABLE IF NOT EXISTS calidad_litros_dia (
  fecha TEXT NOT NULL,
  litros REAL,
  calidad_id INTEGER,
  PRIMARY KEY (fecha, calidad_id)
);
CREATE TABLE IF NOT EXISTS pesaje (
  id INTEGER PRIMARY KEY,
  fecha TEXT NOT NULL,
  placa TEXT NOT NULL,
  litros_am REAL,
  litros_pm REAL,
  UNIQUE (fecha, placa)
);
"""


class Store:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def upsert_recoleccion(self, row: dict[str, Any]) -> None:
        self.conn.execute(
            """INSERT INTO recoleccion
               (fecha, codigo_productor, ruta, medida_tanque, litros,
                conductor, compartimiento, raw)
               VALUES (:fecha, :codigo_productor, :ruta, :medida_tanque, :litros,
                       :conductor, :compartimiento, :raw)
               ON CONFLICT(fecha, codigo_productor, compartimiento) DO UPDATE SET
                 litros=excluded.litros, medida_tanque=excluded.medida_tanque,
                 ruta=excluded.ruta, conductor=excluded.conductor, raw=excluded.raw
            """,
            row,
        )
        self.conn.commit()

    def upsert_calidad(self, row: dict[str, Any], litros_dia: list[dict]) -> None:
        cur = self.conn.execute(
            """INSERT INTO calidad
               (periodo_desde, periodo_hasta, codigo_productor, precio_litro,
                proteina_pct, grasa_pct, solidos_pct, ufc_x1000, frio_c,
                precio_final_litro, total_litros, total_pagar, raw)
               VALUES (:periodo_desde, :periodo_hasta, :codigo_productor, :precio_litro,
                       :proteina_pct, :grasa_pct, :solidos_pct, :ufc_x1000, :frio_c,
                       :precio_final_litro, :total_litros, :total_pagar, :raw)
               ON CONFLICT(periodo_desde, periodo_hasta) DO UPDATE SET
                 precio_litro=excluded.precio_litro,
                 proteina_pct=excluded.proteina_pct, grasa_pct=excluded.grasa_pct,
                 solidos_pct=excluded.solidos_pct, ufc_x1000=excluded.ufc_x1000,
                 precio_final_litro=excluded.precio_final_litro,
                 total_litros=excluded.total_litros, total_pagar=excluded.total_pagar
            """,
            row,
        )
        cid = cur.lastrowid
        if not cid:
            got = self.conn.execute(
                "SELECT id FROM calidad WHERE periodo_desde=? AND periodo_hasta=? AND codigo_productor=?",
                (row["periodo_desde"], row["periodo_hasta"], row["codigo_productor"]),
            ).fetchone()
            cid = got["id"] if got else None
        if cid:
            self.conn.execute("DELETE FROM calidad_litros_dia WHERE calidad_id=?", (cid,))
            for d in litros_dia:
                self.conn.execute(
                    "INSERT INTO calidad_litros_dia (fecha, litros, calidad_id) VALUES (?,?,?)",
                    (d["fecha"], d["litros"], cid),
                )
        self.conn.commit()

    def upsert_pesaje(self, row: dict[str, Any]) -> None:
        self.conn.execute(
            """INSERT INTO pesaje (fecha, placa, litros_am, litros_pm)
               VALUES (:fecha, :placa, :litros_am, :litros_pm)
               ON CONFLICT(fecha, placa) DO UPDATE SET
                 litros_am=excluded.litros_am, litros_pm=excluded.litros_pm
            """,
            row,
        )
        self.conn.commit()

    def last_recoleccion(self) -> dict | None:
        r = self.conn.execute("SELECT * FROM recoleccion ORDER BY fecha DESC LIMIT 1").fetchone()
        return dict(r) if r else None

    def last_calidad(self) -> dict | None:
        r = self.conn.execute("SELECT * FROM calidad ORDER BY periodo_hasta DESC LIMIT 1").fetchone()
        return dict(r) if r else None

    def pesaje_ultimo_dia(self) -> list[dict]:
        day = self.conn.execute("SELECT MAX(fecha) AS d FROM pesaje").fetchone()
        if not day or not day["d"]:
            return []
        rows = self.conn.execute(
            "SELECT * FROM pesaje WHERE fecha=? ORDER BY placa", (day["d"],)
        ).fetchall()
        return [dict(x) for x in rows]

    def calidad_series(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT periodo_hasta, proteina_pct, grasa_pct, solidos_pct, ufc_x1000 FROM calidad ORDER BY periodo_hasta"
        ).fetchall()
        return [dict(x) for x in rows]
