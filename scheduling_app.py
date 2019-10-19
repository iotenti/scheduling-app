from app import create_app, db
from app.models import Teachers, Lessons, Recurring_pattern, Week_days,\
    Recurring_type, User, ContactType

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Teachers': Teachers, 'Lessons': Lessons,
            'Recurring_pattern': Recurring_pattern, 'Week_days': Week_days,
            'Recurring_type': Recurring_type, 'User': User, 'ContactType': ContactType
            }
# check out bottom of db chapter to expand
