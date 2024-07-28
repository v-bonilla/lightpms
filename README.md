# lightpms

![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Apache Superset](https://img.shields.io/badge/Apache%20Superset-4.0.2-blue)
![Docker](https://img.shields.io/badge/Docker-26-blue)
![Poetry](https://img.shields.io/badge/Poetry-1.7.0-blue)

## Table of Contents

- [Description](#description)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Configuration](#configuration)

## Description

`lightpms` is designed to collect data for an investment portfolio of cryptocurrencies and utilize Apache Superset as a platform for visualization. This helps in the risk management process by providing insightful visual data representations. 

The project leverages Python for data collection and processing, PostgreSQL for data storage, and Apache Superset for creating interactive dashboards and reports.

## Dependencies

- Python 3.12
- PostgreSQL 16
- Apache Superset 4.0.2
- Docker 26
- Poetry 1.7.0

## Installation

To set up `lightpms` on your local machine, follow these steps:

1. **Clone the repository**
    ```sh
    git clone https://github.com/v-bonilla/lightpms.git
    cd lightpms
    ```

2. **Set up the Python environment using Poetry**
    ```sh
    poetry install
    ```

3. [**Install Apache Superset**](https://github.com/apache/superset?tab=readme-ov-file#installation-and-configuration)

## Configuration

Configure the values of the `.env` file in the root of your project.

## Run the Application

1. **Make sure Apache Superset is up and running**

2. **Run:**

    ```sh
    docker-compose up
    ```

Now, you can start using `lightpms` for managing and visualizing your cryptocurrency investment portfolio.

## Roadmap

- Add Dockerfile
- Configure to run daily
