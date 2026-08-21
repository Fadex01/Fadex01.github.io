from pathlib import Path
text = Path('index.html').read_text('utf-8')
skills = 'section class="section skills-bg" id="skills"'
portfolio = 'section class="section skills-bg" id="portfolio"'
experience = 'section class="section container" id="experience"'
start = text.find(skills)
portfolio_start = text.find(portfolio)
experience_start = text.find(experience)
print('skills', start, 'portfolio', portfolio_start, 'experience', experience_start)
print('---skills block---')
print(text[start:portfolio_start])
print('---portfolio block---')
print(text[portfolio_start:experience_start])
