# LeetCode Study Plan Scraper

This project is a web scraper that extracts information from the LeetCode Study Plan pages and saves the problem details (such as problem index, name, theme, and difficulty) into an Excel file.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup
- Pandas
- Chrome WebDriver

## Setup

1. Install required libraries:
   ```
   pip install selenium
   pip install bs4
   pip install pandas
   ```

2. Download Chrome WebDriver from [here](https://developer.chrome.com/docs/chromedriver/downloads/) and specify the path in the `path_to_chrome_driver` variable.

3. Update the `url` and `name_of_table` variables to point to the desired LeetCode Study Plan page if needed.

## Usage

1. Clone the repository or download the script.
2. Run the script:
   ```
   python scrap_leetcode.py
   ```
3. The script will scrape the problem data from the LeetCode page and save it as an Excel file in the `results` directory. The filename will be based on the theme (e.g., `Graph Theory.xlsx`).

## Notes

- The script uses incognito mode to run the browser session and bypass Selenium detection.
- If you want the script to run in headless mode (without opening a browser window), uncomment the `chrome_options.add_argument("--headless")` line.
