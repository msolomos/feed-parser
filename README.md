# Feed Parser for Blogspot

## Overview
This Python script fetches new blog posts from a specified Blogspot RSS feed and sends an email notification when new posts are available.

## Features
- Parses an RSS feed using `feedparser`.
- Extracts and processes new posts since the last execution.
- Sends email notifications with new posts formatted in HTML.
- Stores the last fetched post date in a file to track updates.

## Prerequisites
Before running the script, ensure you have the following installed:

- Python 3.x
- Required Python libraries:
  ```sh
  pip install feedparser beautifulsoup4
  ```

## Configuration
### RSS Feed
The script fetches posts from:
```python
rss_feed_url = 'http://kefalonitis-onos.blogspot.com/feeds/posts/default?alt=rss'
```

### Email Settings
Configure the email settings in the script:
```python
from_email = 'your-email@gmail.com'
to_email = 'recipient-email@example.com'
password = 'your-email-password'
```
**Note:** Using plain text passwords is not recommended. Consider using environment variables or secure storage.

### Storage Path
Modify the path to store the last fetched post date:
```python
last_post_file = '/opt/myscripts/python/last_post.txt'
```

## Running the Script
Execute the script using Python:
```sh
python feed_parser.py
```

## Deployment
- Set up a cron job to run the script periodically (e.g., every hour):
```sh
0 * * * * /usr/bin/python3 /path/to/feed_parser.py
```

## Security Considerations
- Store credentials securely using environment variables instead of hardcoding them.
- Use an app-specific password if using Gmail.
- Ensure proper permissions for the `last_post.txt` file.

## License
This project is licensed under the MIT License.

