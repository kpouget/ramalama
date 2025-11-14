#!/bin/bash

RAMALAMA_PORT=8000
ssh -L $RAMALAMA_PORT:localhost:$RAMALAMA_PORT mac \
    /Users/kevinpouget/system/bin/ramalama serve \
      --tool \
      --port=$RAMALAMA_PORT \
        $(cat ./model.txt)
