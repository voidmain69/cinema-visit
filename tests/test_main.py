import pytest
import io
import ast
from _ast import ImportFrom

from contextlib import redirect_stdout

import app.main

from app.main import cinema_visit
from app.cinema.cinema_bar import CinemaBar
from app.cinema.cinema_hall import CinemaHall
from app.people.cinema_staff import Cleaner
from app.people.customer import Customer

@pytest.mark.parametrize(
    "customers,hall_number,cleaner,movie,output",
    [
        (
            [
                {"name": "Bob", "food": "popcorn"}
            ],
            1,
            "Anna",
            "Tenet",
            '''Cinema bar sold popcorn to Bob.
"Tenet" started in hall number 1.
Bob is watching "Tenet".
"Tenet" ended.
Cleaner Anna is cleaning hall number 1.
'''

        ),
        (
            [
                {"name": "Bob", "food": "Coca-cola"},
                {"name": "Alex", "food": "popcorn"}
            ],
            5,
            "Anna",
            "Madagascar",
            '''Cinema bar sold Coca-cola to Bob.
Cinema bar sold popcorn to Alex.
"Madagascar" started in hall number 5.
Bob is watching "Madagascar".
Alex is watching "Madagascar".
"Madagascar" ended.
Cleaner Anna is cleaning hall number 5.
'''
        ),
        (
            [
                {"name": "Susan", "food": "Pepsi"},
                {"name": "Michael", "food": "Coca-cola"},
                {"name": "Monica", "food": "popcorn"}
            ],
            3,
            "Vasiliy",
            "Interstellar",
'''Cinema bar sold Pepsi to Susan.
Cinema bar sold Coca-cola to Michael.
Cinema bar sold popcorn to Monica.
"Interstellar" started in hall number 3.
Susan is watching "Interstellar".
Michael is watching "Interstellar".
Monica is watching "Interstellar".
"Interstellar" ended.
Cleaner Vasiliy is cleaning hall number 3.
'''

        )
    ]
)
def test_cinema_visit(customers, hall_number, cleaner, movie, output):
    f = io.StringIO()

    with redirect_stdout(f):
        cinema_visit(customers, hall_number, cleaner, movie)

    out = f.getvalue()

    assert out == output, (
        f"When 'customers' equals to {customers}, "
        f"'hall_number' equals to {hall_number}. "
        f"'cleaner' equals to {cleaner}, "
        f"and 'movie' equals to {movie}, "
        f"'cinema_visit' output should equal to {output}"
    )


def test_customer_constructor():
    customer = Customer(name="Bob", food="popcorn")
    assert hasattr(customer, "name"), (
        "Customer instance should have 'name' attribute"
    )
    assert hasattr(customer, "food"), (
        "Customer instance should have 'food' attribute"
    )


def test_customer_watch_movie():
    name = "Bob"
    movie = "Matrix"
    customer = Customer(name=name, food="popcorn")
    f = io.StringIO()

    with redirect_stdout(f):
        customer.watch_movie(movie)

    out = f.getvalue()
    output = 'Bob is watching "Matrix".\n'
    assert out == output, (
        f"'watch_movie' output should equal to {output}, "
        f"when customer's name is '{name} and movie is {movie}"
    )


def test_cleaner_clean_hall():
    name = "Anatoly"
    cleaner = Cleaner(name=name)
    hall_number = 9
    f = io.StringIO()

    with redirect_stdout(f):
        cleaner.clean_hall(hall_number=hall_number)

    out = f.getvalue()
    output = "Cleaner Anatoly is cleaning hall number 9.\n"
    assert out == output, (
        f"'clean_hall' output should equal to {output}, "
        f"when cleaner's 'name' equals to {name} and 'hall_number' equals to {hall_number}"
    )


def test_cinema_bar_sell_product():
    name = "Alice"
    food = "Sprite"
    customer = Customer(name=name, food=food)
    cb = CinemaBar()
    f = io.StringIO()

    with redirect_stdout(f):
        cb.sell_product(customer, customer.food)

    out = f.getvalue()
    output = "Cinema bar sold Sprite to Alice.\n"
    assert out == output, (
        f"'sell_product' output should equal to {output}, "
        f"when customer's name equals to {name} and customer's food equals to {food}"
    )


def test_cinema_hall_movie_session():
    hall = 4
    ch = CinemaHall(hall)
    customer1_name = "Max"
    food1 = "chips"
    customer1 = Customer(customer1_name, food1)
    customer2_name = "Alex"
    food2 = "popcorn"
    customer2 = Customer(customer2_name, food2)
    movie_name = "I'm Robot"
    cleaner_name = "John"
    cleaner = Cleaner(cleaner_name)
    f = io.StringIO()

    with redirect_stdout(f):
        ch.movie_session(movie_name, [customer1, customer2], cleaner)

    out = f.getvalue()
    output = '''"I'm Robot" started in hall number 4.
Max is watching "I'm Robot".
Alex is watching "I'm Robot".
"I'm Robot" ended.
Cleaner John is cleaning hall number 4.
'''
    assert out == output, (
        f"'movie_session' output should equal to {output}, "
        f"when hall number is {hall}, there are two customers "
        f"{customer1_name} and {customer2_name} and cleaner's "
        f"name is {cleaner_name}"
    )


def test_cinema_bar_import():
    with open(main.__file__, "r") as source:
        parsed_module = ast.parse(source.read())
        random_import = None

        for child in parsed_module.body:
            if isinstance(child, ImportFrom) and child.module == 'app.cinema.cinema_bar':
                random_import = child
    assert (
            random_import is not None
    ), "Class 'CinemaBar' should be imported using 'from'"
    assert (
            random_import.names[0].name == "CinemaBar"
    ), "Class 'CinemaBar' should be imported from 'cinema_bar' module"


def test_cinema_hall_import():
    with open(main.__file__, "r") as source:
        parsed_module = ast.parse(source.read())
        random_import = None

        for child in parsed_module.body:
            if isinstance(child, ImportFrom) and child.module == 'app.cinema.cinema_hall':
                random_import = child
    assert (
            random_import is not None
    ), "Class 'CinemaHall' should be imported using 'from'"
    assert (
            random_import.names[0].name == "CinemaHall"
    ), "Class 'CinemaHall' should be imported from 'cinema_hall' module"


def test_cleaner_import():
    with open(main.__file__, "r") as source:
        parsed_module = ast.parse(source.read())
        random_import = None

        for child in parsed_module.body:
            if isinstance(child, ImportFrom) and child.module == 'app.people.cinema_staff':
                random_import = child
    assert (
            random_import is not None
    ), "Class 'Cleaner' should be imported using 'from'"
    assert (
            random_import.names[0].name == "Cleaner"
    ), "Class 'Cleaner' should be imported from 'cinema_staff' module"


def test_customer_import():
    with open(main.__file__, "r") as source:
        parsed_module = ast.parse(source.read())
        random_import = None

        for child in parsed_module.body:
            if isinstance(child, ImportFrom) and child.module == 'app.people.customer':
                random_import = child
    assert (
            random_import is not None
    ), "Class 'Customer' should be imported using 'from'"
    assert (
            random_import.names[0].name == "Customer"
    ), "Class 'Customer' should be imported from 'customer' module"
