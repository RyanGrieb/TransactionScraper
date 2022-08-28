# Transaction Scraper
Personal web scraper that fetches bank & credit card transactions from websites, and displays all information into a excel file.

![Data Example](https://user-images.githubusercontent.com/6068039/184972961-207fd3f5-9270-45e2-b372-31af4c43269e.png)

Each time the script is ran, data from the excel file is retained. Allowing the user to save transactions over a long period time.

We use python's selenium web browser to pretend were a normal user, and fetch the respective data.
Currently this script only supports the banking services I use, if you'd like to see another website added. Create an issue/pr.

## Supported sites
* [Broadway Bank](https://broadway.bank/)
* [Cardmember Service](https://www.myaccountaccess.com/onlineCard/login.do)

## Todo
* Refact project layout into proper modules? - I'm not sure but our current approach doesn't seem correct
* Save website cache from selenium - Avoid unrecognized device messages every login
* Handle website errors gracefully (Shouldn't crash the whole script, just skip to next website..)
