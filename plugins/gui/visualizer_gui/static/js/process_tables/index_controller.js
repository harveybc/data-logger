// process tables index view controller
export class IndexController {
  p_config_gui = window.p_config_gui;
  p_conf_store = window.p_config_store;
  process = window.process;
  table = window.table;
  page_num = window.page_num;
  total_pages = window.total_pages;
  num_rows = window.num_rows;

  constructor() {
    // get gymfx_process_list data from the server
    var that = this;
    this.request_view_data().then((response) => {
      var res_list = [];
      for (let i = 0 ; i < response.data.length ; i++) {
        var obj = response.data[i]; 
        //console.log("obj = ", obj);
        res_list.push(obj);
      }

      that.index_list_update(res_list);
      //console.log("res_list:" + JSON.stringify(res_list));
    })
  }

  request_view_data() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    let num_rows=this.num_rows;
    // get the number of rows to be shown in the index view
    if (this.p_config_gui.gui_plugin_config[table['name']]) 
      if (this.p_config_gui.gui_plugin_config[table['name']].index)
        if (this.p_config_gui.gui_plugin_config[table['name']].index.num_rows){
          num_rows = this.p_config_gui.gui_plugin_config[table['name']].index.num_rows;
    }
    // use the result of api request
    return axios_instance.get('/' + this.process.name + '/' + this.table.name + '/index_list_data', { params: { "page_num": this.page_num,  "num_rows": num_rows } })
  }

  // updates the list of the table in the index view
  // params: start: the starting index of the data_ array
  //         num_rows: the number of rows to be added to the table
  //         data_: the data array
  index_list_update(data_) {
    var p_list = "";
    //set total_pages variable tothe number of pages having into account the total of registers as the length of the data_ array and the num_rows as the number of rows per page
    let last_element = data_.pop();
    this.total_pages = last_element.total_pages;
    window.total_pages = this.total_pages; 
    //uses data_length-1 due to the last element of the array is th total_pages variable returned by the server
    for (let i = 0; i < data_.length ; i++) {
      // verify if is defined p_config_gui.gui_plugin_config[table['name']].index.columns_visible and show those columns in the row
      if (((this.p_config_gui.gui_plugin_config[table['name']]) && (this.p_config_gui.gui_plugin_config[table['name']].index)) && (this.p_config_gui.gui_plugin_config[table['name']].index.columns_visible)){
            // for each table['columns'] create a new row of the table in the html element with id index_list
            p_list += (`<tr>`);
            for (let j=0; j < this.p_config_gui.gui_plugin_config[table['name']].index.columns_visible.length; j++ ) {
              let col = this.p_config_gui.gui_plugin_config[table['name']].index.columns_visible[j];
              p_list += (`<td>${data_[i][col]}</td>`);
            }
            p_list += (`</tr>`);
          }
      // else show all columns in the table.columns list
      else {
        // for each table['columns'] create a new row of the table in the html element with id index_list
        p_list += (`<tr>`);
        p_list += (`<td>${data_[i]['id']}</td>`);
        for (let j=0; j<table.columns.length; j++ ) {
          let col = table.columns[j].name;
          p_list += (`<td>${data_[i][col]}</td>`);
        }
        p_list += (`</tr>`);
      }
    }
    // update the index_list element with the new rows
    document.getElementById("index_list")
      .innerHTML += p_list;
    // update the pagination area with the new page_num
    document.getElementById("page_num").innerHTML = this.page_num;
    // update the pagination area with the new total_pages
    document.getElementById("total_pages").innerHTML = this.total_pages;
    // set the first_page_link to the first page
    document.getElementById("first_page_link").href = "/"+this.process.name+"/"+this.table.name+"/view_index?page_num=1";
    // set the previous_page_link to the previous page, verifying that it exists
    if (this.page_num > 1)
      document.getElementById("previous_page_link").href = "/" + this.process.name + "/" + this.table.name + "/view_index?page_num=" + (this.page_num - 1);
    else
      document.getElementById("previous_page_link").href = "/" + this.process.name + "/" + this.table.name + "/view_index?page_num=" + (this.page_num);
    // set the next_page_link to the next page, verifying that it exists
    if (page_num < this.total_pages)
      document.getElementById("next_page_link").href = "/" + this.process.name + "/" + this.table.name + "/view_index?page_num=" + (this.page_num+1);
    else
      document.getElementById("next_page_link").href = "/" + this.process.name + "/" + this.table.name + "/view_index?page_num=" + (this.page_num);
    // set the last_page_link to the last page
    document.getElementById("last_page_link").href = "/" + this.process.name + "/" + this.table.name +"/view_index?page_num="+(this.total_pages);
  }


  // read values from the server
  update_scoreboard() {
    var that = this;
    this.gymfx_best_online_().then((response) => {
      document.getElementById('box_0_value').innerHTML = that.gym_fx_best_online;
    }, (error) => {
      console.log(error);
    });
    this.gymfx_max_training_score_().then((response) => {
      document.getElementById('box_1_value').innerHTML = that.gym_fx_max_training_score;
    }, (error) => {
      console.log(error);
    });
    this.gymfx_best_offline_().then((response) => {
      document.getElementById('box_2_value').innerHTML = that.gym_fx_best_offline;
    }, (error) => {
      console.log(error);
    });
    this.gymfx_max_validation_score_().then((response) => {
      document.getElementById('box_3_value').innerHTML = that.gym_fx_max_validation_score;
    }, (error) => {
      console.log(error);
    });
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

  // call request that returns the config id for the best mse from table fe_training_error that has config.active == true
  gymfx_best_online_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    var that = this;
    // get the best config_id 
    return axios_instance.get(this.p_config_gui['gui_plugin_config'][table['name']]['index']['box_0_route'])
      .then((response) => {
        that.gym_fx_best_online = response.data;
      }, (error) => {
        that.gym_fx_best_online = error.message;
        console.log(error);
      });
  }



  // call request that returns the best mse from table fe_training_error that has config.active == true
  gymfx_max_training_score_() {
    let axios_instance = this.axios_auth_instance();
    var that = this;
    // use the response of api request
    return axios_instance.get(this.p_config_gui['gui_plugin_config'][table['name']]['index']['box_1_route'])
      .then((response) => {
        that.gym_fx_max_training_score = response.data;
        return response.data;
      }, (error) => {
        that.gym_fx_max_training_score = error.message;
        console.log(error);
      });
  }

  // call request that returns the config id for the best mse from table fe_validation_error that has config.active == false
  gymfx_best_offline_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    var that = this;
    // use the result of api request
    return axios_instance.get(this.p_config_gui['gui_plugin_config'][table['name']]['index']['box_2_route'])
      .then((response) => {
        that.gym_fx_best_offline = response.data;
        return response.data;
      }, (error) => {
        that.gym_fx_best_offline = error.message;
        console.log(error);
      });
  }

  // call request that returns the best mse from table fe_validation_error that has config.active == false
  gymfx_max_validation_score_() {
    let axios_instance = this.axios_auth_instance();
    var that = this;
    // use the response of api request
    return axios_instance.get(this.p_config_gui['gui_plugin_config'][table['name']]['index']['box_3_route'])
      .then((response) => {
        that.gym_fx_max_validation_score = response.data;
        return response.data;
      }, (error) => {
        that.gym_fx_max_validation_score = error.message;
        console.log(error);
      });
  }

  gymfx_online_plot_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    // use the result of api request
    return axios_instance.get(this.p_conf_gui.gui_plugin_config.dashboard.rt_plot.data_route)
  }

  // returns an axios instance with configured basic authentication
  // TODO: change to use current user
  axios_auth_instance() {
    let axios_instance = this.axiosBasicAuth("test", "pass");
    return axios_instance;
  }

}

