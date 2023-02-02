from ..user import User
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.util import sanitize_str
_logger = logging.getLogger(__name__)

Base = automap_base()

# seed init data for processes tables, the tablesmust be listed also in the seed_init_data
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
                tmp0 =  table_base(mse=0.540289623, mae=-0.909284882, r2=0.28373445, config_id=1)
                tmp1 =  table_base(mse=0.453582689, mae=-0.808478663, r2=0.708722942, config_id=1)
                tmp2 =  table_base(mse=0.540289623, mae=-0.675440952, r2=0.960191341, config_id=1)
                db.session.add(tmp0)
                db.session.add(tmp1)
                db.session.add(tmp2)
                db.session.commit()
                _logger.info("fe_training_error table seeded")        
            elif table_name == "fe_config":
                tmp0 =  table_base(active=True)
                tmp1 =  table_base(active=False)
                db.session.add(tmp0)
                db.session.add(tmp1)
                db.session.commit()
                _logger.info("fe_config table seeded")
            elif table_name == "fe_validation_error":
                tmp0 =  table_base(mse=0.540289623, mae=-0.909284882, r2=0.28373445, config_id=2)
                tmp1 =  table_base(mse=0.453582689, mae=-0.808478663, r2=0.708722942, config_id=2)
                tmp2 =  table_base(mse=0.540289623, mae=-0.675440952, r2=0.960191341, config_id=2)
                db.session.add(tmp0)
                db.session.add(tmp1)
                db.session.add(tmp2)
                db.session.commit()
                _logger.info("fe_validation_error table seeded") 
            elif table_name == "gym_fx_config":
                tmp0 =  table_base(initial_capital=10000, active=-True)
                tmp1 =  table_base(initial_capital=1000, active=-True)
                db.session.add(tmp0)
                db.session.add(tmp1)
                db.session.commit()
                _logger.info("gym_fx_config table seeded") 
            elif table_name == "gym_fx_data":
                tmp0 =  table_base(score=10000, score_v=9000, config_id=-1)
                tmp1 =  table_base(score=1000, score_v=900, config_id=-2)
                db.session.add(tmp0)
                db.session.add(tmp1)
                db.session.commit()
                _logger.info("gym_fx_data table seeded") 
        except SQLAlchemyError as e:
            error = str(e)
            print("Error : " , error)

        