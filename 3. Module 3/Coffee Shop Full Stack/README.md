# Coffe Shop Full Stack Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application must:

1.  Display graphics representing the ratios of ingredients in each drink.
2.  Allow public users to view drink names and graphics.
3.  Allow the shop baristas to see the recipe information.
4.  Allow the shop managers to create new drinks and edit existing drinks.

## Getting started

### Dependencies

To run this project you need the following dependencies installed:

- Python 3.7
- pip
- node.js
- npm

### Frontend dependencies

For details regarding the fronend dependencies check the frontend README.md in the fronend directory.

### Backend dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server

### Backend server

From within the `backend` directory first ensure you are working using your created virtual environment (if you have created one).

To run the server, execute:

```
export FLASK_APP=src/api.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will run the server in DEBUG mode.

### Frontend server

From within the `frontend` directory, run the following command:

```
npm start
```

Open [http://localhost:4200](http://localhost:4200/) to view it in the browser. The page will reload if you make edits.

## Auth0 information

### Test Users:

---

Test users where created for the purpose of this project, their credentials are as follows:
|Name|Role|Email|Password|
|------|-----|-------|-------|
|manager|`Manager`|`manager@coffeeshop.com`|`ABCabc123456`|
|thebarista|`Barista`|`thebarista@coffeeshop.com`|`ABCabc123456`|
