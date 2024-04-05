// contains a method that shows an html table containing a column for the table's column names and another columdn showing the value of each ot the table's columns for an element of the table with table.id=function_parameter  in the html element with id=detail_table, and a constructor that executes it
export class ReadController {
    id = window.id;  
    table = window.table;
    process = window.process;
    data_ = {};
    // replaces the contents of the html element with id=detail_table with an html table containing a column for the table's column names and another column showing the value of each of the table's columns for an element of the table with table.id=function_parameter
    constructor() {
        console.log("this.id: " + this.id);
        this.update(this.id);
        setTimeout(function () { this.gui_update(this.data_); }.bind(this), 1500);
        
    }
  
  async update(reg_id) {
    var that = this;
    await this.data_request(reg_id).then((response) => {
      that.gui_update(that.data_);
    }, (error) => {
      console.log(error);
    });
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

  
  gui_update(data_) {
    console.log(data_); 
    var p_list = "";
    for (var column in this.table.columns) {
      let col_name = column.name;
      p_list += "<tr>";
      p_list += "<td>"+ col_name +"</td><td>" + data_[col_name]+"</td>";
      p_list += "</tr>";
    }
    document.getElementById('detail_table').innerHTML = p_list;
  }  

  // returns an axios instance for basic authentication
  axiosBasicAuth(username, password) {
    let buffer_auth = buffer.Buffer.from(username + ':' + password);
    let b64 = buffer_auth.toString('base64');
    return axios.create({
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${b64}`,
      }
    });
  }
  // returns an axios instance with configured basic authentication
  // TODO: change to use current user
  axios_auth_instance() {
    let axios_instance = this.axiosBasicAuth("test", "pass");
    return axios_instance;
  }
  
}

