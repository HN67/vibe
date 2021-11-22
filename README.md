# Vibe

A project to provide methods to unify different and unique
sensory experiences into cohesive collections.

## Python Flask Site

### Setup

Create a Python virtual environment using `python -m venv .venv`,
and then activate according to platform.

Install various packages by running `pip install -r requirements.txt`,
which installs Flask and several developement aids
(which VSCode will use if you include the `.vscode` folder that is checked in).)

The project was set up using Python 3.10

### Directory Structure

The root repository is `vibe`, which then contains a folder called `site`
which contains the Flask site. This folder can be easily renamed.

### Running

A flask debug server can be run from the `site` directory with `flask run`,
which starts a server on localhost.

### Example

An example/base Flask app is entirely contained in `site/app.py`.

## MariaDB Database

MariaDB can be installed on a Linux system
using an equivalent of `sudo apt-get install mariadb-server`.

See <https://mariadb.com/kb/en/starting-and-stopping-mariadb-automatically/>

Starting the server can be done with
`sudo systemctl start mariadb.service`,
and enabling it to start on boot can be done with
`sudo systemctl enable mariadb.service`.

See <https://mariadb.com/kb/en/mariadb-basics/>

The database was created with `CREATE DATABASE vibe;`

A user was created with `CREATE USER site@localhost IDENTIFIED BY 'password'`,
and granted permissions with `GRANT ALL privileges ON vibe.* TO 'site'@localhost;`
which gave the user full access to `vibe`.

### Database Operation

Log in as `root` with `mysql -u root -p` (password is blank, press enter).
May instead need to do `mysql -u root -h localhost -p`.

`SHOW DATABASES;` will list the databases on the server,
`mysql.user` is a table containing various user data,
e.g. `User` is the name of users.

`User, Db, Host` from `mysql.db` somewhat shows priveleges of users.

When connecting to the database,
can connect from the same machine,
using user `site`, host `localhost`, database `vibe`, and port `7777`
(not clear on the significance of the port, just choose it randomly),
and appropriate password for the user `site`.
