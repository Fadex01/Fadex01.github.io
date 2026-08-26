#!/usr/bin/env python3
import re
from html.parser import HTMLParser

class ContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.content = []
        self.current_data = []
        self.in_script = False
        self.in_style = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.in_script = True
        elif tag == 'style':
            self.in_style = True
            
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
            
    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            text = data.strip()
            if text:
                self.content.append(text)

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract all content sections using regex patterns
sections = {}

# Meta Tags
print("=" * 60)
print("1. META TAGS")
print("=" * 60)
meta_pattern = r'<meta\s+([^>]+)/?>'
metas = re.findall(meta_pattern, html_content)
for meta in metas:
    print(f"  {meta}")

# Title
title_match = re.search(r'<title>([^<]+)</title>', html_content)
print(f"\n  TITLE: {title_match.group(1) if title_match else 'N/A'}")

# Navigation Links
print("\n" + "=" * 60)
print("2. NAVIGATION LINKS")
print("=" * 60)
nav_section = re.search(r'<div class="navlinks"[^>]*>(.*?)</div>', html_content, re.DOTALL)
if nav_section:
    nav_links = re.findall(r'<a\s+[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', nav_section.group(1))
    for href, text in nav_links:
        print(f"  {text.strip()} -> {href}")

# Hero Section
print("\n" + "=" * 60)
print("3. HERO SECTION")
print("=" * 60)
hero_pattern = r'<section class="hero container"[^>]*id="home">(.*?)</section>'
hero_match = re.search(hero_pattern, html_content, re.DOTALL)
if hero_match:
    hero_content = hero_match.group(1)
    
    # Hero heading
    h1_match = re.search(r'<h1>(.*?)</h1>', hero_content, re.DOTALL)
    if h1_match:
        print(f"  H1: {re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()}")
    
    # Hero description
    p_match = re.search(r'<p>I help crypto(.*?)</p>', hero_content, re.DOTALL)
    if p_match:
        print(f"  Description: I help crypto{p_match.group(1)}")
    
    # Hero buttons
    buttons = re.findall(r'<a[^>]*class="btn[^"]*"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', hero_content)
    print("  CTA Buttons:")
    for href, text in buttons:
        print(f"    - {text.strip()} (href: {href})")
    
    # Hero photo badge
    badge_match = re.search(r'<div class="photo-badge[^>]*>\s*<b>([^<]+)</b>\s*<span>([^<]+)</span>', hero_content)
    if badge_match:
        print(f"  Photo Badge: {badge_match.group(1)}")
        print(f"  Badge Sub: {badge_match.group(2)}")

# About Section
print("\n" + "=" * 60)
print("4. ABOUT SECTION")
print("=" * 60)
about_pattern = r'<section class="section container"[^>]*id="about">(.*?)</section>'
about_match = re.search(about_pattern, html_content, re.DOTALL)
if about_match:
    about_content = about_match.group(1)
    
    # Heading
    h2_match = re.search(r'<h2 class="heading">([^<]+)</h2>', about_content)
    if h2_match:
        print(f"  Heading: {h2_match.group(1)}")
    
    # Description paragraphs
    paragraphs = re.findall(r'<p>([^<]+)</p>', about_content)
    print("  Paragraphs:")
    for i, p in enumerate(paragraphs[:2], 1):
        print(f"    {i}. {p.strip()}")
    
    # Mini stats
    print("  Stats:")
    stats = re.findall(r'<div class="mini-stat[^>]*>\s*<b>([^<]+)</b>\s*<span>([^<]+)</span>', about_content)
    for stat_val, stat_label in stats:
        print(f"    - {stat_val}: {stat_label}")

# Skills Section
print("\n" + "=" * 60)
print("5. SKILLS SECTION")
print("=" * 60)
skills_pattern = r'<section class="section skills-bg"[^>]*id="skills">(.*?)</section>\s*<section class="section skills-bg"'
skills_match = re.search(skills_pattern, html_content, re.DOTALL)
if skills_match:
    skills_content = skills_match.group(1)
    
    # Section heading
    h2_match = re.search(r'<h2 class="heading">([^<]+)</h2>', skills_content)
    if h2_match:
        print(f"  Heading: {h2_match.group(1)}")
    
    # Skills
    skill_items = re.findall(r'<div class="skill[^"]*"[^>]*style="--score:(\d+)%"[^>]*>.*?<div class="skill-top">([^<]+)\s*<span>', skills_content, re.DOTALL)
    print("  Skills with Percentages:")
    for score, skill_name in skill_items:
        print(f"    - {skill_name.strip()}: {score}%")

# Services Section
print("\n" + "=" * 60)
print("6. SERVICES SECTION")
print("=" * 60)
services_pattern = r'<section class="section container"[^>]*id="services">(.*?)</section>\s*<section'
services_match = re.search(services_pattern, html_content, re.DOTALL)
if services_match:
    services_content = services_match.group(1)
    
    # Section heading
    h2_match = re.search(r'<h2 class="heading">([^<]+)</h2>', services_content)
    if h2_match:
        print(f"  Heading: {h2_match.group(1)}")
    
    # Services
    service_items = re.findall(r'<article class="service[^>]*>.*?<div class="service-icon">([^<]+)</div>\s*<h3>([^<]+)</h3>\s*<p>([^<]+)</p>', services_content, re.DOTALL)
    print("  Services:")
    for icon, title, desc in service_items:
        print(f"    - {title.strip()} ({icon.strip()}): {desc.strip()}")

# Portfolio Section
print("\n" + "=" * 60)
print("7. PORTFOLIO SECTION")
print("=" * 60)
portfolio_pattern = r'<section class="section skills-bg"[^>]*id="portfolio">(.*?)</section>\s*<section class="join'
portfolio_match = re.search(portfolio_pattern, html_content, re.DOTALL)
if portfolio_match:
    portfolio_content = portfolio_match.group(1)
    
    # Section heading
    h2_match = re.search(r'<h2 class="heading">([^<]+)</h2>', portfolio_content)
    if h2_match:
        print(f"  Heading: {h2_match.group(1)}")
    
    # Projects
    projects = re.findall(r'<article class="project[^>]*>.*?<h3>([^<]+)</h3>\s*<p>([^<]+)</p>.*?<div class="tags">(.*?)</div>', portfolio_content, re.DOTALL)
    print("  Projects:")
    for title, desc, tags_html in projects:
        print(f"\n    Project: {title.strip()}")
        print(f"    Description: {desc.strip()}")
        tags = re.findall(r'<span class="tag">([^<]+)</span>', tags_html)
        print(f"    Tags: {', '.join(tags)}")

# Community/Join Section
print("\n" + "=" * 60)
print("8. JOIN/COMMUNITY SECTION")
print("=" * 60)
community_pattern = r'<section class="join container"[^>]*id="community">(.*?)</section>'
community_match = re.search(community_pattern, html_content, re.DOTALL)
if community_match:
    community_content = community_match.group(1)
    
    # Heading
    h2_match = re.search(r'<h2>(.*?)</h2>', community_content, re.DOTALL)
    if h2_match:
        print(f"  Heading: {re.sub(r'<[^>]+>', '', h2_match.group(1)).strip()}")
    
    # Buttons
    buttons = re.findall(r'<a class="btn"[^>]*>([^<]+)</a>', community_content)
    print("  Community Links:")
    for btn in buttons:
        print(f"    - {btn.strip()}")

# Contact Section
print("\n" + "=" * 60)
print("9. CONTACT SECTION")
print("=" * 60)
contact_pattern = r'<section class="section container"[^>]*id="contact">(.*?)</section>\s*<footer'
contact_match = re.search(contact_pattern, html_content, re.DOTALL)
if contact_match:
    contact_content = contact_match.group(1)
    
    # Heading
    h2_match = re.search(r'<h2 class="heading">([^<]+)</h2>', contact_content)
    if h2_match:
        print(f"  Heading: {h2_match.group(1)}")
    
    # Description
    p_match = re.search(r'<p>([^<]+)</p>', contact_content)
    if p_match:
        print(f"  Description: {p_match.group(1)}")
    
    # Contact icons/links
    contacts = re.findall(r'<a class="contact-icon\s+(\w+)"[^>]*href="([^"]+)"[^>]*aria-label="([^"]+)"', contact_content)
    print("  Contact Links:")
    for icon_type, href, label in contacts:
        print(f"    - {label}: {href}")

# Footer Section
print("\n" + "=" * 60)
print("10. FOOTER SECTION")
print("=" * 60)
footer_pattern = r'<footer>(.*?)</footer>'
footer_match = re.search(footer_pattern, html_content, re.DOTALL)
if footer_match:
    footer_content = footer_match.group(1)
    
    # Copyright text
    p_match = re.search(r'<p>([^<]+)\s*<span[^>]*>\s*</span>(.*?)</p>', footer_content)
    if p_match:
        year_text = f"{p_match.group(1)} YYYY {p_match.group(2)}"
        print(f"  Copyright: {year_text}")
    
    # Footer links
    links = re.findall(r'<a\s+[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', footer_content)
    print("  Footer Links:")
    for href, text in links:
        print(f"    - {text.strip()}: {href}")
