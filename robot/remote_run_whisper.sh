#!/bin/bash

WHISPER_PORT=8086
ssh -L $WHISPER_PORT:localhost:$WHISPER_PORT mac \
    \$HOME/whisper/whisper.cpp/build/bin/whisper-server \
    --host 0.0.0.0 \
    --port $WHISPER_PORT \
    --model \$HOME/models/ggml-medium.bin
