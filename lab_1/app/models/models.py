from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, Enum, ARRAY, ForeignKey, func, SmallInteger, LargeBinary
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Actor(Base):
    __tablename__ = 'actor'
    actor_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    films = relationship('Film', secondary='film_actor', back_populates='actors')

class Address(Base):
    __tablename__ = 'address'
    address_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    address = Column(String(50), nullable=False)
    address2 = Column(String(50))
    district = Column(String(20), nullable=False)
    city_id = Column(SmallInteger, ForeignKey('city.city_id'), nullable=False)
    postal_code = Column(String(10))
    phone = Column(String(20), nullable=False)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    city = relationship('City', back_populates='addresses')
    customers = relationship('Customer', back_populates='address')
    staffs = relationship('Staff', back_populates='address')
    stores = relationship('Store', back_populates='address')

class Category(Base):
    __tablename__ = 'category'
    category_id = Column(SmallInteger, primary_key=True, autoincrement=True)  # TINYINT
    name = Column(String(25), nullable=False)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    films = relationship('Film', secondary='film_category', back_populates='categories')

class City(Base):
    __tablename__ = 'city'
    city_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    city = Column(String(50), nullable=False)
    country_id = Column(SmallInteger, ForeignKey('country.country_id'), nullable=False)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    country = relationship('Country', back_populates='cities')
    addresses = relationship('Address', back_populates='city')

class Country(Base):
    __tablename__ = 'country'
    country_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    country = Column(String(50), nullable=False)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    cities = relationship('City', back_populates='country')

class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    store_id = Column(SmallInteger, ForeignKey('store.store_id'), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(50))
    address_id = Column(SmallInteger, ForeignKey('address.address_id'), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    create_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now())

    address = relationship('Address', back_populates='customers')
    store = relationship('Store', back_populates='customers')
    payments = relationship('Payment', back_populates='customer')
    rentals = relationship('Rental', back_populates='customer')

class Film(Base):
    __tablename__ = 'film'
    film_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    release_year = Column(Integer)  # YEAR
    language_id = Column(SmallInteger, ForeignKey('language.language_id'), nullable=False)
    original_language_id = Column(SmallInteger, ForeignKey('language.language_id'))
    rental_duration = Column(SmallInteger, nullable=False, default=3)
    rental_rate = Column(Float, nullable=False, default=4.99)
    length = Column(SmallInteger)
    replacement_cost = Column(Float, nullable=False, default=19.99)
    rating = Column(Enum('G', 'PG', 'PG-13', 'R', 'NC-17', name='film_rating'), default='G')
    special_features = Column(ARRAY(String))
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    language = relationship('Language', foreign_keys=[language_id], back_populates='films')
    original_language = relationship('Language', foreign_keys=[original_language_id], back_populates='original_films')
    actors = relationship('Actor', secondary='film_actor', back_populates='films')
    categories = relationship('Category', secondary='film_category', back_populates='films')
    inventories = relationship('Inventory', back_populates='film')

class FilmActor(Base):
    __tablename__ = 'film_actor'
    actor_id = Column(SmallInteger, ForeignKey('actor.actor_id'), primary_key=True)
    film_id = Column(SmallInteger, ForeignKey('film.film_id'), primary_key=True)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

class FilmCategory(Base):
    __tablename__ = 'film_category'
    film_id = Column(SmallInteger, ForeignKey('film.film_id'), primary_key=True)
    category_id = Column(SmallInteger, ForeignKey('category.category_id'), primary_key=True)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

class FilmText(Base):
    __tablename__ = 'film_text'
    film_id = Column(SmallInteger, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)

class Inventory(Base):
    __tablename__ = 'inventory'
    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    film_id = Column(SmallInteger, ForeignKey('film.film_id'), nullable=False)
    store_id = Column(SmallInteger, ForeignKey('store.store_id'), nullable=False)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    film = relationship('Film', back_populates='inventories')
    store = relationship('Store', back_populates='inventories')
    rentals = relationship('Rental', back_populates='inventory')

class Language(Base):
    __tablename__ = 'language'
    language_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    films = relationship('Film', foreign_keys='Film.language_id', back_populates='language')
    original_films = relationship('Film', foreign_keys='Film.original_language_id', back_populates='original_language')

class Payment(Base):
    __tablename__ = 'payment'
    payment_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    customer_id = Column(SmallInteger, ForeignKey('customer.customer_id'), nullable=False)
    staff_id = Column(SmallInteger, ForeignKey('staff.staff_id'), nullable=False)
    rental_id = Column(Integer, ForeignKey('rental.rental_id'))
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship('Customer', back_populates='payments')
    staff = relationship('Staff', back_populates='payments')
    rental = relationship('Rental', back_populates='payments')

class Rental(Base):
    __tablename__ = 'rental'
    rental_id = Column(Integer, primary_key=True, autoincrement=True)
    rental_date = Column(DateTime, nullable=False)
    inventory_id = Column(Integer, ForeignKey('inventory.inventory_id'), nullable=False)
    customer_id = Column(SmallInteger, ForeignKey('customer.customer_id'), nullable=False)
    return_date = Column(DateTime)
    staff_id = Column(SmallInteger, ForeignKey('staff.staff_id'), nullable=False)  # TINYINT
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    customer = relationship('Customer', back_populates='rentals')
    inventory = relationship('Inventory', back_populates='rentals')
    staff = relationship('Staff', back_populates='rentals')
    payments = relationship('Payment', back_populates='rental')

class Staff(Base):
    __tablename__ = 'staff'
    staff_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    address_id = Column(SmallInteger, ForeignKey('address.address_id'), nullable=False)
    picture = Column(LargeBinary)
    email = Column(String(50))
    store_id = Column(SmallInteger, ForeignKey('store.store_id'), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    username = Column(String(16), nullable=False)
    password = Column(String(40))
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    address = relationship('Address', back_populates='staffs')
    store = relationship('Store', back_populates='staffs')
    managed_stores = relationship('Store', back_populates='manager_staff', foreign_keys='Store.manager_staff_id')
    payments = relationship('Payment', back_populates='staff')
    rentals = relationship('Rental', back_populates='staff')

class Store(Base):
    __tablename__ = 'store'
    store_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    manager_staff_id = Column(SmallInteger, ForeignKey('staff.staff_id'), nullable=False)
    address_id = Column(SmallInteger, ForeignKey('address.address_id'), nullable=False)
    last_update = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    address = relationship('Address', back_populates='stores')
    manager_staff = relationship('Staff', back_populates='managed_stores')
    customers = relationship('Customer', back_populates='store')
    inventories = relationship('Inventory', back_populates='store')
    staffs = relationship('Staff', back_populates='store')