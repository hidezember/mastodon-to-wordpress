import json
import re
import urllib.parse
from datetime import datetime
import csv

# Load JSON data from the provided file
file_path = 'outbox.json'  # Update this to the correct path of your JSON file

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Define a function to convert date format
def convert_date(date_str):
    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')

# Function to remove specific <a> and <span> tags from content
def remove_specific_tags(content):
    # Pattern to remove specific <a> tags with href and class attributes
    a_pattern = re.compile(r'<a href="https://o3o\.ca/tags/.*?" class="mention hashtag" rel="tag">#<span>.*?</span></a>')
    content = re.sub(a_pattern, '', content)
    # Pattern to remove specific <span> tags with class h-card
    span_pattern = re.compile(r'<span class="h-card" translate="no"><a href="https://o3o\.ca/@.*?" class="u-url mention">@<span>.*?</span></a></span>')
    content = re.sub(span_pattern, '', content)
    return content

# Initialize a list to store the CSV rows
csv_rows = [["ID", "post_author", "post_date", "post_date_gmt", "post_content", "post_title", "post_excerpt", "post_status", "comment_status", "ping_status", "post_password", "post_name", "to_ping", "pinged", "post_modified", "post_modified_gmt", "post_content_filtered", "post_parent", "guid", "menu_order", "post_type", "post_mime_type", "comment_count"]]
tags_info = [["post_id", "tag"]]

# Process each item in the JSON data
starting_post_id = 1   

for idx, item in enumerate(data.get('orderedItems', []), start=starting_post_id):
    post_id = idx  # Use a simple incrementing ID for each post
    post_author = 1  # Assuming author ID is 1
    post_date = convert_date(item.get('published'))
    post_date_gmt = convert_date(item.get('published'))
    
    # Ensure 'object' is a dictionary
    obj = item.get('object', {})
    if isinstance(obj, dict):
        post_content = obj.get('content', '')
        post_content_filtered = obj.get('summary', '') or ''
    else:
        post_content = ''
        post_content_filtered = ''
        
    # Remove specific <a> and <span> tags from content
    post_content = remove_specific_tags(post_content)
    
    # Extract tags from content
    tags = re.findall(r'rel="tag">#<span>(.*?)</span>', post_content)
    tag = tags[0] if tags else ''
    
    post_title = ''
    post_excerpt = ''
    post_status = 'publish'
    comment_status = 'open'
    ping_status = 'open'
    post_password = ''
    post_name = str(post_id)
    to_ping = ''
    pinged = ''
    post_modified = post_date
    post_modified_gmt = post_date_gmt
    post_parent = 0
    guid = f'https://blog.pursuitus.com/?p={post_id}'
    menu_order = 0
    post_type = 'post'
    post_mime_type = ''
    comment_count = 2  # Assuming a comment count of 2

    # Escape single quotes in content and summary
    post_content = post_content.replace("'", "''")
    post_content_filtered = post_content_filtered.replace("'", "''")

    # Append row to CSV data
    csv_row = [post_id, post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt, post_content_filtered, post_parent, guid, menu_order, post_type, post_mime_type, comment_count]
    csv_rows.append(csv_row)
    tags_info.append([post_id, tag])

# Write the CSV rows to a file
output_csv_path = 'output_data.csv'  # Update this to the desired output path
with open(output_csv_path, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_rows)

# Write the tags information to a CSV file
output_tags_path = 'output_tags.csv'  # Update this to the desired output path
with open(output_tags_path, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(tags_info)

print(f"Data CSV has been written to {output_csv_path}")
print(f"Tags CSV has been written to {output_tags_path}")
