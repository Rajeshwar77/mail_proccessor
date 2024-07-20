# Mail Proccessor
Project will fetch the the emails from Gmail, Outlook through oauth

## Features

- **Fetch Email**: Retrieve a list of email and store in to database
- **Read Email**: Based on database field it will mark those emails as Read
- **Move Email**: Based on database field it will move those emails as Particular folder

# Folder and format

```

├── README.md
├── __init__.py
├── error.log
├── mail
│   ├── __init__.py
│   ├── provider.py - Consolidating all provider
│   └── read.py - Operation related to read email
├── provider
│   ├── __init__.py
│   ├── gmail.py - Auth, Email listing, reading releated to gmail
│   └── outlook.py  - Auth, Email listing, reading releated to outlook
├── requirements.txt
├── run.py - Main file this is file with collobrate with all
├── token - store the files
└── utils
    ├── __init__.py
    ├── common.py - file used to write a common function for logging, validation
    ├── config.py - config releate to the project environments
    ├── models.py - Struture the response format across the project for an entity
    ├── store.py - Store the values in database
    └── validator.py - commong validator to validate the field
```

## Installation
To set up and run the Stand alone project from my repository, follow these steps:

# 1. Clone the Repository: 
Clone your project repository to your local machine.


```bash

git clone https://github.com/Rajeshwar77/mail_proccessor.git

cd mail_proccessor

```

# 2. Create a Virtual Environment: 
It's recommended to use a virtual environment for Python projects. This keeps dependencies required by different projects separate by creating isolated environments for them.

```bash
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
.\venv\Scripts\activate   # On Windows
```


# 3. Install Dependencies: 
Install the required packages, including FastAPI and any others listed in your requirements.txt file.

```bash
pip install -r requirements.txt
```


# 4. Run the Application: 
To run standalone project for local development
```bash
python3 run.py
```

To run stanalone project on server in background

nohup python3 run.py <<email_input>>

```bash
nohup python3 run.py rajeshwar.vellore@gmail.com
```



