from sqlalchemy.orm import Session
from app.repositories.user import get_dashboard_counts_repo
from app.schema.users import DashboardCounts

def get_dashboard_counts(user_id: int, db:Session) -> DashboardCounts:
    counts = get_dashboard_counts_repo(db, user_id)
    return counts