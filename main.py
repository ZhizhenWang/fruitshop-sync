from app.database.sqlite import initialize_relation
from app.service import run, query, update_product_color

if __name__ == '__main__':
    initialize_relation()
    run()
    query()
    update_product_color()
