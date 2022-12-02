import re

s = '''[SJ]-Заходит мужик в бар.
- Бетховен?
- Со спины не разобрать.[EJ]'''
result = re.search(r'\[SJ\](.*)\[EJ\]', s, re.DOTALL)
v1 = result.group(0)
v2 = v1.strip("[SJ](.*)[EJ]")
v2 = '[SJ]' + v2
print (v2)
text = '[SJ]Тут текст простой[EJ]'