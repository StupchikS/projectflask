from jinja2 import Template, Environment, FileSystemLoader

file_load = FileSystemLoader("templates")
env = Environment(loader=file_load)
tm = env.get_template("homeindex.html")
msq = tm.render(title="Домашнее задание", h1="Страница с домашним заданием", done=" выполнено!!!")
print(msq)