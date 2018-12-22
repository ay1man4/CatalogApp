# Catalog App

Catalog App is a website application which can be used to create catalog for any categorized items. It gives the ability to add, edit and delete items under each category.

## Install

Before using this script, you have to prepare the website environment and install required softwares. This illustration showing how to use VM environment using vagrant. Follow below steps to prepare the environment and DB:

- Install [vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- Download and unzip the VM configuration [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)
- Change terminal directory to vagrant directory inside unzipped directory
- Start the virtual Machine using `vagrant up`
- Once done run `vagrant ssh` to log into linux environment
- This website is running with sqlite3, but it can run with any DB by changing the DB engine in database_setup.py
- If DB engine changed, you have to create the DB before using the app
- You may start with demo Catagories using command `python3 seeder.py`

## Usage

In VM terminal run the website using below command:
`python3 application.py`

Items creation, edition and deletion can be accomplished by the website as well as json. Since website is self explanatory, below guide will emphasis JSON part only:

- **Show Categories**: `GET /api/v1/catalog.json`
- **Show One Category**: `GET /api/v1/catalog/<category>/items.json`, *category* is the name of category
- **Show One Item**: `GET /api/v1/catalog/<category>/<item>`, *category* and *item* are the name of category and item
- **Create New Category**: `POST /api/v1/catalog/category/new`, make sure to include category name in the body
- **Create New Item**: `POST /api/v1/catalog/<category>/new`, *category* is the name of category. Also, make sure to include item name and description in the body.
- **Edit Item**: `POST /api/v1/catalog/<category>/<item>/edit`, *category* and *item* are the name of category and item. Also, make sure to include new item name, description and category in the body
- **Delete Item**: `POST /api/v1/catalog/<category>/<item>/delete`, *category* is the name of category. Warning: deletion is not reversible.

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

For more details, please refer to LICENSE file shipped with project.