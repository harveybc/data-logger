from ..user import User
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.util import sanitize_str
import warnings

_logger = logging.getLogger(__name__)

Base = automap_base()


# seed init data for processes tables, the tablesmust be listed also in the seed_init_data
def seed(app, db):
    with warnings.catch_warnings():
        #warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        warnings.simplefilter("ignore")

        with app.app_context():
            # sanitize the input string and limit its length
            Base.prepare(db.engine, reflect=False)
            # perform query
            try:
            # "preprocessor":
                table_name = "feature_selector"
                rows=[]
                # table base class
                table_base = Base.classes[table_name]
                #append rows
                rows.append(table_base(json_config='{"csv_file": "tests\\data\\EURUSD_5m_2006_2007.csv", "plugin": "feature_selector", "method": "select_single", "single": 3}' ))
                # add all the rows to the session
                for row in rows:
                    db.session.add(row)
                # commit the session to the database
                db.session.commit()
                _logger.info(table_name + " table seeded") 
                
            # "fe_training_error":
                rows=[]
                table_name = "fe_training_error"
                # table base class
                table_base = Base.classes[table_name]
                #append rows
                rows.append(table_base(mse=0.9, interface_size=256, config_id=1))
                rows.append(table_base(mse=0.9, interface_size=128, config_id=2))
                rows.append(table_base(mse=0.9, interface_size=64, config_id=3))
                rows.append(table_base(mse=0.9, interface_size=32, config_id=4))
                rows.append(table_base(mse=0.9, interface_size=16, config_id=5))
                # add all the rows to the session
                for row in rows:
                    db.session.add(row)
                db.session.commit()
                _logger.info(table_name + " table seeded") 
            
            except SQLAlchemyError as e:
                error = str(e)
                print("Error : " , error)

            