from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Setup SQLAlchemy
Base = declarative_base()
engine = create_engine("sqlite:///expenses.db")
Session = sessionmaker(bind=engine)
session = Session()


# Define tables
class SpendingCycle(Base):
    __tablename__ = "spending_cycles"
    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    price = Column(Float)
    date = Column(Date)
    cycle_id = Column(Integer)
    currency = Column(String)


# Create tables
Base.metadata.create_all(engine)


# Function to add a new cycle
def add_new_cycle(start_date):
    end_date = start_date + timedelta(days=30)
    cycle = SpendingCycle(start_date=start_date, end_date=end_date)
    session.add(cycle)
    session.commit()
    return cycle.id


# Function to add an expense
def add_expense(category, date, cycle_id, currency, price):
    expense = Expense(
        category=category, price=price, date=date, cycle_id=cycle_id, currency=currency
    )
    session.add(expense)
    session.commit()


# Function to get all expenses for a specific cycle
def get_expenses_by_cycle(cycle_id):
    return session.query(Expense).filter(Expense.cycle_id == cycle_id).all()
