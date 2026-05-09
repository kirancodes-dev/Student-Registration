#!/usr/bin/env bash
# =============================================================
#  Student Hub – Quick-start script
#  Usage:  chmod +x run.sh && ./run.sh
# =============================================================
set -e

echo ""
echo "  🎓  Student Hub – Setup & Run"
echo "  ================================"
echo ""

# 1. Create .env from example if it doesn't exist
if [ ! -f .env ]; then
  cp .env.example .env
  echo "  ✔  Created .env (edit it with your MySQL credentials)"
  echo ""
fi

# 2. Create virtual environment
if [ ! -d venv ]; then
  echo "  ▶  Creating virtual environment..."
  python3 -m venv venv
fi

# 3. Activate and install deps
echo "  ▶  Installing Python dependencies..."
source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# 4. Initialise DB (create tables + seed admin)
echo "  ▶  Initialising database..."
flask --app app init-db

# 5. Start development server
echo ""
echo "  ✅  All set! Starting Flask on http://localhost:5000"
echo "      Admin panel: http://localhost:5000/admin"
echo "      Admin credentials: admin@school.com / Admin123!"
echo ""
flask --app app run --debug --port 5000
