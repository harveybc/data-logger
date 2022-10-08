from ...models.process import Process
import logging
_logger = logging.getLogger(__name__)
# add the default process with id = 0
def seed(app, db):
    with app.app_context():
        tmp =  Process(name='default', description="default process", tables="[]", user_id=1)
        db.session.add(tmp)
        db.session.commit()
        _logger.info(" Process table seeded")