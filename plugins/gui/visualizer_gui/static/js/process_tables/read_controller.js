// contains a method that shows an html table containing a column for the table's column names and another columdn showing the value of each ot the table's columns for an element of the table with table.id=function_parameter  in the html element with id=detail_table, and a constructor that executes it
export class ReadController {
    id = window.id;  
    table = window.table;
    process = window.process;

    // replaces the contents of the html element with id=detail_table with an html table containing a column for the table's column names and another column showing the value of each of the table's columns for an element of the table with table.id=function_parameter
    constructor() {
        this.read(this.id);


    }

    // suppose there is a variable called table containing an array called columns with the table's column names
    // the parameter reg_id is the id of the element of the table that we want to read
  // to read the register, we need to call an axios http request to the endpoint: '/' + this.process.name + '/' + this.table.name + '/detail/{id}', { params: {} }
    read(reg_id) {
        let url = '/' + this.process.name + '/' + this.table.name + '/detail/' + reg_id;
        axios.get(url, { params: {} })
            .then((response) => {
              let data_ = JSON.parse(response.data);
              let table = document.getElementById('detail_table');
              var p_list = "";
              
              for (let column in table.columns) {
                let col_name = column.name;
                p_list += (`<tr>`);
                p_list += (`<td>${col_name}</td><td>${data_[col_name]}</td>`);
                p_list += (`</tr>`);
              }
              table.innerHTML = p_list;
            })
            .catch((error) => {
                console.log(error);
            });
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

