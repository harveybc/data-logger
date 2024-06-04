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
                table_name = "preprocessor"
                rows=[]
                # table base class
                table_base = Base.classes[table_name]
                #append rows
                rows.append(table_base(json_config='{"csv_file": ".\\tests\\datasets\\EURUSD_5m_2006_2007.csv", "output_file": "./csv_output.csv", "plugin_name": "default_plugin", "method": "min-max", "range": [0.0, 1.0], "save_config": "out_config.json", "load_config": "./config_in.json", "quiet_mode": false, "remote_log": null, "remote_config": null}' ))
                # add all the rows to the session
                for row in rows:
                    db.session.add(row)
                # commit the session to the database
                db.session.commit()
                _logger.info(table_name + "table seeded") 
                
            # "fe_config":
                table_name = "fe_config"
                rows=[]
                # table base class
                table_base = Base.classes[table_name]
                #append rows
                rows.append(table_base(csv_file="EURUSD_5m_mar2014_mar2024_preprocessed.csv", 
                                        save_encoder="EURUSD_5m_mar2014_mar2024_encoder.h5", 
                                        save_decoder="EURUSD_5m_mar2014_mar2024_decoder.h5", 
                                        load_encoder="EURUSD_5m_mar2014_mar2024_encoder.h5", 
                                        load_decoder="EURUSD_5m_mar2014_mar2024_decoder.h5", 
                                        evaluate_encoder="EURUSD_5m_mar2014_mar2024_encoder.h5", 
                                        evaluate_decoder="EURUSD_5m_mar2014_mar2024_decoder.h5", 
                                        encoder_plugin="cnn", 
                                        decoder_plugin="cnn", 
                                        window_size=512, 
                                        max_error=0.1, 
                                        initial_size=256, 
                                        step_size=16, 
                                        remote_log="http://localhost:60500/feature_extractor/fe_training_error/1", 
                                        quiet_mode=0, 
                                        active=True))
                rows.append(table_base(csv_file="EURUSD_15m_mar2014_mar2024_preprocessed.csv",
                                        save_encoder="EURUSD_15m_mar2014_mar2024_encoder.h5",
                                        save_decoder="EURUSD_15m_mar2014_mar2024_decoder.h5",
                                        load_encoder="EURUSD_15m_mar2014_mar2024_encoder.h5",
                                        load_decoder="EURUSD_15m_mar2014_mar2024_decoder.h5",
                                        evaluate_encoder="EURUSD_15m_mar2014_mar2024_encoder.h5",
                                        evaluate_decoder="EURUSD_15m_mar2014_mar2024_decoder.h5",
                                        encoder_plugin="cnn",
                                        decoder_plugin="cnn",
                                        window_size=256,
                                        max_error=0.1,
                                        initial_size=128,
                                        step_size=8,
                                        remote_log="http://localhost:60500/feature_extractor/fe_training_error/2",
                                        quiet_mode=0,
                                        active=True))
                rows.append(table_base(csv_file="EURUSD_1h_mar2014_mar2024_preprocessed.csv", 
                                        save_encoder="EURUSD_1h_mar2014_mar2024_encoder.h5", 
                                        save_decoder="EURUSD_1h_mar2014_mar2024_decoder.h5", 
                                        load_encoder="EURUSD_1h_mar2014_mar2024_encoder.h5", 
                                        load_decoder="EURUSD_1h_mar2014_mar2024_decoder.h5", 
                                        evaluate_encoder="EURUSD_1h_mar2014_mar2024_encoder.h5", 
                                        evaluate_decoder="EURUSD_1h_mar2014_mar2024_decoder.h5", 
                                        encoder_plugin="cnn", 
                                        decoder_plugin="cnn", 
                                        window_size=128, 
                                        max_error=0.1, 
                                        initial_size=64, 
                                        step_size=4, 
                                        remote_log="http://localhost:60500/feature_extractor/fe_training_error/3", 
                                        quiet_mode=0, 
                                        active=True))
                rows.append(table_base(csv_file="EURUSD_4h_mar2014_mar2024_preprocessed.csv",
                                            save_encoder="EURUSD_4h_mar2014_mar2024_encoder.h5",
                                            save_decoder="EURUSD_4h_mar2014_mar2024_decoder.h5",
                                            load_encoder="EURUSD_4h_mar2014_mar2024_encoder.h5",
                                            load_decoder="EURUSD_4h_mar2014_mar2024_decoder.h5",
                                            evaluate_encoder="EURUSD_4h_mar2014_mar2024_encoder.h5",
                                            evaluate_decoder="EURUSD_4h_mar2014_mar2024_decoder.h5",
                                            encoder_plugin="cnn",
                                            decoder_plugin="cnn",
                                            window_size=64,
                                            max_error=0.1,
                                            initial_size=32,
                                            step_size=2,
                                            remote_log="http://localhost:60500/feature_extractor/fe_training_error/4",
                                            quiet_mode=0,
                                            active=True))                            
                rows.append(table_base(csv_file="EURUSD_1d_mar2014_mar2024_preprocessed.csv",
                                            save_encoder="EURUSD_4h_mar2014_mar2024_encoder.h5",
                                            save_decoder="EURUSD_4h_mar2014_mar2024_decoder.h5",
                                            load_encoder="EURUSD_4h_mar2014_mar2024_encoder.h5",
                                            load_decoder="EURUSD_4h_mar2014_mar2024_decoder.h5",
                                            evaluate_encoder="EURUSD_4h_mar2014_mar2024_encoder.h5",
                                            evaluate_decoder="EURUSD_4h_mar2014_mar2024_decoder.h5",
                                            encoder_plugin="cnn",
                                            decoder_plugin="cnn",
                                            window_size=32,
                                            max_error=0.1,
                                            initial_size=16,
                                            step_size=1,
                                            remote_log="http://localhost:60500/feature_extractor/fe_training_error/5",
                                            quiet_mode=0,
                                            active=True))                            
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

            