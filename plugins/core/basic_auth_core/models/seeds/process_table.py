from ..user import User
from sqlalchemy.ext.automap import automap_base
import logging
from app.util import sanitize_str
_logger = logging.getLogger(__name__)

Base = automap_base()

# add the default user with id = 0 and username = test
def seed(app, db, table_name):
    with app.app_context():
        # sanitize the input string and limit its length
        table_name = sanitize_str(table_name, 256)
        Base.prepare(db.engine, reflect=False)
        # table base class
        table_base = eval("Base.classes." + table_name)
        # perform query
        try:
            #id,mse,mae,r2,created,process_id 
            #0	0.540289623	-0.909284882	0.28373445	2020-07-06 02:20:31	0
            #1	0.453582689	-0.808478663	0.708722942	2020-07-06 02:20:32	0
            #2	0.362343707	-0.675440952	0.960191341	2020-07-06 02:20:32	0
            tmp =  User(id=0, username='test', password='pass', admin=True, email='test@test.com')
            db.session.add(tmp)
            db.session.commit()
            _logger.info(" User table seeded")        
            res = db.session.query(func.max(table_base_column)) 
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)
            res ={ 'error_ca' : error}
        return res
        