#!/bin/bash

echo "🚀 Starting project setup..."

# Step 1: Create Virtual Environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment already exists."
fi

# Step 2: Activate Virtual Environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Step 3: Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Step 4: Install Dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found. Aborting setup."
    deactivate
    exit 1
fi

# Step 5: Apply Migrations
echo "📂 Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 6: Create Superuser (Optional)
read -p "Do you want to create a superuser? (y/n): " create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

# Step 7: Run the Server (Optional)
read -p "Do you want to start the server now? (y/n): " start_server
if [ "$start_server" = "y" ]; then
    python manage.py runserver
else
    echo "✅ Setup complete! Run 'python manage.py runserver' when ready."
fi

# Step 8: Deactivate virtual environment
deactivate
echo "🌟 All done!"
