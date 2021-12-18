# Vibe

A project to provide methods to unify different and unique
sensory experiences into cohesive collections.

The project has two main components,
a Flask application that serves a website,
and a relational MariaDB database server.

## Directory Structure

The root repository is `vibe`.
The Flask application is contained in `site`,
and the folder `database` contains various SQL scripts, codes,
and API informational files.

## Site

### Setup

Flask is used to host the website.

Create a Python virtual environment using `python -m venv .venv`,
and then activate according to platform.

Install various packages by running `pip install -r requirements.txt`,
which installs Flask and several developement aids
(which VSCode will use if you include the `.vscode` folder that is checked in).)

The project should be able to run on Python 3.7 and above.

The site requires a configuration file to run, named `config.toml` in the `site` directory.
This config file should contain a `[database]` section with connection parameters.

For example,

```toml
[database]
user="site"
password="password"
host="address"
port=3306
database="vibe"
```

### Running

A Flask server can be run from the `site` directory with `flask run`.

Making the site available on other hosts requires hosting on the external interface,
for example my pi currently has an address of `192.168.1.64`,
so the site should be started with `flask run -h 192.168.1.64`.

The Flask application serves both the website and the API.

### API Usage

API endpoints can be used as described in `database/api.txt`.

Inputs to GET requests take the form of parameters,
and inputs to other requests take the form of a JSON body.

All requests return a JSON body as output.

Any non-site (e.g. qualia) modification endpoints
require an admin ID to be given as the header `Admin`.
An admin has an associated permissions number,
which is a two bit number where each bit
indicates their ability to create and delete respectively.

## MariaDB Database

### Server Setup

MariaDB can be installed on a Linux system
using the equivalent of `sudo apt-get install mariadb-server`.

Starting the server can be done with
`sudo systemctl start mariadb.service`,
and enabling it to start on boot can be done with
`sudo systemctl enable mariadb.service`.

The database server should be created with a fully privileged user `root`,
with a blank password.

### Database Setup

The database was created with `CREATE DATABASE vibe;`

A user was created with `CREATE USER site@'192.168.1.%' IDENTIFIED BY 'password'`,
and granted permissions with `GRANT ALL privileges ON vibe.* TO 'site'@'192.168.1.%';`
which gave the user full access to `vibe`.
This user can log in from anywhere on my local area network.
Note that not all local area networks may have all devices on `.1`,
at worst a /16 address space can be given instead, i.e. `'192.168.%'`.

### Database Operation

Log in as `root` with `mysql -u root -p` (password is blank, press enter).
May instead need to do `mysql -u root -h localhost -p`.

`SHOW DATABASES;` will list the databases on the server,
`mysql.user` is a table containing various user data.

When connecting to the database,
the user `site` can be used to connect from LAN,
using port `3306` to database `vibe`.

Database configuration and setup can be done with
the various provided SQL files,
`database/tables.sql` and `database/procedures.sql`.

This files can be loaded from the command line,
e.g. by running `mysql -u root < database/tables.sql`.

`tables.sql` will create the neccesary tables,
and `procedures.sql` will create and update the stored procedures
that are used by the API.

### Database Configuration

In order to allow connections from LAN,
edit the configuration file `/etc/mysql/mariadb.conf.d/50-server.cnf`
and change `bind-address=127.0.0.1` to `0.0.0.0`.
