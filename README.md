# Visualize your Music Interval Training
- Teoria.com is a website which provides customized music interval training. It also allows users to save their exercises and scores.  Unfornately, these training statistics are only represented in a tabular format which limits a users understanding of their training progess which may lead to inefficient or all together ineffective training going unnoticed.
- The goal of this project is to consume a users Teoria training data and produce informative and interactive visualizations. These graphs will give a user a better understanding of the success of their musical training and help them make better choices in training regiments. 
- The users training data will be webscrapped with Python and Selenium
- Interactive visualizations will be created with Plotly Dash.

## Setting up the program 
1. Navigate to the project folder in command prompt and execute the following command to install the packages required for this program:
```
conda create --name teoria_viz --file requirements.txt
conda activate teoria_viz
# Or just add the required packages to your current Anaconda environment with:
conda install --yes --file requirements.txt
```
2. Create an file called ".env" add the following lines to the file:
```
TEORIA_USERNAME = "your_username"
TEORIA_PASSWORD = "your_password"
```
3. Unzip the "chromedriver_win32.zip" file and put the chromedriver.exe file in the root of this project folder
4. Run the main.py file
```
python main.py
```