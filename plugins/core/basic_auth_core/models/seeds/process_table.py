from ..user import User
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.util import sanitize_str
import warnings

_logger = logging.getLogger(__name__)

Base = automap_base()


# seed init data for processes tables, the tablesmust be listed also in the seed_init_data
def seed(app, db, table_name):
    with warnings.catch_warnings():
        #warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        warnings.simplefilter("ignore")

        with app.app_context():
            # sanitize the input string and limit its length
            table_name = sanitize_str(table_name, 256)
            Base.prepare(db.engine, reflect=False)
            # table base class
            table_base = eval("Base.classes." + table_name)
            # perform query
            try:
                rows=[]
                if table_name == "gym_fx_config":
                    rows.append(table_base(initial_capital=10000, active=True))
                    rows.append(table_base(initial_capital=1000, active=True))
                    rows.append(table_base(initial_capital=9000, active=False))
                    for row in rows:
                        db.session.add(row)
                    db.session.commit()
                    _logger.info("gym_fx_config table seeded") 
                elif table_name == "gym_fx_data":
                    rows.append(table_base(score=10000, score_v=9001, config_id=1))
                    rows.append(table_base(score=1000, score_v=900, config_id=2))
                    rows.append(table_base(score=1200, score_v=9900, config_id=1))
                    rows.append(table_base(score=1300, score_v=9700, config_id=3))
                    for row in rows:
                        db.session.add(row)
                    db.session.commit()
                    _logger.info("gym_fx_data table seeded") 
                elif table_name == "gym_fx_validation_plot":
                    # TODO: add reward, num_closes
                    rows.append(table_base(balance=10000, equity=10000, order_status= 0, reward=0, num_closes=0, config_id=3, tick_timestamp=0))
                    rows.append(table_base(balance=10000, equity=13000, order_status= 1, reward=0, num_closes=0 ,config_id=3, tick_timestamp=1))
                    rows.append(table_base(balance=12000, equity=12000, order_status= 0, reward=2000, num_closes=1 ,config_id=3, tick_timestamp=2))
                    rows.append(table_base(balance=12000, equity=7000, order_status= -1, reward=0, num_closes=1 ,config_id=3, tick_timestamp=3))
                    rows.append(table_base(balance=8000, equity=6000, order_status= 0, reward=-2000, num_closes=2,config_id=3, tick_timestamp=4))
                    rows.append(table_base(balance=9000, equity=8000, order_status= -1, reward=0, num_closes=2 ,config_id=3, tick_timestamp=5))
                    rows.append(table_base(balance=9000, equity=9000, order_status= 0, reward=0, num_closes=3 ,config_id=3, tick_timestamp=6))
                    rows.append(table_base(balance=9000, equity=11000, order_status= 1, reward=0, num_closes=3 ,config_id=3, tick_timestamp=7))
                    rows.append(table_base(balance=13000, equity=13000, order_status= 0 , reward=4000, num_closes=4,config_id=3, tick_timestamp=8))
                    rows.append(table_base(balance=13000, equity=12000, order_status= 1, reward=0, num_closes=4 ,config_id=3, tick_timestamp=9))
                    rows.append(table_base(balance=11000, equity=11000, order_status= 0 , reward=-2000, num_closes=5,config_id=3, tick_timestamp=10))
                    rows.append(table_base(balance=11000, equity=13000, order_status= 1, reward=0, num_closes=5 ,config_id=3, tick_timestamp=11))
                    for row in rows:
                        db.session.add(row)
                    db.session.commit()
                    _logger.info("gym_fx_validation_plot table seeded") 
            except SQLAlchemyError as e:
                error = str(e)
                print("Error : " , error)

            