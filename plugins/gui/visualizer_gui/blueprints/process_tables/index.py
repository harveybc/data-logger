# endpoint index functions
from sqlalchemy.exc import SQLAlchemyError
import json
from app.util import as_dict

# returns a list of the rows from the table table['name] from page_num*num_rows to page_num*num_rows+num_rows filtering on culter_col==filter_val and ordering by order_by and asc_desc
def list_data_index(db, Base, process, table, page_num=1, num_rows=15, filter_col=None, filter_val=None, order_by=None, asc_desc=None):
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
    res_list.append({"total_pages": total_rows/num_rows})

    print("res_list : " , res_list)
    return json.dumps(res_list)    
    