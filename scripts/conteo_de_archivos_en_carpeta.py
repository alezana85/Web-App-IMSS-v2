from pathlib import Path
import csv


def main() -> None:
	# Ruta fija de prueba (lectura y exportación del CSV en la misma carpeta)
	base = Path(r"F:\01 TRABAJO\WALMART\02 IMSS\02 EMISIONES")
	if not base.exists() or not base.is_dir():
		print(f"Ruta no válida o inaccesible: {base}")
		return

	# Recorre solo subcarpetas inmediatas y cuenta archivos (no recursivo)
	rows = [("Registro Patronal", "Numero de Archivos")]
	for sub in sorted((p for p in base.iterdir() if p.is_dir()), key=lambda p: p.name):
		count = sum(1 for x in sub.iterdir() if x.is_file())
		rows.append((sub.name, count))

	# Exporta CSV en la misma ruta
	out_csv = base / "reporte_conteo_archivos.csv"
	with out_csv.open("w", newline="", encoding="utf-8-sig") as f:
		writer = csv.writer(f)
		writer.writerows(rows)

	print(f"Reporte generado: {out_csv}")


if __name__ == "__main__":
	main()

