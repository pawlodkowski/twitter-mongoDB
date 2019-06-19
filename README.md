# Python Twitter API with MongoDB

### Example python code pipeline for storing real-time, streamed tweets (using tweepy) into a NoSQL database (MongoDB).

The purpose of this repository is to show students how to use tweepy to intercept
streamed tweets, parse the relevant information from each JSON object, and store
the data into a Mongo database for further processing.

In studying this code,
students will:

  - learn how to use a complicated Python library / API (tweepy);
  - better understand how Python classes work;
  - connect multiple Python scripts together into a pipeline;
  - refresh their knowledge on command-line interfaces (using argparse);
  - and practice basic software engineering principles (e.g. functions, clean code, git).

#### Useful Applications
The working code in this repository can be used a foundation for interesting data science projects, such as:
  - **sentiment analysis**
  - **data visualization**
    - *e.g. plotting maps*
  - **cloud deployment**
    - *e.g. running the code on a cloud server and collecting tweets for an extended period of time*
  - **time-series analysis**
    - *e.g. tracking use of key words or hashtags over time*

In addition, students can use this code to practice making pip-installable python packages:
  - through the use of [Cookiecutter](https://github.com/audreyr/cookiecutter), and
  - uploading the package to the [Python Package Index (PyPI)](https://packaging.python.org/tutorials/packaging-projects/).


#### Data Flow Diagram

![Alt text](twitter-mongo-diagram.png?raw=true "Title")

#### How to run the script
*(hopefully to be more automated in the future)*

  1. Clone the repository ``git clone https://github.com/pawlodkowski/twitter-mongoDB.git``

  2. Go into the folder ``cd twitter-mongoDB``

  3. Install requirements ``pip install -r requirements.txt``

  4. Make a copy of the *config_template.py* file and name it *config.py*.

  5. Inside the *config.py* file, fill in the empty strings with your Twitter API credentials.

  6. In another terminal, make sure you have a local MongoDB server running (e.g. ``mongod --config /usr/local/etc/mongod.conf``)

  7. Run the *load_database.py* script and supply a keyword argument to filter tweets by any particular keyword.

    - e.g. ``python load_database.py -k berlin``

    - To view argument parser help in the command line, type ``python load_database.py -h``

#### Credits

Parts of this code were inspired by and modified from the **tweego** project (developed by the [realtweego](https://github.com/realtweego) development team).

Repository:
[https://github.com/realtweego/tweego](https://github.com/realtweego/tweego).
