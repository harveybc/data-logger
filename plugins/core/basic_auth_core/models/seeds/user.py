from .models.user import User
# add the default user with id = 0 and username = test
def seed(app, db):
    with app.app_context():
        tmp =  User(id=0, username='test', password='pass', admin=True, email='test@test.com')
        db.session.add(tmp)
        db.session.commit()