![Python](https://img.shields.io/badge/python-3.x-blue) ![Flask](https://img.shields.io/badge/flask-framework-black) ![SQLite](https://img.shields.io/badge/sqlite-database-lightgrey) ![License](https://img.shields.io/badge/license-MIT-green)

<div align="center">

# URL Shortener API

A Flask-based URL Shortener API that converts long URLs into short, shareable links — with click tracking, click limits, and expiry date support, backed by SQLite.

[Explore the repo »](#)

[Report Bug](#) · [Request Feature](#)

</div>

## Table of Contents

- [About The Project](#about-the-project)
- [Built With](#built-with)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About The Project

The **URL Shortener API** is a Python Flask application that takes any long URL and converts it into a short, unique code. When the short URL is visited, it automatically redirects to the original website while tracking click counts and enforcing optional click limits and expiry dates.

This project was built during my internship to practice REST API design, database operations, and real-world validation logic such as duplicate prevention and link expiry.

Here's what makes it useful:

- No duplicate short URLs are created for the same long URL while it's still active
- Click limits and expiry dates can be set per link, after which the link automatically stops working
- Once a link expires, submitting the same long URL again generates a brand-new short code automatically
- Every click is tracked and stored, along with the exact creation date and time of each link

(back to top)

## Built With

- ![Python](https://img.shields.io/badge/python-3.x-blue)
- ![Flask](https://img.shields.io/badge/flask-framework-black)
- SQLite3 (Python built-in)

(back to top)

## Key Features

| Feature | Description |
|---|---|
| Shorten Long URLs | Converts any long URL into a unique short code |
| Auto Redirect | Visiting the short URL automatically redirects to the original site |
| Duplicate Prevention | Returns the same short code for a long URL that is still active |
| Click Limit | Optional maximum number of clicks per short URL |
| Expiry Date | Optional expiry date after which the short URL stops working |
| Click Tracking | Stores and updates click count on every visit |
| Auto Regeneration | Creates a new short code automatically if the old one expired |
| Creation Date Logging | Stores the exact date and time each short URL was created |

(back to top)

## Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

You'll need Python 3 and `pip` installed on your machine.