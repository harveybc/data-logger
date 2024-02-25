// process tables index view controller
export class IndexController {
  p_conf_gui = window.p_config_gui;
  p_conf_store = window.p_config_store;
  process = window.process;
  table = window.table;
  page_num = window.page_num;

  constructor() {
    // get gymfx_process_list data from the server
    var that = this;
    this.request_view_data().then((response) => {
      that.index_list_update(0, 20, response.data);
    })
  }

  request_view_data() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    let num_rows=25;
    // get the number of rows to be shown in the index view
    if (p_config_gui.gui_plugin_config[table['name']].index.num_rows) {
      num_rows = p_config_gui.gui_plugin_config[table['name']].index.num_rows;
    }
    // use the result of api request
    return axios_instance.get('/' + this.process.name + '/' + this.table.name + '/index_list_data', { params: { "page_num": this.page_num,  "num_rows": num_rows } })
  }

  // updates the list of the table in the index view
  // params: start: the starting index of the data_ array
  //         num_rows: the number of rows to be added to the table
  //         data_: the data array
  index_list_update(page_num, num_rows, data_) {
    var p_list = "";
    // create each row of the table until length or num_rows
    if (data_.length < num_rows) {
      num_rows = data_.length;
    }

    for (let i = 0; i < data_.length ; i++) {
      // verify if is defined p_config_gui.gui_plugin_config[table['name']].index.columns_visible and show those columns in the row
      if (p_config_gui.gui_plugin_config[table['name']].index.columns_visible) {
        // for each table['columns'] create a new row of the table in the html element with id index_list
        p_list += (`<tr>`);
        for (let j = 0; j < this.p_config_gui.gui_plugin_config.table['name'].index.columns_visible.length; j++) {
          p_list += (`<td>${data_[i].column_visible[j]}</td>`);
        }
        p_list += (`</tr>`);
      }
      // else show all columns in the table.columns list
      else {
        // for each table['columns'] create a new row of the table in the html element with id index_list
        p_list += (`<tr>`);
        for (let j = 0; j < table.columns.length; j++) {
          p_list += (`<td>${data_[i].current_process.table.columns[j].name}</td>`);
        }
        p_list += (`</tr>`);
      }
    }
    document.getElementById("index_list")
      .innerHTML += p_list;
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

