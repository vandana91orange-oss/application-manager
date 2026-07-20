from app.database import SessionLocal
from app.seeders.role_seeder import seed_roles
from app.seeders.admin_seeder import seed_admin_user



def run_seeders():

    db = SessionLocal()

    try:
        seed_roles(db)
        seed_admin_user(db)

    finally:
        db.close()


if __name__ == "__main__":
    run_seeders()