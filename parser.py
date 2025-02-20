import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime, timezone
from bs4 import BeautifulSoup

# URL του RSS Feed του Blogspot
rss_feed_url = 'http://kefalonitis-onos.blogspot.com/feeds/posts/default?alt=rss'

# Αρχείο για αποθήκευση της ημερομηνίας του τελευταίου post
last_post_file = '/opt/myscripts/python/last_post.txt'

# Συνάρτηση για την ανάγνωση της ημερομηνίας του τελευταίου post
def read_last_post_date():
    if os.path.exists(last_post_file):
        with open(last_post_file, 'r') as file:
            return file.read().strip()
    return None

# Συνάρτηση για την αποθήκευση της ημερομηνίας του τελευταίου post
def write_last_post_date(date):
    with open(last_post_file, 'w') as file:
        file.write(date)

# Ανάγνωση του RSS Feed
feed = feedparser.parse(rss_feed_url)

# Ανάκτηση της ημερομηνίας του τελευταίου post
last_post_date_str = read_last_post_date()
last_post_date = datetime.strptime(last_post_date_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) if last_post_date_str else None

# Έλεγχος αν υπάρχουν νέα posts
latest_post_date = None
new_posts = []

for entry in feed.entries:
    # Μετατροπή της ημερομηνίας σε αντικείμενο datetime
    post_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')

    if latest_post_date is None or post_date > latest_post_date:
        latest_post_date = post_date

    if not last_post_date or post_date > last_post_date:
        new_posts.append(entry)

# Αν υπάρχουν νέα posts, στέλνουμε email
if new_posts:
    # Δημιουργία περιεχομένου email σε HTML
    content = "<h1>Νέες αναρτήσεις από το Blogspot</h1><br>"
    for entry in new_posts:
        post_date_str = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').strftime('%d %b %Y, %H:%M:%S')

        # Αφαίρεση HTML tags από την περίληψη
        summary = entry.summary if 'summary' in entry else 'No summary available.'
        soup = BeautifulSoup(summary, 'html.parser')
        clean_summary = soup.get_text()

        # Αντικατάσταση νέων γραμμών με HTML break lines
        formatted_summary = clean_summary.replace("\n", "<br><br>")

        # Προσθήκη της ανάρτησης στο email περιεχόμενο
        content += f"<h2>{entry.title}</h2>"
        content += f"<p><strong>Date:</strong> {post_date_str}</p>"
        content += f"<p><strong>Summary:</strong> {formatted_summary}</p>"
        content += f"<p><a href='{entry.link}'>Read more</a></p><br><br>"

    # Ρυθμίσεις email
		from_email = 'your-email@gmail.com'
		to_email = 'recipient-email@example.com'
		password = 'your-email-password'
		subject = 'feed parser email subject'

    # Δημιουργία του μηνύματος email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html'))  # Χρήση 'html' αντί για 'plain'

    # Αποστολή του email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Το email στάλθηκε με επιτυχία!")
        # Ενημέρωση της ημερομηνίας του τελευταίου post
        write_last_post_date(latest_post_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
    except Exception as e:
        print(f"Σφάλμα κατά την αποστολή του email: {e}")
else:
    print("Δεν υπάρχουν νέες αναρτήσεις.")
