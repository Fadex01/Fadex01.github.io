from pathlib import Path
text = Path('index.html').read_text('utf-8')
start = text.find('section class="section skills-bg" id="skills"')
end = text.find('section class="section skills-bg" id="portfolio"')
print('START', start, 'END', end)
print(text[start:end])
print('---PORTFOLIO START---')
end2 = text.find('section class="section container" id="experience"')
print(text[end:end2])
