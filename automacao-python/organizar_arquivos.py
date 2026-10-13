#!/usr/bin/env python3
"""Organiza uma pasta bagunçada (tipo Downloads) separando os arquivos por tipo.

Uso:
    python organizar_arquivos.py ~/Downloads            # só mostra o que faria
    python organizar_arquivos.py ~/Downloads --executar # move de verdade
"""
import argparse, csv, shutil, datetime
from pathlib import Path

TIPOS = {
    "Imagens": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"},
    "Documentos": {".pdf", ".doc", ".docx", ".odt", ".txt", ".rtf"},
    "Planilhas": {".xls", ".xlsx", ".ods", ".csv"},
    "Apresentacoes": {".ppt", ".pptx", ".odp"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv"},
    "Audios": {".mp3", ".wav", ".ogg", ".m4a", ".opus"},
    "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Instaladores": {".exe", ".msi", ".deb", ".apk", ".dmg"},
}

def pasta_destino(arq: Path) -> str:
    ext = arq.suffix.lower()
    for nome, exts in TIPOS.items():
        if ext in exts:
            return nome
    return "Outros"

def nome_livre(destino: Path) -> Path:
    # se já existir um arquivo com o mesmo nome, coloca (1), (2)...
    if not destino.exists():
        return destino
    i = 1
    while True:
        novo = destino.with_name(f"{destino.stem} ({i}){destino.suffix}")
        if not novo.exists():
            return novo
        i += 1

def main():
    ap = argparse.ArgumentParser(description="Organiza arquivos por tipo.")
    ap.add_argument("pasta", type=Path)
    ap.add_argument("--executar", action="store_true", help="move os arquivos (sem isso é só simulação)")
    a = ap.parse_args()
    pasta = a.pasta.expanduser().resolve()
    if not pasta.is_dir():
        raise SystemExit(f"Pasta não encontrada: {pasta}")

    movidos = []
    for arq in sorted(p for p in pasta.iterdir() if p.is_file() and not p.name.startswith(".")):
        if arq.name.startswith("relatorio-organizacao"):
            continue
        destino = nome_livre(pasta / pasta_destino(arq) / arq.name)
        print(f"{arq.name}  ->  {destino.parent.name}/{destino.name}")
        if a.executar:
            destino.parent.mkdir(exist_ok=True)
            shutil.move(str(arq), destino)
        movidos.append((arq.name, destino.parent.name, destino.name))

    if not movidos:
        print("Nada pra organizar.")
        return
    if a.executar:
        rel = pasta / f"relatorio-organizacao-{datetime.datetime.now():%Y%m%d-%H%M%S}.csv"
        with rel.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["arquivo_original", "pasta", "nome_final"])
            w.writerows(movidos)
        print(f"\n{len(movidos)} arquivos movidos. Relatório: {rel.name}")
    else:
        print(f"\n{len(movidos)} arquivos seriam movidos. Rode de novo com --executar pra valer.")

if __name__ == "__main__":
    main()
