from ..user import User
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
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
            if table_name == "fe_training_error":
                tmp0 =  table_base(id=0, mse=0.540289623, mae=-0.909284882, r2=0.28373445, config_id=0)
                tmp1 =  table_base(id=1, mse=0.453582689, mae=-0.808478663, r2=0.708722942, config_id=0)
                tmp2 =  table_base(id=2, mse=0.540289623, mae=-0.675440952, r2=0.960191341, config_id=0)
                db.session.add(tmp0)
                db.session.add(tmp1)
                db.session.add(tmp2)
                db.session.commit()
                _logger.info("fe_training_error table seeded")        
            elif table_name == "fe_config":
                tmp0 =  table_base(id=0, active=True)
                db.session.add(tmp0)
                db.session.commit()
                _logger.info("fe_config table seeded")

        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)

        