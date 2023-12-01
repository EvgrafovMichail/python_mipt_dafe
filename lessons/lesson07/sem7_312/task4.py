
""" Женя работает в фирме, которая разробатывает приложение для создание заметок. 
    Ему дали задание написать 2 функции:
        1) Функция, которая добавляет запись в заметку по ее названию, 
           если заметка уже существует, или создает новую заметку.
        
        2) Функция, которая выводит все записи из конкретной заметки, 
           если название заметки не указывается, то выводятся записи 
           из главной заметки под названием "home" (она всегда существует).

    Но есть один ньюнас: 
        записи в заметках разделены на предложение (и хранятся в базе данных как список предложеий), 
        поэтому на вход в функцию Жени подается имя заметки и n предложений из потока ввода. 
        Значение n всегда разное, Женя не знает сколько предложений ему прийдет. 
        
    Помогите Жене реализовать эти функции!

    Сценарий использоавния функций:
    
        add_note("name", "sentence1", "sentence2", "sentence3", ...)

        get_note("name")
        get_note()

"""

notes = {'home' : []}







# add_note('home', "wash dishes", "cook dinner")
# add_note('store', 'bread', 'butter', 'milk')
# add_note('movies', 'Barbie', 'Oppenheimer', 'Dark Knight')

# get_note()          # wash dishes cook dinner
# get_note('home')    # wash dishes cook dinner
# get_note('store')   # bread butter milk
# get_note('movies')  # Barbie Oppenheimer Dark Knight


# add_note('home', "clean window")
# add_note('store', 'icecream')
# add_note('movies', 'Back To The Future')

# get_note()          # wash dishes cook dinner clean window
# get_note('home')    # wash dishes cook dinner clean window
# get_note('store')   # bread butter milk icecream
# get_note('movies')  # Barbie Oppenheimer Dark Knight Back To The Future
