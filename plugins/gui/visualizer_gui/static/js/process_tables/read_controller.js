// contains a method that shows an html table containing a column for the table's column names and another columdn showing the value of each ot the table's columns for an element of the table with table.id=function_parameter  in the html element with id=detail_table, and a constructor that executes it
export class ReadController {
    id = window.id;  
    table = window.table;
    process = window.process;
    data_ = {};
    // replaces the contents of the html element with id=detail_table with an html table containing a column for the table's column names and another column showing the value of each of the table's columns for an element of the table with table.id=function_parameter
    constructor() {
        this.update(this.id);
    }
  
    // call request that returns the config id for the best mse from table fe_training_error that has config.active == true
  data_request(reg_id) {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    var that = this;
    var url = '/' + this.process.name + '/' + this.table.name + '/detail/' + reg_id;
    // get the best config_id 
    return axios_instance.get(url)
      .then((response) => {
        that.data_ = response.data;
      }, (error) => {
        that.data_ = error.message;
        console.log(error);
      });
  }
  
  // suppose there is a variable called table containing an array called columns with the table's column names
  // the parameter reg_id is the id of the element of the table that we want to read
  // to read the register, we need to call an axios http request to the endpoint: '/' + this.process.name + '/' + this.table.name + '/detail/{id}', { params: {} }
  update(reg_id) {
    var that = this;
    this.data_request(reg_id).then((response) => {
      document.getElementById('detail_table').innerHTML = that.gui_update(that.data_);
    }, (error) => {
      console.log(error);
    });
  }  
  
  gui_update(data_) {
    console.log(data_); 
    var p_list = "";
    for (var column in this.table.columns) {
      let col_name = column.name;
      p_list += (`<tr>`);
      p_list += (`<td>${col_name}</td><td>${data_[col_name]}</td>`);
      p_list += (`</tr>`);
    }
    return p_list;
  }  
  // updates the list of the table in the index view
  // params: start: the starting index of the data_ array
  //         num_rows: the number of rows to be added to the table
  //         data_: the data array
  detail_table_update(data_) {
    var p_list = "";
    // verify if is defined p_config_gui.gui_plugin_config[table['name']].index.columns_visible and show those columns in the row
    if (((this.p_config_gui.gui_plugin_config[table['name']]) && (this.p_config_gui.gui_plugin_config[table['name']].index)) && (this.p_config_gui.gui_plugin_config[table['name']].index.columns_visible)) {
      // for each table['columns'] create a new row of the table in the html element with id index_list
      p_list += (`<tr>`);
      for (let j = 0; j < this.p_config_gui.gui_plugin_config[table['name']].index.columns_visible.length; j++) {
        let col = this.p_config_gui.gui_plugin_config[table['name']].index.columns_visible[j];
        p_list += (`<td>${data_[i][col]}</td>`);
      }
      //p_list += "<td>View</td><td>Edit</td><td>Delete</td>"
      p_list += '<td><a href="/' + this.process.name + "/" + this.table.name + "/view_detail/" + data_[i]["id"] + '"><i class="fas fa-eye"></i></a></td>';
      p_list += '<td><a href="/' + this.process.name + "/" + this.table.name + "/view_edit/" + data_[i]["id"] + '"><i class="fas fa-pen"></i></a></td>';
      p_list += '<td><a href="/' + this.process.name + "/" + this.table.name + "/view_remove/" + data_[i]["id"] + '"><i class="fas fa-trash"></i></a></td>';
      p_list += (`</tr>`);
    }
    // else show all columns in the table.columns list
    else {
      // for each table['columns'] create a new row of the table in the html element with id index_list
      p_list += (`<tr>`);
      p_list += (`<td>${data_[i]['id']}</td>`);
      for (let j = 0; j < table.columns.length; j++) {
        let col = table.columns[j].name;
        p_list += (`<td>${data_[i][col]}</td>`);
      }
      p_list += '<td><a href="/' + this.process.name + "/" + this.table.name + "/view_detail/" + data_[i]["id"] + '"><i class="fas fa-eye"></i></a></td>';
      p_list += '<td><a href="/' + this.process.name + "/" + this.table.name + "/view_edit/" + data_[i]["id"] + '"><i class="fas fa-pen"></i></a></td>';
      p_list += '<td><a href="/' + this.process.name + "/" + this.table.name + "/view_remove/" + data_[i]["id"] + '"><i class="fas fa-trash"></i></a></td>';
      p_list += (`</tr>`);
    }
  }
}

