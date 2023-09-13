from model.browser_automation import browser_automation
from model.excel_automation import excel_automation
from model.helpers import helpers as he
from datetime import datetime
import logging
import sys
import os

# Define a main() function that calls the other functions in order:
def main():
    try:
        # Manage folders and logs
        output_folder=f'{os.path.dirname(os.path.realpath(__file__))}/output'
        he.setup_folder(output_folder)
        logging.basicConfig(filename=f"{output_folder}/error_log.txt", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%B %d, %Y, %H:%M:%S')

        # Retrieve Posts from NyTimes Page
        try:
            ba = browser_automation(output_folder)
            # Open Browser
            ba.open_website(ba.url)
            # Detect empty inputs
            ba.validate_inputs(ba.search_phrase, ba.sections, ba.months_number)
            # Perform phrase search
            ba.search_news(ba.search_phrase)
            # Calculate the time frame for a post to be relevant
            start_date, end_date, start_datetime = ba.calculate_date_range(ba.months_number)
            # Set date, sections and sort order
            news_available = ba.apply_filters(ba.sections, start_date, end_date)
            # Extract Posts

            if news_available:
                posts_data = ba.retrieve_posts(start_datetime)
            else:
                posts_data = [["No recent news found for the sections provided"]]
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        #finally:
            # Close browser
            #ba.browser_lib.close_all_browsers()
        
        
        # Write Output Excel
        try:
            filename = f"{output_folder}/Output_Fresh_News_{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}.xlsx"
            ea = excel_automation(filename)
            # Open/Create file
            wb, ws = ea.open_excel(ea.filename)
            ws.title = "Fresh News"

            # Write header and extracted data
            header_data = [["Title", "Post Date", "Description", "Picture Filename", "Count of Phrases", "Title Contains Money"]]
            ea.write_excel(wb, ws, header_data, 1, 1, True, True)
            ea.write_excel(wb, ws, posts_data, None, 1, False, False)
            
            # Adust the columns Width
            ws.column_dimensions["A"].width = 70
            ws.column_dimensions["C"].width = 112
            ws.column_dimensions["A"].width = 70

        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        finally:
            # Save File
            wb.save(ea.filename)


    except Exception as err:
        exc_tb = sys.exc_info()[2]
        logging.error(f"{err} ({exc_tb.tb_lineno})", exc_info=True)

# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()
