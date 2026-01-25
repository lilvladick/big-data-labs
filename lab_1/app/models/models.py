from __future__ import annotations

from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, DateTime, ForeignKey, Numeric, Text, Boolean, LargeBinary, func, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()

film_actor_table = Table(
    "film_actor",
    Base.metadata,
    Column("actor_id", Integer, ForeignKey("actor.actor_id"), primary_key=True),
    Column("film_id", Integer, ForeignKey("film.film_id"), primary_key=True),
    Column("last_update", DateTime, nullable=False, server_default=func.now()),
)

film_category_table = Table(
    "film_category",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("film.film_id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("category.category_id"), primary_key=True),
    Column("last_update", DateTime, nullable=False, server_default=func.now()),
)


class Language(Base):
    __tablename__ = "language"

    language_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    films: Mapped[List["Film"]] = relationship(back_populates="language", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Language(id={self.language_id} name={self.name!r})>"


class Film(Base):
    __tablename__ = "film"

    film_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    release_year: Mapped[Optional[int]] = mapped_column(Integer)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.language_id"), nullable=False)
    original_language_id: Mapped[Optional[int]] = mapped_column(ForeignKey("language.language_id"), nullable=True)
    rental_duration: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    rental_rate: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False, default=Decimal("4.99"))
    length: Mapped[Optional[int]] = mapped_column(Integer)
    replacement_cost: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal("19.99"))
    rating: Mapped[Optional[str]] = mapped_column(String(10))
    special_features: Mapped[Optional[str]] = mapped_column(String(255))
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    language: Mapped["Language"] = relationship(
        "Language",
        foreign_keys=[language_id],
        back_populates="films",
        lazy="selectin",
    )
    original_language: Mapped[Optional["Language"]] = relationship(
        "Language",
        foreign_keys=[original_language_id],
        lazy="selectin",
    )

    actors: Mapped[List["Actor"]] = relationship(
        "Actor",
        secondary=film_actor_table,
        back_populates="films",
        lazy="selectin",
    )
    categories: Mapped[List["Category"]] = relationship(
        "Category",
        secondary=film_category_table,
        back_populates="films",
        lazy="selectin",
    )
    inventories: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="film", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Film(id={self.film_id} title={self.title!r})>"


class Actor(Base):
    __tablename__ = "actor"

    actor_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(45), nullable=False)
    last_name: Mapped[str] = mapped_column(String(45), nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    films: Mapped[List["Film"]] = relationship(
        "Film",
        secondary=film_actor_table,
        back_populates="actors",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Actor(id={self.actor_id} name={self.first_name} {self.last_name})>"


class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    films: Mapped[List["Film"]] = relationship(
        "Film",
        secondary=film_category_table,
        back_populates="categories",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.category_id} name={self.name!r})>"


class Country(Base):
    __tablename__ = "country"

    country_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    cities: Mapped[List["City"]] = relationship("City", back_populates="country", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Country(id={self.country_id} name={self.country!r})>"


class City(Base):
    __tablename__ = "city"

    city_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.country_id"), nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    country: Mapped["Country"] = relationship("Country", back_populates="cities")
    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="city", lazy="selectin")

    def __repr__(self) -> str:
        return f"<City(id={self.city_id} name={self.city!r})>"


class Address(Base):
    __tablename__ = "address"

    address_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    address2: Mapped[Optional[str]] = mapped_column(String(50))
    district: Mapped[str] = mapped_column(String(20), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.city_id"), nullable=False)
    postal_code: Mapped[Optional[str]] = mapped_column(String(10))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    city: Mapped["City"] = relationship("City", back_populates="addresses")
    customers: Mapped[List["Customer"]] = relationship("Customer", back_populates="address", lazy="selectin")
    staff: Mapped[List["Staff"]] = relationship("Staff", back_populates="address", lazy="selectin")
    stores: Mapped[List["Store"]] = relationship("Store", back_populates="address", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Address(id={self.address_id} address={self.address!r})>"


class Staff(Base):
    __tablename__ = "staff"

    staff_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(45), nullable=False)
    last_name: Mapped[str] = mapped_column(String(45), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("address.address_id"), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(50))
    store_id: Mapped[int] = mapped_column(ForeignKey("store.store_id"), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    username: Mapped[str] = mapped_column(String(16), nullable=False)
    password: Mapped[Optional[str]] = mapped_column(String(255))
    picture: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    address: Mapped["Address"] = relationship("Address", back_populates="staff")
    # relationship to Store (Store declared below)
    store: Mapped["Store"] = relationship("Store", back_populates="staff_members", foreign_keys=[store_id])
    rentals: Mapped[List["Rental"]] = relationship("Rental", back_populates="staff", lazy="selectin")
    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="staff", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Staff(id={self.staff_id} name={self.first_name} {self.last_name})>"


class Store(Base):
    __tablename__ = "store"

    store_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    manager_staff_id: Mapped[int] = mapped_column(ForeignKey("staff.staff_id"), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("address.address_id"), nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    manager: Mapped["Staff"] = relationship("Staff", foreign_keys=[manager_staff_id], backref="manages_store")
    address: Mapped["Address"] = relationship("Address", back_populates="stores")
    inventories: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="store", lazy="selectin")
    customers: Mapped[List["Customer"]] = relationship("Customer", back_populates="store", lazy="selectin")
    staff_members: Mapped[List["Staff"]] = relationship("Staff", back_populates="store", foreign_keys=[Staff.store_id])

    def __repr__(self) -> str:
        return f"<Store(id={self.store_id})>"


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    film_id: Mapped[int] = mapped_column(ForeignKey("film.film_id"), nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey("store.store_id"), nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    film: Mapped["Film"] = relationship("Film", back_populates="inventories")
    store: Mapped["Store"] = relationship("Store", back_populates="inventories")
    rentals: Mapped[List["Rental"]] = relationship("Rental", back_populates="inventory", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Inventory(id={self.inventory_id} film_id={self.film_id})>"


class Customer(Base):
    __tablename__ = "customer"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("store.store_id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(45), nullable=False)
    last_name: Mapped[str] = mapped_column(String(45), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(50))
    address_id: Mapped[int] = mapped_column(ForeignKey("address.address_id"), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    store: Mapped["Store"] = relationship("Store", back_populates="customers")
    address: Mapped["Address"] = relationship("Address", back_populates="customers")
    rentals: Mapped[List["Rental"]] = relationship("Rental", back_populates="customer", lazy="selectin")
    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="customer", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Customer(id={self.customer_id} name={self.first_name} {self.last_name})>"


class Rental(Base):
    __tablename__ = "rental"

    rental_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rental_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    inventory_id: Mapped[int] = mapped_column(ForeignKey("inventory.inventory_id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.customer_id"), nullable=False)
    return_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.staff_id"), nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    inventory: Mapped["Inventory"] = relationship("Inventory", back_populates="rentals")
    customer: Mapped["Customer"] = relationship("Customer", back_populates="rentals")
    staff: Mapped["Staff"] = relationship("Staff", back_populates="rentals")
    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="rental", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Rental(id={self.rental_id} date={self.rental_date})>"


class Payment(Base):
    __tablename__ = "payment"

    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.customer_id"), nullable=False)
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.staff_id"), nullable=False)
    rental_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rental.rental_id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    payment_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    customer: Mapped["Customer"] = relationship("Customer", back_populates="payments")
    staff: Mapped["Staff"] = relationship("Staff", back_populates="payments")
    rental: Mapped[Optional["Rental"]] = relationship("Rental", back_populates="payments")

    def __repr__(self) -> str:
        return f"<Payment(id={self.payment_id} amount={self.amount})>"
