from models.user import User

def seed(app, db):
    with app.app_context():
        tmp =  User(id=0, name='default', description="default table", tables="[]", user_id=0)
        db.session.add(tmp)
        db.session.commit()