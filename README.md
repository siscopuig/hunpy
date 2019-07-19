![build-passing-green.svg](https://img.shields.io/badge/build-passing-green.svg) ![version-0.0.1-green.svg](https://img.shields.io/badge/version-0.0.1-green.svg)


## Overview

Find ads and store the ad server source in a database table.

1. [Install prerequisites](#install-prerequisites)

2. [Clone the project](#clone-the-project)
    
3. [Edit config.yml file in config directory](#edit-config-file)

4. [Run the application](#run-the-application)


## Install prerequisites

For now, this project has been mainly created for Unix `(Linux/MacOS)`. Perhaps it could work on Windows.
All requisites should be available for your distribution. The most important are:

* [Git](https://git-scm.com/downloads)

* Python 3.4 ^ 

* [Chromedriver](http://chromedriver.chromium.org/) !important (Driver version need to match Chromium Browser version) 
    - Download driver, then unzip file:
    ````sh
    unzip ~/chromedriver_linux64.zip -d ~/
    ````
    - Move binary to /usr/local/share/
    ````sh     
    sudo mv -f ~/chromedriver /usr/local/share/
    ````
    Give execution permissions:
    ````sh
    sudo chmod +x /usr/local/share/chromedriver
    ````
    Create a symbolic link
    ````sh
    sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
    ````
    Remove zip package
    ````sh
    rm ~/chromedriver_linux64.zip
    ````

* [Chromium Browser](https://www.chromium.org/getting-involved/download-chromium)

    - Install browser for Ubuntu or Debian 
    
        ````sh
        sudo apt install chromium-browser
        ````
        
* MySQL

    - Install MySQL and create a new database called `hunpy`.
      
    - Import schema: 

        from hunpy/hunpy/connector/hunpy_db_blank.sql directory import `hunpy_db_blank.sql` to the database hunpy:

        ````sh
        mysql -u root -p hunpy < hunpy_db_blank.sql
        ````
## Clone the project

To install [Git](http://git-scm.com/book/en/v2/Getting-Started-Installing-Git), 
download it and install following the instructions:

We’ll download the code from its repository on GitHub.

```sh
git clone https://github.com/siscopuig/hunpy.git
```

## Edit config file

1. Edit MySQL credentials in config.yml file:
    ````yaml
    connection.parameters:
        'user': 'root'
        'password': 'pass123'
        'host': 'localhost'
        'database': 'hunpy'
    ````
2. Configure browser viewport (By default is 1440x990):
    ````yaml
    chrome.window.width: 1440
    chrome.window.height: 990
    ````

## Run the application

1. Install Pip and create a virtualenv:

    ````sh
    # Install pip.
    sudo apt-get install python3-pip
    
    # Install virtualenv using pip3.
    pip3 install virtualenv
    
    # Create a virtualenv within the root project folder.
    virtualenv venv
    
    # You can also use a Python interpreter of your choice.
    E.g. virtualenv -p /usr/bin/python3.7 venv
    
    # Activate virtualenv
    source hunpy/venv/bin/activate
    ````
    
2. Install project dependencies:

    ````sh
    pip install -r requirements.txt
    ````
    
3. Fill `sources.txt` file in datasource directory. E.g:
    ````txt
    http://page_one.com
    http://page_two.com
    ...
    ````

4. Run application from command line:

    Run as normal
    ````sh
    python3 hunpu_runner.py
    ````
    
    Is possible to pass a url only
    ````sh
    python3 hunpu_runner.py --url http://example.com
    ````
    
    To run in headless mode --headless (-a)
    ````sh
    python3 hunpu_runner.py --headless
    ````
    
    Running debugging mode display verbose:
    ````sh
    python3 hunpu_runner.py --debug
    ````
    
## Help

Any thought, 
    
        
    

    

    
    
    
   

    










 