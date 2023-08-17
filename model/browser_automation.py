from dateutil.relativedelta import relativedelta
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Desktop.Clipboard import Clipboard
from RPA.Browser.Selenium import Selenium
from datetime import date, datetime
from RPA.Desktop import Desktop
from model.helpers import helpers as he
import requests
import time
import sys
import re

class browser_automation:

    NyPosts_months = {
        "Jan.":"1",
        "Feb.":"2",
        "March":"3",
        "April":"4",
        "May":"5",
        "June":"6",
        "July":"7",
        "Aug.":"8",
        "Sept.":"9",
        "Oct.":"10",
        "Nov.":"11",
        "Dic.":"12"
    }

    # Cloud Deployment
    def __init__(self, output_folder):
        self.browser_lib = Selenium()
        self.wi = WorkItems()
        self.desktop_lib = Desktop()
        self.clip = Clipboard()
        self.wi.get_input_work_item()
        self.search_phrase = self.wi.get_work_item_variable("search_phrase")
        self.sections = self.wi.get_work_item_variable("sections")
        self.months_number = self.wi.get_work_item_variable("months_number")
        self.output_folder = output_folder
        self.url = "https://www.nytimes.com/"

    # # Local Run
    # def __init__(self, output_folder):
    #     self.browser_lib = Selenium()
    #     self.desktop_lib = Desktop()
    #     self.clip = Clipboard()
    #     self.search_phrase = "Argentina"
    #     self.sections = ["Arts", "Business", "U.S."]
    #     self.months_number = 1
    #     self.output_folder = output_folder
    #     self.url = "https://www.nytimes.com/"

    def validate_inputs(self, search_phrase: str, sections: list, months_number: int):
        """
        Validate input variables are not empty
        """
        try:
            # Handle empty inputs
            he.check_if_empty(search_phrase, "search_phrase")
            he.check_if_empty(sections, "sections")
            if months_number < 0:
                raise Exception(f"The {months_number} input must be positive")
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')


    def open_website(self, url: str):
        """
        Open browser
        """
        try:
            self.browser_lib.open_available_browser(url, maximized=True)
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        
        
    def search_news(self, search_phrase: str):
        """
        Click on the search bar and type the input phrase
        """
        try:
            self.browser_lib.click_element("xpath: //*[contains(text(), \"Continue\")]")
            self.browser_lib.click_element("xpath: //*[@aria-controls=\"search-input\"]")
            locator = "xpath: //*[@aria-label=\"Search the new york times\"]"
            self.browser_lib.input_text(locator, search_phrase)
            self.browser_lib.press_keys(locator, "ENTER")
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        

    def calculate_date_range(self, months_number: int):
        """
        Calculate the start and end dates for the datetime filter
        """
        try:
            end_date = date.today()
            start_date = end_date

            if months_number != 0 and months_number != 1:
                start_date = end_date - relativedelta(months=months_number-1)
            return start_date.strftime('%m/01/%Y'), end_date.strftime('%m/%d/%Y'), start_date.replace(day=1)
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')


    def apply_filters(self, sections: list, start_date: str, end_date:str):
        """
        Change the date time filter, Apply input sections, sort by the newest posts
        """
        try:
            # Select Date Range
            self.browser_lib.click_element("xpath: //*[@aria-label=\"Date Range\"]")
            self.browser_lib.click_element("xpath: //*[@aria-label=\"Specific Dates\"]")
            self.browser_lib.input_text("id:startDate", start_date)
            self.browser_lib.input_text("id:endDate", end_date)
            self.browser_lib.press_keys("id:endDate", "ENTER")

            # Select sections
            news_available = False
            if "Any" not in sections:
                self.browser_lib.click_element("xpath: //*[@data-testid=\"section\"]")
                for i, section in enumerate(sections):
                    try:
                        time.sleep(0.5)
                        self.browser_lib.click_element(f"xpath: //*[@data-testid=\"section\"]//*[contains(text(), \"{section}\")]")
                        news_available = True
                    except Exception as err:
                        # Ignore if category not found
                        continue
            else:
                news_available = True

            # Sort by the newest
            self.browser_lib.click_element("xpath: //*[contains(text(), \"Sort by Newest\")]")
            return news_available
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        

    def check_post_date(self, post_date: str, start_datetime: date):
        """
        Extracts the Post date and returns True if the Post is within the date range
        """
        try:
            # Possible Formats
            # [29m ago]: no month -> no validation req.
            # [Aug. 14]: month available -> validate month
            # [Sept. 18, 1851]: year available -> validate year and month

            month_day_year_match = re.match(r'(Jan\.|Feb\.|March|April|May|June|July|Aug\.|Sept\.|Oct\.|Nov\.|Dic\.) (\d{1,2})(, (\d{4}))?', post_date)

            if month_day_year_match:
                month = self.NyPosts_months[month_day_year_match.group(1)]
                day = month_day_year_match.group(2)
                year = month_day_year_match.group(4) or datetime.now().year
                post_date = f'{month}/{day}/{year}'
                post_datetime = datetime.strptime(f'{month}/{day}/{year}', "%m/%d/%Y").date()
            else:
                post_date = date.today().strftime('%m/%d/%Y')
                post_datetime = date.today()
            return post_date, (post_datetime >= start_datetime)
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        

    def text_has_currency(self, text: str):
        """
        Returns True if the Post has a currency
        """
        try:
            dollar_sign_format = r'\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?'
            word_dollars_format = r'\b\d+\s+dollars\b'
            currency_code_format = r'\b\d+\s+USD\b'

            pattern = '|'.join([dollar_sign_format, word_dollars_format, currency_code_format])

            if re.search(pattern, text):
                return True
            else:
                return False
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')


    def retrieve_posts(self, start_datetime: str):
        """
        Returns an array where each row represents one extracted post
        """
        try:
            # Clic on Show More if needed
            date_within_range = True
            while date_within_range:
                time.sleep(2)   #   Allow load before extraction
                posts = self.browser_lib.find_elements("xpath: //*[@data-testid=\"search-bodega-result\"]")
                post_date = posts[-1].text.split('\n')[0]
                post_date, date_within_range = self.check_post_date(post_date, start_datetime)

                # Show more posts if required
                if date_within_range:
                    try:
                        self.browser_lib.click_element("xpath: //*[contains(text(), \"Show More\")]")
                    except Exception as err:
                        # End of the posts reached, break
                        break
            
            # Data extraction and Image download
            posts_data = []
            for post in posts:
                # Split/Organize Extracted Data
                post_content = post.text.split('\n')
                title = post_content[2]
                description = post_content[3]
                post_date, date_within_range = self.check_post_date(post_content[0], start_datetime)

                # Stop extracting if Post is out of range
                if date_within_range is False:
                    break
                
                try:
                    # Locate image
                    picture_url = self.browser_lib.get_element_attribute(f"xpath: //*[contains(text(), \"{title}\")]/../../..//*[@decoding=\"async\"]", "src")

                    # Download image
                    picture_filename = f'{self.output_folder}/{he.remove_special_characters(title)}.jpg'
                    response = requests.get(picture_url)
                    if response.status_code:
                        fp = open(picture_filename, 'wb')
                        fp.write(response.content)
                        fp.close() 
                    
                    #   Open the url in a new window and use keystroke to download it -> Doesn't work on cloud
                    """ Does not work on cloud
                    browser_aux = Selenium()
                    browser_aux.open_available_browser(picture_url, maximized=True)
                    time.sleep(2)
                    browser_aux.press_keys(None, "ctrl","s")
                    self.clip.copy_to_clipboard(picture_filename)
                    time.sleep(2)
                    browser_aux.press_keys(None, "ctrl", "v")
                    browser_aux.press_keys(None, "enter")
                    time.sleep(2)
                    browser_aux.close_window()
                    """
                except Exception as err:
                    picture_filename = f"Image not available"
                
                # Calculate phrase ocurrences
                phrases_count = he.count_substring(self.search_phrase, f"{title} {description}")

                # Check if money on post
                money_in_post = self.text_has_currency(f"{title} {description}")

                # Store Post Data
                posts_data.append([title, post_date, description, picture_filename, phrases_count, money_in_post])
            return posts_data
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')

