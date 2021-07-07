def do_stuff(**kwargs):
    for k, v in kwargs.items():
        print(f'{k}: {v}')

do_stuff(first_name='Derek', last_name='Hawkins')