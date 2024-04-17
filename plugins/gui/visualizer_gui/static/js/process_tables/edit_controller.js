// contains a method that shows an html table containing a column for the table's column names and another columdn showing the value of each ot the table's columns for an element of the table with table.id=function_parameter  in the html element with id=detail_table, and a constructor that executes it
export class EditController {
    table = window.table;
    process = window.process;
    data_ = {};
    // replaces the contents of the html element with id=detail_table with an html table containing a column for the table's column names and another column showing the value of each of the table's columns for an element of the table with table.id=function_parameter
    constructor() {
      this.update(this.id);
    }
  
  async update(reg_id) {
    this.gui_update(this.data_);
  }  

  gui_update() {
    var p_list = "";
    for (var i = 0; i<this.table.columns.length; i++) {
      
            //<input type="text" id="fname" name="fname" value="John">
            //<label for="lname">Last name:</label>
            //<input type="text" id="lname" name="lname" value="Doe">
      p_list += "<tr>";
      p_list += "<td><label for=" + this.table.columns[i].name + ">" + this.table.columns[i].name + ":</label>" + this.table.columns[i].name + '</td><td><input type="text" id="' + this.table.columns[i].name + '" name="' + this.table.columns[i].name +'"></td>';
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

