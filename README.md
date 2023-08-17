# RPA Challenge - Fresh News

## Overview

Our mission is to enable all people to do the best work of their lives—the first act in achieving that mission is to help companies automate tedious but critical business processes. This RPA challenge should showcase your ability to build a bot for purposes of process automation.

## 🟢 The Challenge

The challenge is to automate the process of extracting data from the [NY Times news site](http://www.nytimes.com/).

### Configuration Variables

Three variables must be configured:
- **Search Phrase:** The phrase to search for in the news site.
- **News Category or Section:** The specific section or category of news to filter by.
- **Number of Months for News:** Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on.

### Main Steps

1. Open the NY Times site by following the [link](http://www.nytimes.com/).
2. Enter a phrase in the search field.
3. On the result page, apply the following filters:
    - Select a news category or section.
    - Choose the latest (i.e., newest) news.
4. Extract the following values: title, date, and description.
5. Store the following in an Excel file:
    - Title
    - Date
    - Description (if available)
    - Picture Filename
    - Count of search phrases in the title and description
    - `True` or `False`, depending on whether the title or description contains any amount of money (Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD).
6. Download the news picture and specify the file name in the Excel file.
7. Repeat steps 4-6 for all news that falls within the required time period.

### Submission Criteria

1. **Quality Code:** Your code is clean, maintainable, and well-architected. The use of an object-oriented model is preferred.
2. **Resiliency:** Your architecture is fault-tolerant and can handle failures both at the application level and website level.
3. **Best Practices:** Your implementation follows best RPA practices.
