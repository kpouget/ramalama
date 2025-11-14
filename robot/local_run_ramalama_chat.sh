#!/bin/bash

cd ..

echo "Running with PID=$$"

RAMALAMA_PORT=8000
MCP_PORT=8001
exec ./bin/ramalama chat \
         --mcp http://127.0.0.1:$MCP_PORT/mcp \
         --url http://127.0.0.1:$RAMALAMA_PORT/
