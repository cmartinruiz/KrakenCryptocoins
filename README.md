# KrakenCryptocoins
Top 20 KRAKEN cryptocoins comparison using Krakenex API

## Instructions:

### IMPORTANT: Required installations
Sign up and download the program in https://dashboard.ngrok.com/signup

Download git in https://git-scm.com/

### 1. Open a Google Colab Notebook:
#### Install Git
!apt-get install git -y

#### Clone this repository
repository = "https://github.com/cmartinruiz/KrakenCryptocoins.git"
!git clone $repository

#### Check the contents of the repository
!ls

#### Navigate to the repository
%cd KrakenCryptocoins/

#### Install required dependencies
!pip install -r requirements.txt

#### Execute the notebook
!jupyter nbconvert --to notebook --execute MartinRuiz.ipynb --output output_notebook.ipynb

##### IMPORTANT: You will be asked for an authorization token, copy and paste the authotoken from your ngrok account

