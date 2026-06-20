<a name="readme-top"></a>

![Python](https://img.shields.io/badge/python-3.x-blue) ![Flask](https://img.shields.io/badge/flask-framework-black) ![SQLite](https://img.shields.io/badge/sqlite-database-lightgrey) ![License](https://img.shields.io/badge/license-MIT-green) [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin)](https://linkedin.com/in/prarthanasriyas)

<div align="center">

# URL Shortener API

A Flask-based URL Shortener API that converts long URLs into short, shareable links — with click tracking, click limits, and expiry date support, backed by SQLite.

[Explore the repo »](https://github.com/prarthanasriyas7/url-shortener)

[Report Bug](https://github.com/prarthanasriyas7/url-shortener/issues) · [Request Feature](https://github.com/prarthanasriyas7/url-shortener/issues)

</div>

<details>
<summary>Table of Contents</summary>

1. [About The Project](#about-the-project)
   - [Built With](#built-with)
2. [Key Features](#key-features)
3. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Validation Rules](#validation-rules)
7. [Project Structure](#project-structure)
8. [Roadmap](#roadmap)
9. [Contributing](#contributing)
10. [License](#license)
11. [Contact](#contact)

</details>

## About The Project

The **URL Shortener API** is a Python Flask application that takes any long URL and converts it into a short, unique code. When the short URL is visited, it automatically redirects to the original website while tracking click counts and enforcing optional click limits and expiry dates.

This project was built during my internship to practice REST API design, database operations, and real-world validation logic such as duplicate prevention and link expiry.

Here's what makes it useful:

- No duplicate short URLs are created for the same long URL while it's still active
- Click limits and expiry dates can be set per link, after which the link automatically stops working
- Once a link expires, submitting the same long URL again generates a brand-new short code automatically
- Every click is tracked and stored, along with the exact creation date and time of each link

(back to top)

### Built With

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

```
python -m pip install --upgrade pip
```

### Installation

1. Clone the repo

```
git clone https://github.com/prarthanasriyas7/url-shortener.git
```

2. Move into the project directory

```
cd url-shortener
```

3. Install the required Python packages

```
pip install flask python-dotenv
```

or, if a `requirements.txt` is present:

```
pip install -r requirements.txt
```

### Configuration

All settings are controlled through a `.env` file in the project root. Create one (or edit the existing one) with values like:

```
FLASK_SECRET_KEY=your_secret_key_here
DATABASE_NAME=urls.db
PORT=5000
```

(back to top)

## Usage

Run the application:

```
python app.py
```

The server will start at:

```
http://127.0.0.1:5000
```

Use Thunder Client, Postman, or your browser to interact with the API endpoints below.

(back to top)

## API Endpoints

### 1. POST /shorten

Creates a short URL from a long URL.

**Request Body:**

```json
{
    "url": "https://www.example.com",
    "click_limit": 5,
    "expiry_date": "2026-12-31"
}
```

**Response:**

```json
{
    "short_url": "http://localhost:5000/aB3xZ9456",
    "code": "aB3xZ9456",
    "click_limit": 5,
    "expiry_date": "2026-12-31",
    "created_date": "2026-06-20 10:00:00",
    "message": "New short URL created!"
}
```

### 2. GET /url/<short_code>

Returns the original URL and all statistics for a given short code.

**Response:**

```json
{
    "original_url": "https://www.example.com",
    "click_count": 2,
    "click_limit": 5,
    "expiry_date": "2026-12-31",
    "created_date": "2026-06-20 10:00:00",
    "short_url": "http://localhost:5000/aB3xZ9456"
}
```

### 3. GET /<short_code>

Redirects to the original URL, tracks the click count, and checks expiry/click limit before redirecting.

(back to top)

## Validation Rules

| Rule | Behavior |
|---|---|
| Duplicate URL | If the same long URL is submitted while its short code is still active, the same short code is returned instead of creating a new one |
| Click Limit | Optional integer; once `click_count` reaches `click_limit`, the short URL stops redirecting and returns an error |
| Expiry Date | Optional date in `YYYY-MM-DD` format; once the current date passes the expiry date, the short URL stops redirecting |
| Expired URL Resubmission | If a short URL has expired (by date or click limit) and the same long URL is submitted again, a brand-new short code is generated automatically with fresh settings |
| Short Code Format | 6 random letters/digits followed by 3 random digits (e.g. `aB3xZ9456`) |
| Missing URL Field | Returns a `400` error if the `url` field is missing from the request body |

(back to top)

## Project Structure

| File | Purpose |
|---|---|
| `app.py` | Main Flask application |
| `.env` | Environment configuration file |
| `.gitignore` | Git ignore rules |
| `README.md` | Project documentation |
| `urls.db` | SQLite database (auto-generated on first run) |

(back to top)

## Roadmap

- [x] Shorten long URLs into unique short codes
- [x] Auto-redirect on visiting short URL
- [x] Duplicate URL prevention
- [x] Click limit support
- [x] Expiry date support
- [x] Click count tracking
- [x] Creation date logging
- [ ] User authentication for managing personal links
- [ ] Deploy to a live hosting platform
- [ ] Custom alias support (user-chosen short codes)

See the [open issues](https://github.com/prarthanasriyas7/url-shortener/issues) for a full list of proposed features and known issues.

(back to top)

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

(back to top)

## License

Distributed under the MIT License. See `LICENSE` for more information.

(back to top)

## Contact

Prarthana Sriya - prarthanasriyas@gmail.com - [LinkedIn](https://linkedin.com/in/prarthanasriyas)

Project Link: [https://github.com/prarthanasriyas7/url-shortener](https://github.com/prarthanasriyas7/url-shortener)

(back to top)