#!/bin/bash
# Build Instruments Serif variable font with fontc

set -e

SOURCES_DIR="sources"
FONTS_DIR="fonts"

mkdir -p "$FONTS_DIR"

fontc "$SOURCES_DIR/InstrumentsSerif.designspace" -o "$FONTS_DIR/InstrumentsSerif[wght].ttf"

echo "Built $FONTS_DIR/InstrumentsSerif[wght].ttf"
