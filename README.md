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
