import os
import csv

DIRECTORI = "../../precip.MIROC5.RCP60.2006-2100.SDSM_REJ"
EXTENSIO = ".dat"
LOG_FILE = "resultat_PAS2.log"

def validar_format_arxius(directori, extensio):
    if not os.path.exists(directori):
        print(f"Error: El directori especificat no existeix: {directori}")
        return

    formats = []
    total_columns = 0
    delimiters_count = {}

    for nom_arxiu in os.listdir(directori):
        if nom_arxiu.endswith(extensio):
            ruta_arxiu = os.path.join(directori, nom_arxiu)
            with open(ruta_arxiu, "r", encoding="utf-8") as arxiu:
                delimitador = determinar_delimitador(arxiu)
                arxiu.seek(0)  # Reset file pointer to the beginning
                lector = csv.reader(arxiu, delimiter=delimitador)
                primer_fila = next(lector, None)
                if primer_fila:
                    primer_fila = [col for col in primer_fila if col]
                    format_actual = (len(primer_fila), primer_fila, delimitador)
                    formats.append((nom_arxiu, format_actual))
                    total_columns += len(primer_fila)
                    if delimitador in delimiters_count:
                        delimiters_count[delimitador] += 1
                    else:
                        delimiters_count[delimitador] = 1

    if not formats:
        print("No s'han trobat arxius amb l'extensió especificada.")
        return

    format_base = formats[0][1]
    diferencies = []

    for nom_arxiu, format_actual in formats:
        if format_actual != format_base:
            diferencies.append((nom_arxiu, format_actual))

    total_files = len(formats)
    bad_files = len(diferencies)
    good_files = total_files - bad_files

    with open(LOG_FILE, "w", encoding="utf-8") as log:
        if diferencies:
            log.write("\nFormats diferents detectats:\n")
            for nom_arxiu, format_actual in diferencies:
                log.write(f"Arxiu: {nom_arxiu} | Columnes: {format_actual[0]} | Primeres dades: {format_actual[1]} | Delimitador: '{format_actual[2]}'\n")
        else:
            log.write("Tots els arxius tenen el mateix format.\n")

        log.write(f"\nTotal d'arxius: {total_files}\n")
        log.write(f"Arxius correctes: {good_files} ({(good_files / total_files) * 100:.2f}%)\n")
        log.write(f"Arxius incorrectes: {bad_files} ({(bad_files / total_files) * 100:.2f}%)\n")

        # Print the total number of columns and delimiters
        log.write(f"\nTotal columnes en tots els arxius: {total_columns}\n")
        log.write("Total delimitadors en tots els arxius:\n")
        for delimitador, count in delimiters_count.items():
            log.write(f"Delimitador '{delimitador}': {count} vegades\n")

def determinar_delimitador(arxiu):
    delimitadors = [',', ';', '\t', ' ']
    primer_fila = arxiu.readline()
    for delimitador in delimitadors:
        if delimitador in primer_fila:
            return delimitador
    return ','

if __name__ == "__main__":
    validar_format_arxius(DIRECTORI, EXTENSIO)