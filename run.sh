#!/bin/bash
PID=$(lsof -t -i:8000)

if [ -z "$PID" ]; then
  echo "✅ Port 8000 is free."
else
  echo "🔪 Killing process on port 8000 (PID: $PID)..."
  kill -9 $PID
  echo "✅ Port 8000 is now free."
fi

source venv/bin/activate
uvicorn app.main:app --reload
