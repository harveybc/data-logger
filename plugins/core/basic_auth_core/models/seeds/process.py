from ...models.process import Process
# add the default process with id = 0
def seed(app, db):
    with app.app_context():
        tmp =  Process(name='default', description="default process", tables="[]", user_id=0)
        db.session.add(tmp)
        db.session.commit()