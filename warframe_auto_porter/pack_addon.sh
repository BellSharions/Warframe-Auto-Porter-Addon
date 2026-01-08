#!/bin/bash

# Warframe Porter Addon Packer
# Usage: ./pack_addon.sh [version]
# Example: ./pack_addon.sh 0.49.0
# Yes I was lazy

set -e

if [ $# -eq 0 ]; then
    echo "Error: Version argument is required"
    echo "Usage: $0 <version>"
    echo "Example: $0 0.49.0"
    exit 1
fi

VERSION=$1
ARCHIVE_NAME="warframe-porter"
MANIFEST_FILE="blender_manifest.toml"

if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Warning: Version '$VERSION' doesn't match expected format (x.y.z)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Packing Warframe Porter addon version $VERSION..."

ORIGINAL_DIR="$(pwd)"

if [ -f "$MANIFEST_FILE" ]; then
    sed -i "s/^version = \".*\"/version = \"$VERSION\"/" "$MANIFEST_FILE"
else
    echo "$MANIFEST_FILE not found"
fi

echo "Creating zip archive: ${ARCHIVE_NAME}.zip"

zip -r "${ARCHIVE_NAME}.zip" . \
    -x "__pycache__/*" \
    -x "warframe-porter.py.backup" \
    -x "test_*.py" \
    -x "pack_addon.sh" \
    -x "*.zip"

echo "Created ${ARCHIVE_NAME}.zip with version $VERSION"
echo "Contents:"
unzip -l "${ARCHIVE_NAME}.zip" | tail -n +4 | head -n -2
