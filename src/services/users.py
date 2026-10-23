from src.repositories import users as user_repo

def get_user_events(user_id: int):
    return user_repo.select_user_events(user_id)
