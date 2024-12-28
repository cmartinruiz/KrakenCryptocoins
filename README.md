# KrakenCryptocoins
Top 20 KRAKEN cryptocoins comparison using Krakenex API

## Instructions:

### IMPORTANT: Required installations
Sign up in https://dashboard.ngrok.com/signup and downoad the platform
Download git in https://git-scm.com/

### 1. Open a Google Colab and connect with GitHub:
!apt-get install git -y

repository = "https://github.com/cmartinruiz/KrakenCryptocoins.git"

!git clone $repository


### 2. Install required packages:
%cd KrakenCryptocoins/

!pip install -r requirements.txt


### 3. Run the main file
!jupyter nbconvert --to notebook --execute MartinRuiz.ipynb --output output_notebook.ipynb

