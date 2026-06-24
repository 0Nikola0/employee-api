import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from repository.conn_setup import SessionLocal, engine
from models.db import Base, Employee

Base.metadata.create_all(bind=engine)

employees = [
    {
        "date_of_birth": date(1990, 6, 29),
        "image": "https://lorempixel.com/640/480/people/?96612",
        "email": "andres34@gmail.com",
        "first_name": "Dayni",
        "last_name": "Mayez",
        "title": "Mr.",
        "address": "18342 Alisa Square Suite 259",
        "country": "USA",
        "bio": "Experienced software engineer with a passion for backend systems.",
        "rating": 3.06,
    },
    {
        "date_of_birth": date(1985, 3, 14),
        "image": "https://lorempixel.com/640/480/people/?96612",
        "email": "sarah.connor@example.com",
        "first_name": "Sarah",
        "last_name": "Connor",
        "title": "Ms.",
        "address": "9432 Maple Drive Apt 4B",
        "country": "USA",
        "bio": "Project manager with 10 years of experience in agile environments.",
        "rating": 4.75,
    },
    {
        "date_of_birth": date(1992, 11, 2),
        "image": "https://lorempixel.com/640/480/people/?96612",
        "email": "luca.bianchi@example.com",
        "first_name": "Luca",
        "last_name": "Bianchi",
        "title": "Mr.",
        "address": "Via Roma 12, Floor 3",
        "country": "Italy",
        "bio": "Frontend developer specializing in React and design systems.",
        "rating": 4.20,
    },
    {
        "date_of_birth": date(1988, 7, 19),
        "image": "https://lorempixel.com/640/480/people/?96612",
        "email": "amina.yilmaz@example.com",
        "first_name": "Amina",
        "last_name": "Yilmaz",
        "title": "Dr.",
        "address": "Bağcılar Cad. No:5",
        "country": "Turkey",
        "bio": "Data scientist focused on NLP and machine learning pipelines.",
        "rating": 4.90,
    },
    {
        "date_of_birth": date(1995, 1, 8),
        "image": "https://lorempixel.com/640/480/people/?96612",
        "email": "james.okafor@example.com",
        "first_name": "James",
        "last_name": "Okafor",
        "title": "Mr.",
        "address": "14 Broad Street, Victoria Island",
        "country": "Nigeria",
        "bio": "DevOps engineer with expertise in Kubernetes and CI/CD pipelines.",
        "rating": 3.85,
    },
]


def populate():
    db = SessionLocal()
    try:
        for data in employees:
            employee = Employee(**data)
            db.add(employee)

        db.commit()
        print(f"Populated {len(employees)} employees.")

    except Exception as e:
        db.rollback()
        print(f"Error populating DB: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    populate()
