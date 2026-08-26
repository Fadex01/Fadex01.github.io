#!/usr/bin/env python3
import re

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Experience Section
print("=" * 70)
print("EXPERIENCE SECTION")
print("=" * 70)

# Find experience section - it should be between id="experience" and the next section or footer
experience_pattern = r'id="experience"[^>]*>(.*?)(?=<section|<footer|</main>)'
experience_match = re.search(experience_pattern, html_content, re.DOTALL)

if experience_match:
    exp_content = experience_match.group(1)
    
    # Try to extract any structured data
    # Look for timeline items or experience entries
    exp_entries = re.findall(r'<article[^>]*class="[^"]*experience[^"]*"[^>]*>(.*?)</article>', exp_content, re.DOTALL)
    
    if not exp_entries:
        # Try alternate patterns
        exp_entries = re.findall(r'<div[^>]*class="[^"]*exp[^"]*"[^>]*>(.*?)</div>\s*(?=<div|</section>)', exp_content, re.DOTALL)
    
    if exp_entries:
        print("Experience Entries:")
        for i, entry in enumerate(exp_entries, 1):
            print(f"\nEntry {i}:")
            # Extract job title
            title_match = re.search(r'<h3[^>]*>([^<]+)</h3>', entry)
            if title_match:
                print(f"  Title: {title_match.group(1).strip()}")
            
            # Extract company/org
            company_match = re.search(r'<h4[^>]*>([^<]+)</h4>|<span[^>]*class="[^"]*company[^"]*"[^>]*>([^<]+)</span>', entry)
            if company_match:
                company = company_match.group(1) or company_match.group(2)
                print(f"  Company: {company.strip()}")
            
            # Extract duration
            duration_match = re.search(r'<span[^>]*class="[^"]*duration[^"]*"[^>]*>([^<]+)</span>|<time[^>]*>([^<]+)</time>', entry)
            if duration_match:
                duration = duration_match.group(1) or duration_match.group(2)
                print(f"  Duration: {duration.strip()}")
            
            # Extract description
            desc_match = re.search(r'<p[^>]*>([^<]+)</p>', entry)
            if desc_match:
                print(f"  Description: {desc_match.group(1).strip()}")
    else:
        print("Raw Experience Section Content:")
        # Remove HTML tags to see what's there
        clean_exp = re.sub(r'<[^>]+>', ' ', exp_content)
        clean_exp = re.sub(r'\s+', ' ', clean_exp).strip()
        if clean_exp:
            print(f"  {clean_exp[:500]}")
        else:
            print("  (No text content found)")
else:
    print("Experience section not found in expected location")
    # Try broader search
    broad_search = re.search(r'<section[^>]*id="experience"[^>]*>(.*?)</section>', html_content, re.DOTALL)
    if broad_search:
        print("Found experience section, content preview:")
        content_preview = re.sub(r'<[^>]+>', '', broad_search.group(1))[:300]
        print(f"  {content_preview}")

# Contact Section with Links
print("\n" + "=" * 70)
print("CONTACT SECTION - DETAILED LINKS")
print("=" * 70)

# More precise pattern for contact section
contact_pattern = r'<section[^>]*id="contact"[^>]*>(.*?)(?=<section|<footer|</main>)'
contact_match = re.search(contact_pattern, html_content, re.DOTALL)

if contact_match:
    contact_content = contact_match.group(1)
    
    # Contact heading
    h2_match = re.search(r'<h2[^>]*class="heading"[^>]*>([^<]+)</h2>', contact_content)
    if h2_match:
        print(f"\nHeading: {h2_match.group(1)}")
    
    # Contact description
    p_match = re.search(r'<p>([^<]+)</p>', contact_content)
    if p_match:
        print(f"Description: {p_match.group(1)}")
    
    # All contact links with SVG
    print("\nContact Links (with details):")
    links = re.findall(r'<a\s+class="contact-icon\s+([^"]*)"[^>]*href="([^"]+)"[^>]*aria-label="([^"]+)"[^>]*>.*?<svg[^>]*>(.*?)</svg>', contact_content, re.DOTALL)
    
    for icon_class, href, label, svg in links:
        print(f"\n  {label}:")
        print(f"    Icon class: {icon_class.strip()}")
        print(f"    Link: {href}")
        # Extract SVG path
        path_match = re.search(r'<path\s+d="([^"]+)"', svg)
        if path_match:
            print(f"    SVG Path: {path_match.group(1)[:80]}...")
    
    # If no SVG links found, try basic pattern
    if not links:
        print("Contact links (alternative extraction):")
        alt_links = re.findall(r'<a[^>]*href="([^"]+)"[^>]*aria-label="([^"]+)"', contact_content)
        for href, label in alt_links[:10]:
            print(f"  - {label}: {href}")

# Download CV link
print("\n" + "=" * 70)
print("CV/DOWNLOAD LINKS")
print("=" * 70)
cv_link = re.search(r'<a[^>]*href="([^"]+Akewusola[^"]*\.pdf)"[^>]*download[^>]*>([^<]+)</a>', html_content)
if cv_link:
    print(f"CV Download: {cv_link.group(1)}")
    print(f"Button Text: {cv_link.group(2)}")
else:
    # Try without download attribute
    cv_link = re.search(r'<a[^>]*href="([^"]*CV\.pdf)"[^>]*>([^<]+)</a>', html_content)
    if cv_link:
        print(f"CV Download: {cv_link.group(1)}")

# Images and assets
print("\n" + "=" * 70)
print("IMAGES AND ASSETS")
print("=" * 70)
images = re.findall(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', html_content)
print("Images:")
for src, alt in images:
    print(f"  - {alt if alt else '(no alt)'}: {src}")

# External CSS and Scripts
print("\n" + "=" * 70)
print("EXTERNAL RESOURCES")
print("=" * 70)
stylesheets = re.findall(r'<link[^>]*href="([^"]+)"[^>]*rel="stylesheet"', html_content)
print("Stylesheets:")
for css in stylesheets:
    print(f"  - {css}")

scripts = re.findall(r'<script[^>]*src="([^"]+)"', html_content)
print("Scripts:")
for script in scripts:
    print(f"  - {script}")

# Preconnects
print("\nPreconnects:")
preconnects = re.findall(r'<link[^>]*rel="preconnect"[^>]*href="([^"]+)"', html_content)
for pc in preconnects:
    print(f"  - {pc}")

print("\n" + "=" * 70)
print("SUMMARY COMPLETE")
print("=" * 70)
