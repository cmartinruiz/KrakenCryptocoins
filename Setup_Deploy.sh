#!/bin/bash

# Clone the repository
echo "Cloning the repository..."
git clone https://github.com/cmartinruiz/KrakenCryptocoins.git
cd KrakenCryptocoins || exit

# Create and activate a virtual environment
echo "Creating and activating virtual environment..."
python -m venv myenv
source myenv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Run Kraken_Data.py (data processing script)
echo "Running Kraken_Data.py..."
python Kraken_Data.py
if [ $? -ne 0 ]; then
    echo "Failed to execute Kraken_Data.py. Exiting."
    exit 1
fi

# Run Kraken_Visualization.py (visualization script)
echo "Running Kraken_Visualization.py..."
python Kraken_Visualization.py
if [ $? -ne 0 ]; then
    echo "Failed to execute Kraken_Visualization.py. Exiting."
    exit 1
fi

# Run unit tests
echo "Running unit tests..."
python -m unittest discover
if [ $? -ne 0 ]; then
    echo "Unit tests failed. Exiting."
    exit 1
fi

# Create a Procfile for Heroku
echo "Creating Procfile..."
echo "web: python Kraken_Data.py" > Procfile

# Install Heroku CLI if not installed
if ! command -v heroku &> /dev/null
then
    echo "Installing Heroku CLI..."
    curl https://cli-assets.heroku.com/install.sh | sh
fi

# Login to Heroku
echo "Logging into Heroku..."
heroku login

# Create a new Heroku app
echo "Creating a new Heroku app..."
heroku create kraken_app

# Deploy to Heroku
echo "Deploying to Heroku..."
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# Open the Heroku app
echo "Opening the Heroku app..."
heroku open

echo "Setup and deployment complete!"
