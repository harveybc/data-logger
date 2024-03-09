# endpoint index functions
from sqlalchemy.exc import SQLAlchemyError
import json
from app.util import as_dict
import math
from sqlalchemy import func, asc, desc

# returns a list of the rows from the table table['name] from page_num*num_rows to page_num*num_rows+num_rows filtering on culter_col==filter_val and ordering by order_by and asc_desc
def list_data(db, Base, process, table, page_num=1, num_rows=15, filter_col=None, filter_val=None, order_by=None, asc_desc=None):
    try:
        # if filter_col is None and order_by is None, query a list of the rows from the table table['name] from page_num*num_rows to page_num*num_rows+num_rows
        if filter_col is None and order_by is None:
            res = db.session.query(Base.classes[table['name']]).offset((page_num-1)*num_rows).limit(num_rows).all()
            total_rows = db.session.query(Base.classes[table['name']]).count()
        elif filter_col is not None and order_by is None:
            # query a list of the rows from the table table['name] from page_num*num_rows to page_num*num_rows+num_rows filtering on culter_col==filter_val
            res = db.session.query(Base.classes[table['name']]).filter(Base.classes[table['name']][filter_col] == filter_val).offset((page_num-1)*num_rows).limit(num_rows).all()
            total_rows = db.session.query(Base.classes[table['name']]).filter(Base.classes[table['name']][filter_col] == filter_val).count()
        elif filter_col is None and order_by is not None:
            # query a list of the rows from the table table['name] from page_num*num_rows to page_num*num_rows+num_rows ordering by order_by and asc_desc
            res = db.session.query(Base.classes[table['name']]).order_by(asc_desc(Base.classes[table['name']][order_by])).offset((page_num-1)*num_rows).limit(num_rows).all()
            total_rows = db.session.query(Base.classes[table['name']]).order_by(asc_desc(Base.classes[table['name']][order_by])).count()
        else:
            # if both filter_col and order_by are not None
            # query query a list of the rows from the table table['name] from page_num*num_rows to page_num*num_rows+num_rows filtering on culter_col==filter_val and ordering by order_by and asc_desc
            res = db.session.query(Base.classes[table['name']]).filter(Base.classes[table['name']][filter_col] == filter_val).order_by(asc_desc(Base.classes[table['name']][order_by])).offset((page_num-1)*num_rows).limit(num_rows).all()
            total_rows = db.session.query(Base.classes[table['name']]).filter(Base.classes[table['name']][filter_col] == filter_val).order_by(asc_desc(Base.classes[table['name']][order_by])).count()
        res_list = list(map(as_dict, res))
    except SQLAlchemyError as e:
        error = str(e)
        print("SQLAlchemyError : " , error)
        return error
    except Exception as e:
        error = str(e)
        print("Error : " ,error)
        return error
    # add the total number of pages to the res_list
    res_list.append({"total_pages": math.ceil(total_rows/num_rows)})
    print("res_list : " , res_list)
    return json.dumps(res_list)    

# returns the config id  or score for the best score from table gym_fx_data that has config.active == true
def scoreboard_data(db, Base, table, col, order_by, order, foreign_key, rel_table, rel_filter_col, rel_filter_op, rel_filter_val):
    """ Returns the config id for the best score from table gym_fx_data that has config.active == true. """
    # table base class
    #Base.prepare(db.engine)
    # perform query, the column classs names are configured in config_store.json
    #params:
    #   col=config_id
    #   order_by=score
    #   order=desc
    #   foreign_key=config_id
    #   rel_table=gym_fx_config
    #   rel_filter_col=active
    #   rel_filter_op=equal
    #   rel_filter_val=True
    # create the query dependin on order and rel_filter_op, first for order==desc and rel_filter_op==equal
    base_table = Base.classes[table]
    base_rel = Base.classes[rel_table]
    res = db.session.query(base_table).join(base_rel, getattr(base_table,foreign_key) == base_rel.id).filter(getattr(base_rel,rel_filter_col) == rel_filter_val).order_by(desc(getattr(base_table,order_by))).first_or_404()
    if order == "desc" and rel_filter_op == "not_equal":
        res = db.session.query(Base.classes[table]).join(Base.classes[rel_table], Base.classes[table][foreign_key] == Base.classes[rel_table]["id"]).filter(Base.classes[rel_table][rel_filter_col] != rel_filter_val).order_by(desc(Base.classes[table][order_by])).first_or_404()
    if order == "asc" and rel_filter_op == "is_equal":
        res = db.session.query(Base.classes[table]).join(Base.classes[rel_table], Base.classes[table][foreign_key] == Base.classes[rel_table]["id"]).filter(Base.classes[rel_table][rel_filter_col] == rel_filter_val).order_by(asc(Base.classes[table][order_by])).first_or_404()
    if order == "asc" and rel_filter_op == "not_equal":
        res = db.session.query(Base.classes[table]).join(Base.classes[rel_table], Base.classes[table][foreign_key] == Base.classes[rel_table]["id"]).filter(Base.classes[rel_table][rel_filter_col] != rel_filter_val).order_by(asc(Base.classes[table][order_by])).first_or_404()
    attr = getattr(res, col)
    return json.dumps(attr)

def online_plot_data(db, Base, num_points, table, val_col, best_col, order_by, order, foreign_key, rel_table, rel_filter_col, rel_filter_op, rel_filter_val):
    """ Returns an array of points [tick_count, score] from the gym_fx_data table for thebest prcess with config_id.active== True. """
    # perform query, the column classs names are configured in config_store.json
    try:
        best = int(float(scoreboard_data(db, Base, table, best_col, order_by, order, foreign_key, rel_table, rel_filter_col, rel_filter_op, rel_filter_val)))
        print("best : " , best)
        base_table = Base.classes[table]
        points = db.session.query(base_table).filter(base_table.config_id == best).order_by(desc(base_table.id)).limit(num_points).all()
        res = []
        count = 0
        for p in points:
            res.append({"x":count, "y":p[val_col] })
            count += 1
    except Exception as e:
        error = str(e)
        print("Error 1: " ,error)
        return error
    return json.dumps(res)
