from statemachine import StateMachine, State
from tinydb import Query

import db


class StartUpMachine(StateMachine):
    user_id = None

    not_started = State("Not started", initial=True)
    entering_login = State("Entering login")
    entering_city = State("Entering city")
    entering_oo = State("Entering OO")
    entering_school = State("Entering school")

    reset = not_started.from_(entering_login, entering_city, entering_oo, entering_school, not_started)
    sent_start = entering_login.from_(not_started)
    sent_login = entering_city.from_(entering_login)
    sent_city = entering_oo.from_(entering_city)
    sent_oo = entering_school.from_(entering_oo)

    cycle = sent_start | sent_login | sent_oo | sent_city

    @staticmethod
    def from_user_id(user_id):
        q = Query()
        try:
            p = db.db.search(q.user_id == user_id)[0]["start_value"]
        except IndexError:
            p = None
        m = StartUpMachine(start_value=p)
        m.user_id = user_id
        return m

    def save(self):
        q = Query()
        db.db.upsert({"user_id": self.user_id, "start_value": self.model.state}, q.user_id == self.user_id)


