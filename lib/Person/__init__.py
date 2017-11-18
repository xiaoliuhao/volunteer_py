class Person(object):
    def __init__(self, name='xiaoming', gender='male', **kw):
        self.name = name
        self.gender = gender
        for k,v in kw.items():
            setattr(self, k, v)