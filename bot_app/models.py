from dataclasses import dataclass


@dataclass
class User:
    __collection__ = 'users'
    user_id: int
    username: str
    first_name: str
    real_name: str = None
    phone_number: str = None
    email_address: str = None
    nation: str = None
    geo: str = None
    menu_id: int = None
    state: str = None
    avatar_b64: str = None
    register_time: str = None
