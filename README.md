# Visualize your Music Interval Training
- Teoria.com is a website which provides customized music interval training. It also allows users to save their exercises and scores.  Unfornately, these training statistics are only represented in a tabular format which limits a users understanding of their training progess which may lead to inefficient or all together ineffective training going unnoticed.
- The goal of this project is to consume a users Teoria training data and produce informative and interactive visualizations. These graphs will give a user a better understanding of the success of their musical training and help them make better choices in training regiments. 
- The users training data will be webscrapped with Python and Selenium
- Interactive visualizations will be created with Plotly Dash.

## Usage
1. Navigate to the project folder in command prompt and execute the following command to install the packages required for this program
```
pip install -r requirements.txt
```
2. Create a .env file and add 2 lines to it as such:
```
username = ""
password = ""
```