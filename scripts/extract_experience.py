#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract experience section - find between id="experience" and next section
exp_pattern = r'id="experience"[^>]*>(.*?)(?=<section|<footer)'
exp_match = re.search(exp_pattern, content, re.DOTALL)

if exp_match:
    exp_text = exp_match.group(1)
    
    # Get section heading
    heading = re.search(r'<h2[^>]*>([^<]+)</h2>', exp_text)
    print('=== EXPERIENCE SECTION ===')
    if heading:
        print(f'Heading: {heading.group(1)}')
    
    intro = re.search(r'<p class="intro"[^>]*>([^<]+)</p>', exp_text)
    if intro:
        print(f'Intro: {intro.group(1)}\n')
    
    # Extract experience entries - look for any divs or articles with job info
    # Pattern 1: Looking for h3 (job title) followed by text
    exp_entries = re.findall(
        r'<h3[^>]*>([^<]+)</h3>\s*<span[^>]*class="[^"]*date[^"]*"[^>]*>([^<]*)</span>.*?<p[^>]*>([^<]+)</p>',
        exp_text,
        re.DOTALL
    )
    
    if not exp_entries:
        # Try alternate pattern without date span
        exp_entries = re.findall(
            r'<h3[^>]*>([^<]+)</h3>\s*(?:<[^>]*>)*([^<]*\d{4}[^<]*)?.*?<p[^>]*>([^<]+)</p>',
            exp_text,
            re.DOTALL
        )
    
    if not exp_entries:
        # Most basic pattern
        exp_entries = re.findall(
            r'<h3[^>]*>([^<]+)</h3>.*?<p[^>]*>([^<]+)</p>',
            exp_text,
            re.DOTALL
        )
        # Format the basic entries to have 3 fields
        exp_entries = [(role, '', desc) for role, desc in exp_entries]
    
    print('Experience Entries:')
    for i, entry in enumerate(exp_entries, 1):
        if len(entry) >= 3:
            role, date, desc = entry[0], entry[1] if len(entry) > 1 else '', entry[2] if len(entry) > 2 else ''
        elif len(entry) == 2:
            role, desc = entry
            date = ''
        else:
            role = entry[0]
            desc = ''
            date = ''
        
        print(f'\n  {i}. {role.strip()}')
        if date and date.strip():
            print(f'     Date: {date.strip()}')
        print(f'     Description: {desc.strip()[:300]}...' if len(desc.strip()) > 300 else f'     Description: {desc.strip()}')

# Try to find more complete experience info with a different approach
print('\n=== RAW EXPERIENCE TEXT (first 1500 chars) ===')
exp_raw = re.sub(r'<[^>]+>', '\n', exp_text) if exp_match else 'Not found'
exp_raw = re.sub(r'\n+', '\n', exp_raw)
print(exp_raw[:1500] if exp_match else 'Experience section not found')

# Extract Discord link
print('\n=== CONTACT LINKS ===')
discord_link = re.search(r'contact-icon discord[^>]*href="([^"]+)"', content)
if discord_link:
    print(f'Discord: {discord_link.group(1)}')
else:
    print('Discord: (not found in standard location)')

# Check for all social/contact links again
contact_links = re.findall(
    r'class="contact-icon\s+(\w+)"[^>]*href="([^"]+)"[^>]*aria-label="([^"]+)"',
    content
)
print('\nAll Contact Links:')
for icon_type, url, label in contact_links:
    print(f'  {label}: {url}')
