import requests
from bs4 import BeautifulSoup

# Function to check if a tweet has an embedded image
def check_tweet_for_image(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup);
        # Look for the 'og:image' meta tag that holds the image URL
        og_image_tag = soup.find("meta", property="og:image")

        # Check if the 'og:image' tag exists and contains an image URL
        if og_image_tag and og_image_tag.get('content'):
            print("Tweet has an embedded image.")
            return True  # Embedded image found
        else:
            print("Tweet does not have an embedded image.")
            return False  # No embedded image
    else:
        print(f"Failed to fetch the tweet. Status code: {response.status_code}")
        return False

# Test with the Twitter URL
tweet_url = 'https://x.com/Y3shh_/status/1859775624052867368/'
has_image = check_tweet_for_image(tweet_url)

if not has_image:
    # Modify the URL to fix it or take another action
    new_url = tweet_url.replace("x.com", "fixupx.com")
    print(f"Modified URL: {new_url}")
