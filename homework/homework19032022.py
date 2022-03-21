from jinja2 import Template

dict_hrev = [
    {"arr": "index", "name": "Главная"},
    {"arr": "news", "name": "Новости"},
    {"arr": "about", "name": "О Компании"},
    {"arr": "shop", "name": "Магазин"},
    {"arr": "contacts", "name": "Контакты"}
]

html = """<ul>
{% for item in link -%}
{%- if item.arr == "index" -%}
<li><a href="/{{item.arr}}" class="active">{{item.name}}</a></li>
{%- else -%}
<li><a href="/{{item.arr}}">{{item.name}}</a></li>
{%- endif %}
{% endfor -%}
</ul>
"""

tm = Template(html)
msg = tm.render(link=dict_hrev)

print(msg)
