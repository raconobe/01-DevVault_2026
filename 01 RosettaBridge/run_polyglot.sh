#!/bin/bash
# Cargar explícitamente las variables de entorno de Rust/Cargo
[ -f "$HOME/.cargo/env" ] && source "$HOME/.cargo/env"

EXT="${1##*.}"
FILE="$1"
DIR="${2}"
NAME="${3}"

OUT_DIR="/home/prolog/Desktop/01 DevVault_2026/bin"
mkdir -p "$OUT_DIR"

case "$EXT" in
    py) python3 "$FILE" ;;
    js) node "$FILE" ;;
    cpp) g++ "$FILE" -o "$OUT_DIR/$NAME" && "$OUT_DIR/$NAME" ;;
    rs) rustc "$FILE" -o "$OUT_DIR/$NAME" && "$OUT_DIR/$NAME" ;;
    java) javac "$FILE" -d "$OUT_DIR" && java -cp "$OUT_DIR" "$NAME" ;;
    f90) gfortran "$FILE" -o "$OUT_DIR/$NAME" && "$OUT_DIR/$NAME" ;;
    cob) cobc -x -free "$FILE" -o "$OUT_DIR/$NAME" && "$OUT_DIR/$NAME" ;;
    *) echo "⚠️ Extensión no soportada." ;;
esac
