from maria_db import Database


db = Database()


def test():
    # db.create_table_users()
    # db.create_table_cont_users()
    db.add_cont_user(name='Two', user=290053979)
    # db.add_user('Two', 'One')
    # db.update_cont_user(name='Two', status='Oasdasdae',
    #                     adress='asdasdas', phone='asdasdasd')


test()
