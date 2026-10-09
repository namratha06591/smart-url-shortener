
# SmartURL — URL Shortener with LRU Cache

SmartURL is a URL-shortening web application built with Python and FastAPI.
It generates short links, stores URLs in SQLite, redirects visitors, and
tracks link clicks. An LRU cache helps speed up repeated URL lookups.

## Features

- Generate unique six-character short codes
- Redirect short links to their original URLs
- Store URL data persistently using SQLite
- Use an LRU cache for faster repeated lookups
- Track click counts
- Validate URL input
- Provide interactive API documentation

## Tech Stack

- Python
- FastAPI
- SQLite
- HTML, CSS, JavaScript
- OrderedDict for LRU caching

## Run Locally

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   `python -m pip install -r requirements.txt`

4. Start the application:

   `python -m uvicorn main:app --reload`

5. Open `http://127.0.0.1:8000`.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Open the website |
| GET | `/health` | Check application status |
| POST | `/shorten` | Create a short link |
| GET | `/{short_code}` | Redirect to the original URL |
| GET | `/stats/{short_code}` | View click statistics |

## Future Improvements

- Custom short links
- QR code generation
- User accounts and authentication
- Link expiration
- Deployment to a public hosting platform

## Author

Somisetty Siri Lakshmi Namratha
GITHUB: https://github.com/namratha06591