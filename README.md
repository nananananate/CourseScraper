# CourseCake - Our Aim
At the end of the day all courses are... Courses. Every college course shares similar attributes: instructors, course name, units, etc. Therefore, we aim to scrape college course website to create an API where all course data can be accessed, where each college course shares the same basic, expected data.

By making course data easier to access and more "edible" for programs, we hope CourseCake gives a smoother approach build useful tools for students.

## What is a Course?
Here is an example response from our online Flask API endpoint
```
{
  "courses": [
    {
      "code": "01020",
      "department": "Art",
      "departmentTitle": "Art",
      "enrolled": 72,
      "instructor": "MAJOLI, M.BORNSTEIN, J.",
      "location": "VRTL REMOTE",
      "max": 160,
      "name": "Art 1A",
      "requested": 0,
      "restrictions": "",
      "school": "Claire Trevor School of the Arts",
      "status": "NewOnly",
      "time": "TBA",
      "title": "ART IN CONTEXT",
      "type": "Lec",
      "units": 4,
      "waitlisted": 0
    }
  ]
}
```

The breakdown of a course from the JSON response is analogous to the definition of a `Course` in `coursecake/scrapers/course.py`:

Key/Attribute | Value
--- | ---
"code" | String
"department" | String       
"departmentTitle" | String
"enrolled" | String
"instructor" | String
"location" | String
"max" | int
"name" | String
"requested" | int
"restrictions" | String
"school" | String
"status" | String
"time" | String
"title" | String
"type" | String
"units" | int
"waitlisted" | int`





## UC Irvine -- Zot your courses easier and responsibly
CourseCake was inspired to make it easier to develop tools like AntPlanner and Antscoper.

All of the latest scraped data is stored in a local database, which avoids congesting WebSoc and does not

Also, UCI's WebSoc is kinda... ugly. With the course information, I plan to make something useful. Idk what that is yet lol


## Installation

#### Clone repository
`git clone https://github.com/nananananate/CourseScraper`

#### Navigate to the repository folder and install packages
`pip install -r requirements.txt`


# Documentation
## Web API Endpoint

Currently not available online. See below for deploying the Flask Web App locally.


### `/api/uci/courses/all`
Returns all UCI courses

### `/api/uci/courses/search`
Query our database for courses

Usage:
```
/api/uci/courses/search?instructor=pattis&units=4&department=compsci

/api/uci/courses/search?notinstructor=badprof&notlocation=badlocation
```


## CourseScraper `coursecake.scrapers.course_scraper`

Importing CourseScraper:
```
from coursecake.scrapers.course_scraper import CourseScraper
```

### `CourseScraper.getAllUciCourses() -> dict`

From CourseScraper, you can load all UCI courses as a dictionary of `Course`
Usage:
```
scraper = CourseScraper()
courses = scraper.getAllUCICourses()
```
Courses are loaded in chunks; it will take a minute for all courses to be collected.

### `CourseScraper.getCourses(args: dict) -> dict`

Get the latest course information (directly scraped from web) on courses fulfilling search criteria.
`args` is a `dict` in which you specify search parameters and their values. 

Here are the currently supported arguments: 

Key | Value
--- | ---
"code" | String
"department" | String       
"instructor" | String
"breadth" | String
"starttime" | String (ex: 8:00am)
"endtime" | String (ex: 8:00am)
"title" | String
"units" | int

You must specify one of the following parameters: `code`, `department`, `instructor`, or `breadth`

Example usage:
```
args = {
  "department': "compsci",
  "units": 4
  }

courses = scraper.getCourses(args)
```

## Course `coursecake.scrapers.course`
A `Course` object holds all information you can get on a course, accessible by attributes (ex: `Course.instructor`).
You can easily serialize a `Course` using `Course.__dict__`

`courses` is a list of `Course` objects, ad defined in `coursecake/scrapers/course.py`. From the `Course` object, you can get obtain the course's data.

Here is an example of printing some course data from `courses`
```
for course in courses:

  # This does not print out all attributes, just a select few to avoid clutter
  # see more in Course.__str__(self)
  print(course)

  # print the status of the course; if it is open, closed, full, etc.
  print(course.status)
```

To save all UCI courses into a JSON file:
```
scraper.downloadUCICourses()
```

The format of data within the JSON file is a dictionary of `Course.__dict__`, where `Course.code` are the keys.


## Deploy Flask Application locally


#### Run flask
For Linux and Mac:

```
export FLASK_APP=coursecake/flaskapp
export FLASK_ENV=development
flask run
```

For Windows cmd, use set instead of export:

```
set FLASK_APP=coursecake/flaskapp
set FLASK_ENV=development
flask run
```

For Windows PowerShell, use $env: instead of export:

```
$env:FLASK_APP = "coursecake/flaskapp"
$env:FLASK_ENV = "development"
flask run
```

You’ll see output similar to this:

```
* Serving Flask app "coursecake/flaskapp"
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 855-212-761
```
donezo
