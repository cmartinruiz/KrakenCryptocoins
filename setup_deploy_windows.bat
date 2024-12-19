@echo off

REM Clone the repository
echo Cloning the repository...
git clone https://github.com/cmartinruiz/KrakenCryptocoins.git
cd KrakenCryptocoins || exit /b

REM Create and activate a virtual environment
echo Creating and activating virtual environment...
python -m venv myenv
call myenv\Scripts\activate

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

REM Run the main script
echo Running the main script...
python martinruiz.py

REM Run unit tests
echo Running unit tests...
python -m unittest discover

REM Create a Procfile for Heroku
echo Creating Procfile...
echo web: python martinruiz.py > Procfile

REM Install Heroku CLI if not installed
where heroku >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Heroku CLI...
    curl https://cli-assets.heroku.com/install.sh | sh
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
