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

# Run the main script
echo "Running the main script..."
python martinruiz.py

# Run unit tests
echo "Running unit tests..."
python -m unittest discover

# Create a Procfile for Heroku
echo "Creating Procfile..."
echo "web: python martinruiz.py" > Procfile

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
