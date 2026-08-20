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
CREATE TABLE IF NOT EXISTS sitio (
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL UNIQUE,
  usuario TEXT
);
CREATE TABLE IF NOT EXISTS potrero (
  id INTEGER PRIMARY KEY,
  sitio_id INTEGER NOT NULL,
  numero TEXT NOT NULL,
  nombre TEXT NOT NULL,
  geojson TEXT,
  UNIQUE (sitio_id, numero)
);
CREATE TABLE IF NOT EXISTS pastoreo_mov (
  id INTEGER PRIMARY KEY,
  potrero_id INTEGER NOT NULL,
  fecha TEXT NOT NULL,
  momento TEXT,
  tipo TEXT NOT NULL,
  mensaje TEXT
);
CREATE TABLE IF NOT EXISTS fertilizacion (
  id INTEGER PRIMARY KEY,
  potrero_id INTEGER NOT NULL,
  fecha TEXT NOT NULL,
  abono TEXT,
  bultos REAL,
  mensaje TEXT
);
CREATE TABLE IF NOT EXISTS ingest_log (
  id INTEGER PRIMARY KEY,
  message_id TEXT NOT NULL UNIQUE,
  kind TEXT,
  fecha TEXT,
  status TEXT,
  detail TEXT
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

    def last_recoleccion_fecha(self) -> str | None:
        r = self.conn.execute("SELECT MAX(fecha) AS d FROM recoleccion").fetchone()
        return r["d"] if r and r["d"] else None

    def already_ingested(self, message_id: str) -> bool:
        r = self.conn.execute(
            "SELECT 1 FROM ingest_log WHERE message_id=? AND status='ok'",
            (message_id,),
        ).fetchone()
        return r is not None

    def log_ingest(self, message_id: str, kind: str, fecha: str | None, status: str, detail: str = "") -> None:
        self.conn.execute(
            """INSERT INTO ingest_log (message_id, kind, fecha, status, detail)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(message_id) DO UPDATE SET
                 status=excluded.status, detail=excluded.detail, fecha=excluded.fecha
            """,
            (message_id, kind, fecha, status, detail[:500]),
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

    def ensure_sitio(self, nombre: str, usuario: str | None = None) -> int:
        row = self.conn.execute("SELECT id FROM sitio WHERE nombre=?", (nombre,)).fetchone()
        if row:
            return row["id"]
        cur = self.conn.execute(
            "INSERT INTO sitio (nombre, usuario) VALUES (?, ?)", (nombre, usuario)
        )
        self.conn.commit()
        return cur.lastrowid

    def sitios_de(self, usuario: str | None) -> list[dict]:
        if usuario:
            rows = self.conn.execute(
                "SELECT * FROM sitio WHERE usuario=? OR usuario IS NULL ORDER BY nombre",
                (usuario,),
            ).fetchall()
        else:
            rows = self.conn.execute("SELECT * FROM sitio ORDER BY nombre").fetchall()
        return [dict(r) for r in rows]

    def upsert_potrero(self, sitio_id: int, numero: str, nombre: str, geojson: str | None) -> int:
        self.conn.execute(
            """INSERT INTO potrero (sitio_id, numero, nombre, geojson)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(sitio_id, numero) DO UPDATE SET
                 nombre=excluded.nombre,
                 geojson=COALESCE(excluded.geojson, potrero.geojson)
            """,
            (sitio_id, str(numero), nombre, geojson),
        )
        self.conn.commit()
        row = self.conn.execute(
            "SELECT id FROM potrero WHERE sitio_id=? AND numero=?",
            (sitio_id, str(numero)),
        ).fetchone()
        return row["id"]

    def potreros(self, sitio_id: int) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM potrero WHERE sitio_id=? ORDER BY CAST(numero AS INTEGER), numero",
            (sitio_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def find_potrero(self, sitio_id: int, token: str) -> dict | None:
        token = (token or "").strip().lower()
        if not token:
            return None
        rows = self.potreros(sitio_id)
        for r in rows:
            if str(r["numero"]).lower() == token or r["nombre"].lower() == token:
                return r
        for r in rows:
            if token in r["nombre"].lower() or r["nombre"].lower() in token:
                return r
        return None

    def add_movimiento(self, potrero_id: int, fecha: str, momento: str | None, tipo: str, mensaje: str) -> None:
        self.conn.execute(
            """INSERT INTO pastoreo_mov (potrero_id, fecha, momento, tipo, mensaje)
               VALUES (?, ?, ?, ?, ?)""",
            (potrero_id, fecha, momento, tipo, mensaje),
        )
        self.conn.commit()

    def add_fertilizacion(
        self, potrero_id: int, fecha: str, abono: str | None, bultos: float | None, mensaje: str
    ) -> None:
        self.conn.execute(
            """INSERT INTO fertilizacion (potrero_id, fecha, abono, bultos, mensaje)
               VALUES (?, ?, ?, ?, ?)""",
            (potrero_id, fecha, abono, bultos, mensaje),
        )
        self.conn.commit()

    def historial_potrero(self, potrero_id: int, limit: int = 5) -> list[dict]:
        rows = self.conn.execute(
            """SELECT fecha, momento, tipo, mensaje FROM pastoreo_mov
               WHERE potrero_id=? ORDER BY fecha DESC, id DESC LIMIT ?""",
            (potrero_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def fertilizaciones_potrero(self, potrero_id: int, limit: int = 5) -> list[dict]:
        rows = self.conn.execute(
            """SELECT fecha, abono, bultos FROM fertilizacion
               WHERE potrero_id=? ORDER BY fecha DESC, id DESC LIMIT ?""",
            (potrero_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def ocupacion(self, sitio_id: int) -> int | None:
        """Última entrada del sitio (potrero_id) si no hay salida posterior."""
        row = self.conn.execute(
            """SELECT m.potrero_id, m.tipo, m.fecha, m.id
               FROM pastoreo_mov m
               JOIN potrero p ON p.id = m.potrero_id
               WHERE p.sitio_id=?
               ORDER BY m.fecha DESC, m.id DESC LIMIT 1""",
            (sitio_id,),
        ).fetchone()
        if not row:
            return None
        return row["potrero_id"] if row["tipo"] == "entrada" else None

    def calidad_series(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT periodo_hasta, proteina_pct, grasa_pct, solidos_pct, ufc_x1000 FROM calidad ORDER BY periodo_hasta"
        ).fetchall()
        return [dict(x) for x in rows]
