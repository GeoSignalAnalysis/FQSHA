#!/bin/bash

echo "🔧 Starting OpenQuake patch process..."

# Locate the file
OQ_PATH=$(python -c "import openquake; print(openquake.__path__[0])")
TARGET="$OQ_PATH/hazardlib/gsim/projects/acme_2019.py"

if [ -f "$TARGET" ]; then
  echo "📄 Found: $TARGET"
  echo "🔁 Replacing the problematic line..."

  # Use sed to perform the replacement
  sed -i 's/warnings.filterwarnings("ignore", category=np.RankWarning)/import warnings\nwarnings.filterwarnings("ignore")/' "$TARGET"

  echo "✅ Patch applied. You can review the file manually:"
  echo "   gedit \"$TARGET\""
else
  echo "❌ File not found: $TARGET"
fi

