#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract ALL contact links including X/Twitter
print('=== ALL CONTACT LINKS (COMPLETE) ===')
contact_pattern = r'<a\s+class="contact-icon\s+([^"]*?)"[^>]*href="([^"]+)"[^>]*aria-label="([^"]+)"'
contacts = re.findall(contact_pattern, content)

if contacts:
    for icon_class, url, label in contacts:
        print(f'  {label}: {url}')
else:
    print('  No contact links found with standard pattern')
    # Try broader search
    all_contact_links = re.findall(r'href="(https?://[^"]+|tel:[^"]+|#[^"]+)"[^>]*aria-label="([^"]+)"', content)
    for url, label in all_contact_links:
        if 'contact' in content[max(0, content.find(url)-200):content.find(url)]:
            print(f'  {label}: {url}')

# Also check for X specifically
x_link = re.search(r'href="https://x\.com/([^"]+)"', content)
if x_link:
    print(f'\nX (Twitter) handle: @{x_link.group(1)}')
