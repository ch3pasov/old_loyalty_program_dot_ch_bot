# import server.server_vars
from dataclasses import dataclass


@dataclass
class LoyaltyLevel:
    level: int
    days: int
    reward: float
    congrats_text: str = "🥳Отпраздновать!🥳"
    congrats_link: str = "https://youtu.be/LDU_Txk06tM?t=74"
