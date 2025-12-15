with open('billing.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\u00a0', ' ')
with open('billing.py', 'w', encoding='utf-8') as f:
    f.write(content)