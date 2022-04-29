from typing import Dict, List

from datetime import datetime
import smtplib
import hashlib

from db import Group, User
from db import Session

from config import smtp_server as server, smtp_sender as sender

body = """Subject: Your credentials for the VAST Annotation Tool

Dear Evaluator,

Thank you for taking part in the VAST Annotation Usability Evaluation.
Your credentials are:
username: {}
password: {}

Looking forward to your contribution.

Best regards,
The VAST project team"""


def send_mail(email: str, user: str, password: str):
    smtplib.SMTP(server).sendmail(sender, email, body.format(user, password))


def get_groups() -> List[Group]:
    s = Session()
    result = s.query(Group).all()
    # s.commit()
    return result


def get_available_users(
    group_id: int, email: str = None, hide_used: bool = False
) -> Dict[str, str]:
    s = Session()
    if email:
        owner = hashlib.sha256(email.encode("UTF-8")).hexdigest()
        u = s.query(User).filter(User.owner == owner).first()
        if u:
            return [{"id": u.id, "name": u.name, "available": True}]
    q = s.query(User).filter(User.group_id == group_id)
    if hide_used:
        q = q.filter(User.date is None)
    return [{"id": u.id, "name": u.name, "available": not u.date} for u in q.all()]


def assign_user(group_id: int, user_id: int, email: str) -> Dict[str, str]:
    s = Session()
    owner = hashlib.sha256(email.encode("UTF-8")).hexdigest()
    u = s.query(User).filter(User.owner == owner).first()
    if not u:
        u = s.query(User).filter(User.group_id == group_id, User.id == user_id).first()
        if not u:
            return {}
        u.date = datetime.now()
        u.owner = owner
        send_mail(email, u.name, u.password)
    result = {"name": u.name, "password": u.password}
    s.add(u)
    s.commit()
    return result
