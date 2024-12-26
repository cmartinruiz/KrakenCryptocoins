@echo off

REM Check if repository folder exists
if exist KrakenCryptocoins (
    echo "Directory already exists. Deleting it..."
    rmdir /s /q KrakenCryptocoins
)
echo Cloning the repository...
git clone https://github.com/cmartinruiz/KrakenCryptocoins.git
cd KrakenCryptocoins || exit /b

REM Create and activate a virtual environment
echo Creating and activating virtual environment...
python -m venv myenv
call myenv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo "Failed to activate virtual environment. Exiting."
    exit /b
)

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo "Failed to install required packages. Exiting."
    exit /b
)

REM Run Kraken_Data.py (data processing script)
echo Running Kraken_Data.py...
python Kraken_Data.py
if %ERRORLEVEL% NEQ 0 (
    echo "Failed to execute Kraken_Data.py. Exiting."
    exit /b
)

REM Run Kraken_Visualization.py (visualization script)
echo Running Kraken_Visualization.py...
python Kraken_Visualization.py
if %ERRORLEVEL% NEQ 0 (
    echo "Failed to execute Kraken_Visualization.py. Exiting."
    exit /b
)

REM Run unit tests
echo Running unit tests...
python -m unittest discover
if %ERRORLEVEL% NEQ 0 (
    echo "Unit tests failed. Exiting."
    exit /b
)

REM Create a Procfile for Heroku
echo Creating Procfile...
echo web: python Kraken_Data.py > Procfile

REM Check for Heroku CLI
where heroku >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo "Heroku CLI is not installed. Please install it from https://devcenter.heroku.com/articles/heroku-cli."
    pause
    exit /b
)

REM Login to Heroku
echo Logging into Heroku...
heroku login

REM Create a new Heroku app
echo Creating a new Heroku app...
heroku create kraken_app

REM Deploy to Heroku
echo Deploying to Heroku...
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

REM Open the Heroku app
echo Opening the Heroku app...
heroku open

echo Setup and deployment complete!
pause
