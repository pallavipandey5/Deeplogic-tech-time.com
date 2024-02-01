from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.json.sort_keys = False

@app.route('/getTimeStories')
def get_time_stories():
    # URL of the Time.com website
    url = "https://time.com/"
    
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the latest stories section
        latest_stories_section = soup.find('div', class_='partial latest-stories')
        
        # Find all story items within the latest stories section
        story_items = latest_stories_section.find_all('li', class_='latest-stories__item')
        
        # Initialize an empty list to store the stories
        stories = []
        
        # Extract the title and link of each story
        for item in story_items:
            # Find the link and title elements within each story item
            link_element = item.find('a')
            title_element = item.find('h3', class_='latest-stories__item-headline')
            
            # Extract the link and title text
            if link_element and title_element:
                title = title_element.text.strip()
                link = link_element['href']
                
                # Add the story to the list of stories
                stories.append({"title": title, "link": link})
                
                # Break the loop if we have collected 6 stories
                if len(stories) >= 6:
                    break
        
        # Return the stories as JSON
        return jsonify(stories)
    
    except Exception as e:
        # If an error occurs, return an error message
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
