from ...models.user import User
import logging
_logger = logging.getLogger(__name__)
# add the default user with id = 0 and username = test
def seed(app, db):
    _logger.info(" Seeding user table..")
    with app.app_context():
        tmp =  User( username='test', password='pass', admin=True, email='test@test.com')
        db.session.add(tmp)
        db.session.commit()
        _logger.info(" User table seeded")