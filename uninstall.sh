#!/usr/bin/env bash
set -euo pipefail
echo "Asaan Lang hata rahe hain..."
rm -f /usr/local/bin/asaan "$HOME/.local/bin/asaan"
rm -rf /usr/local/share/asaan-lang "$HOME/.asaan-lang"
echo "✅ Hata di. (Python khud nahi hata — wo alag rehti hai.)"
