#!/bin/sh
set -e

echo "[lpm] package manager by nesantime"


if [ -n "$TERMUX_VERSION" ] || [ -d "/data/data/com.termux" ]; then
    INSTALL_BASE="$HOME/.local/share/lpm/lpm_"
    BIN_DIR="$PREFIX/bin"
    MODE="USER (TERMUX)"
else
    INSTALL_BASE="$HOME/.local/share/lpm/lpm_"
    BIN_DIR="$HOME/.local/bin"
    MODE="USER LINUX"
fi

echo "[lpm] Mode: $MODE"

command -v python3 >/dev/null 2>&1 || {
    echo "[ERROR] python3 no está instalado"
    exit 1
}

mkdir -p "$INSTALL_BASE"
mkdir -p "$BIN_DIR"

echo "[lpm] Copiando archivos..."
cp -r source "$INSTALL_BASE/"
cp lpm.py "$INSTALL_BASE/"

echo "[lpm] Creando entorno virtual..."
python3 -m venv "$INSTALL_BASE/lpm_venv"

VENV_PY="$INSTALL_BASE/lpm_venv/bin/python"

echo "[lpm] Instalando dependencias..."
"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install requests brotli

echo "[lpm] Creando launcher..."

cat > "$BIN_DIR/lpm" <<EOF
#!/bin/sh
exec "$VENV_PY" "$INSTALL_BASE/lpm.py" "\$@"
EOF

chmod +x "$BIN_DIR/lpm"

echo
echo "[ OK ] lpm instalado correctamente"
