from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

from bs4 import BeautifulSoup
import pandas as pd

# URL to scrape and name of the output table
url = "https://leetcode.com/studyplan/graph-theory/"
name_of_table = "Graph Theory"
path_to_chrome_driver = "D:\\Downloads\\chromedriver-win64\\chromedriver.exe"

# Setting Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")  # Enable incognito mode
# chrome_options.add_argument("--headless")  # Uncomment to run in background mode
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass Selenium detection

# Path to ChromeDriver
service = Service(path_to_chrome_driver)

# Start the browser session
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target URL
driver.get(url)

try:
    # Open URL and wait for the "Show tags" button to be clickable
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Show tags']"))
    )
    button.click()  # Click the button to reveal problem tags
    time.sleep(2)  # Wait for the page to load updated content
finally:
    # Get the full HTML of the page after interactions
    page = driver.page_source
    driver.quit()  # Close the browser session

# CSS class selectors for scraping specific elements
themes_class = r"w-full overflow-hidden rounded-lg border-[1.5px] border-lc-fill-02 dark:border-dark-lc-fill-02"
theme_name_class = r"text-[12px] font-medium"
problems_class = r"flex flex-col border-b-[1.5px] duration-300 last:border-b-0 border-lc-fill-02 dark:border-dark-lc-fill-02 hover:bg-lc-fill-02 dark:hover:bg-dark-lc-fill-02 cursor-pointer"
problem_name_class = r"truncate"
problem_tags_class = r"inline-flex min-h-[24px] min-w-[24px] max-w-full items-center rounded-full px-2 text-xs bg-lc-fill-02 dark:bg-dark-lc-fill-02 text-lc-text-primary dark:text-dark-lc-text-primary"

# Parse the page source using BeautifulSoup
soup = BeautifulSoup(page, features="html.parser")

# Find all theme blocks on the page
themes = soup.find_all("div", class_=themes_class)

# Initialize an empty DataFrame with specified column names and data types
df = pd.DataFrame(columns=["Index", "Name", "Theme", "Difficulty"])
df = df.astype({
    "Index": "int32",           # Integer type for problem indices
    "Name": "string",           # String type for problem names
    "Theme": "string",          # String type for themes
    "Difficulty": "category"    # Categorical type for difficulty levels
})

# Extract data from each theme block
for theme in themes:
    # Extract theme name
    theme_name = theme.find("div", class_=theme_name_class).text.strip()
    # Find all problems within the theme
    problems = theme.find_all("div", class_=problems_class)
    for problem in problems:
        # Extract problem details: name, index, and difficulty
        problem_name = problem.find("div", class_=problem_name_class).text.strip()
        problem_index = int(problem.find("span", class_=problem_tags_class).text.strip()[2:])
        problem_difficulty = problem.find("p").text.strip()
        
        # Add the extracted data as a new row in the DataFrame
        df.loc[len(df)] = [problem_index, problem_name, theme_name, problem_difficulty]

# Save the DataFrame to an Excel file
df.to_excel("results\\" + name_of_table + ".xlsx", index=False)
df.to_csv("results\\" + name_of_table + ".csv", index=False)
