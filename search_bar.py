from wtforms import form, stringField, SelectField

class search_results(form):
    choices = [('Anna', 'Jones'),
                ('Anna', 'Jones')
                ('Allan', 'Smith'),
                ('Andrea', 'Smith'),
                ('Albie', 'Jones'),
                ('Albie', 'Jones'),
                ('Ahmed', 'Fahad')]
    select = SelectField('search for patients:', choices=choices)
    search =stringField('')
