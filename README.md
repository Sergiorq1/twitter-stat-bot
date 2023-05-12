# Twitter-stat-bot

My Pyhton program that **automates tweets** by sraping basketball stats from the basketball reference website and stores data into a Sqlite database

## Features

- Tweets Top players in effective field goal percentage
- future implementations: Top players in points per game, rebounds, assists, and 3 point percentage

## How to run:

- create your own twitter developer account and save access keys and tokens in a .env file
- create and activate a virtual environment, if you need help doing so, [refer to this article](https://python.land/virtual-environments/virtualenv)
- when inside virtual environment, run the following code:
```bash
  pip install -r requirements.txt
```

- finally, inside your terminal, change directory to bots and run your choice of twitter bot
```bash
  cd bots
  python3 efgp.py
```

## Tech Stack

**Server:** Python, BeautifulSoup, Sqlite
**Client** Terminal

## Acknowledgements

 - [Baketball Reference](https://www.basketball-reference.com/)

## Authors

- [@sergiorq1](https://www.github.com/sergiorq1)

## Demo

This [here](https://www.github.com/sergiorq1) demonstrates how my project works:

## How to contribute (step-by-step):

- For starters, you want to decide what kind of basketball statistic you will want to implement
- for this example, we will be implementing a feature that keeps track of points per game leaders in the current  season 
- in the root directory, we change directory to bots and create a new file named weeklyPPG:
```bash
  cd bots
  touch weeklyPPG.py
```

- Next, we import functions from config.py
```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```

- Finally, we write code that will tweet out the expected result in a tweet
```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```

- This is a great introduction to open source for python developers!