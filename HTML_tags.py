# Класс HTML аргументы: 
# file_path - путь к файлу для записи содержимого, 
# output - выводить ли содержимое на экран (по умолч. отображает) 
class HTML():
# Инициализация атрибутов класса
    def __init__(self, file_path, output = True):
        self.file_path = open(file_path, "w")
        self.children = []
        self.output = output  
# Методы для работы с контекстным методом with
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for child in self.children:
            file_text = "<html>\n%s\n</html>" % child
        self.file_path.write(file_text)
        self.file_path.close()
        if self.output:
            print(file_text)

# Перегрузка оператора += . добавляет указанный объект к списку дочерних 
    def __iadd__(self, other): 
        self.children.append(other)
        return self    

class TopLevelTag():
# Инициализация атрибутов класса
    def __init__(self, tag):
        self.tag = tag
        self.children = []
# Методы для работы с контекстным методом with 
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

# Перегрузка оператора += . Добавляет указанный объект к списку дочерних 
    def __iadd__(self, other): 
        self.children.append(other)
        return self   
# метод при вызове объекта в виде строки
    def __str__(self):
        for child in self.children:
            child.tabs += 1
            tag_text = "<{tag}>\n{child}\n</{tag}>".format(tag = self.tag, child = child)
        return tag_text


class Tag:
    # Инициализация атрибутов класса
    def __init__(self, tag, attributes={}, is_single=False):
        self.tag = tag
        self.text = ""
        self.attributes = attributes
        self.tabs = 0

        self.is_single = is_single
        self.children = []
# Методы для работы с контекстным методом with 
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self
# Метод для вычисления отступов
    def AddTabs(self, tabs_amount):
        tab_str = ''	            		
        i = tabs_amount
        while i > 0:
            tab_str += "  " # В качестве отступа двойной пробел
            i -= 1
        return tab_str
# метод при вызове объекта в виде строки
    def __str__(self):
        attrs = []
    # превод атрибутов тега в строку
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
    # превод открывающегося тега с отступами и атрибутами в строку
        if self.children:	
            if attrs:       
                opening = "{tabs}<{tag} {attrs}>".format(tabs = self.AddTabs(self.tabs), tag=self.tag, attrs=attrs)
            else:
                opening = "{tabs}<{tag}>".format(tabs = self.AddTabs(self.tabs), tag=self.tag)
    # превод содержимого тега с с дочерними объектами в строку
            internal = "%s" % self.text
            for child in self.children:
            	child.tabs = self.tabs + 1
            	internal += "\n{child}".format(child = child)
    # превод закрывающегося тега с отступами и атрибутами в строку        
            ending = "\n{tabs}</{tag}>".format(tabs = self.AddTabs(self.tabs), tag=self.tag)

            return opening + internal + ending
    # Тоже самое только без дочерних объектов и с проверкой на одинарный тег
        else:
            if self.is_single:
                if attrs:
                    return "{tabs}<{tag} {attrs}>{text}".format(tabs = self.AddTabs(self.tabs), tag=self.tag, attrs=attrs, text=self.text)
                else:
           	        return "{tabs}<{tag}>{text}".format(tabs = self.AddTabs(self.tabs), tag=self.tag, text=self.text)		
            else:
                if attrs:
                    return "{tabs}<{tag} {attrs}>{text}</{tag}>".format(tabs = self.AddTabs(self.tabs), tag=self.tag, attrs=attrs, text=self.text)
                else:
                    return "{tabs}<{tag}>{text}</{tag}>".format(tabs = self.AddTabs(self.tabs), tag=self.tag, text=self.text)

# Перегрузка оператора += . добавляет указанный объект к списку дочерних 
    def __iadd__(self, other):
        self.children.append(other)
        return self   

with HTML("text.txt") as doc: # добавить аргумент output=False чтобы не отображать результат на экране
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
            doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", attributes = {'class':"main-text"}) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div",attributes = {'class':"container container-fluid", 'id':"lead"}) as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", attributes = {'src':"/icon.png", 'data-image':"responsive"}, is_single = True) as img:
                div += img

            body += div
        doc += body