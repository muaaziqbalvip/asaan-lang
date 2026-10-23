#!/usr/bin/env bash
# Asaan Lang installer — Linux / macOS
# Python ki tarah system par 'asaan' command lagaata hai.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ Pehle Python 3 install karo: https://www.python.org/downloads/"
  echo "   (Asaan Lang ke andar Python engine chalti hai, jaise Java ke andar JVM.)"
  exit 1
fi

PY="$(command -v python3)"
VER="$("$PY" -c 'import sys; print("%d.%d"%sys.version_info[:2])')"
echo "🐍 Python $VER mili: $PY"

# Install location — system-wide agar likh sakte hain, warna user home
if [ -w /usr/local/share ] && [ -w /usr/local/bin ]; then
  HOME_DIR="/usr/local/share/asaan-lang"
  BIN="/usr/local/bin/asaan"
else
  HOME_DIR="${ASAAN_HOME:-$HOME/.asaan-lang}"
  mkdir -p "$HOME/.local/bin"
  BIN="$HOME/.local/bin/asaan"
fi

echo "📦 Files copy: $HOME_DIR"
rm -rf "$HOME_DIR"
mkdir -p "$HOME_DIR"
cp "$HERE/asaan.py" "$HERE/studio.py" "$HERE/README.md" "$HOME_DIR/"
cp -R "$HERE/studio" "$HERE/examples" "$HOME_DIR/"
[ -d "$HERE/web" ] && cp -R "$HERE/web" "$HOME_DIR/" || true
# optional extras
[ -f "$HERE/pyproject.toml" ] && cp "$HERE/pyproject.toml" "$HOME_DIR/" || true

cat > "$BIN" <<EOF
#!/usr/bin/env bash
export ASAAN_HOME="$HOME_DIR"
exec "$PY" "$HOME_DIR/asaan.py" "\$@"
EOF
chmod +x "$BIN" "$HOME_DIR/asaan.py" "$HOME_DIR/studio.py"

# PATH check for ~/.local/bin
if [ "$BIN" = "$HOME/.local/bin/asaan" ]; then
  case ":$PATH:" in
    *":$HOME/.local/bin:"*) ;;
    *)
      SHELL_NAME="$(basename "${SHELL:-bash}")"
      RC=""
      [ "$SHELL_NAME" = "zsh" ] && RC="$HOME/.zshrc"
      [ "$SHELL_NAME" = "bash" ] && RC="$HOME/.bashrc"
      [ -z "$RC" ] && RC="$HOME/.profile"
      echo "" >> "$RC"
      echo "# Asaan Lang" >> "$RC"
      echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC"
      echo "ℹ️  PATH mein ~/.local/bin add kiya: $RC"
      echo "   Nayi terminal kholo, ya:  export PATH=\"\$HOME/.local/bin:\$PATH\""
      export PATH="$HOME/.local/bin:$PATH"
      ;;
  esac
fi

echo
echo "✅ Asaan Lang install ho gayi!  🇵🇰"
echo "   Developer: Muaaz Iqbal  ·  MIT License"
echo
echo "   Ab Python ki tarah kahin se bhi:"
echo "     asaan                  # REPL (interactive)"
echo "     asaan meri.asaan       # program chalao"
echo "     asaan -e 'likho 1+2'   # ek line"
echo "     asaan --studio         # playground"
echo "     asaan --version"
echo
"$PY" "$HOME_DIR/asaan.py" --version
echo "   Home: $HOME_DIR"
echo "   Command: $BIN"
echo
echo "Hatane ke liye:  bash $HERE/uninstall.sh"
