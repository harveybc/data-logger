// process tables index view controller
export class IndexController {
  xy_points_ = [];
  data_ = [];
  p_config_gui = window.p_config_gui;
  p_conf_store = window.p_config_store;
  process = window.process;
  table = window.table;
  page_num = window.page_num;
  total_pages = window.total_pages;
  num_rows = window.num_rows;
  //Fetch data ever x milliseconds
  realtime = 'on'; //If == to on then fetch data every x seconds. else stop fetching
  updateInterval = 1000 * window.interval;

  constructor() {
    // get gymfx_process_list data from the server
    this.request_view_data().then((response) => {
      var res_list = [];
      for (let i = 0 ; i < response.data.length ; i++) {
        var obj = response.data[i]; 
        //console.log("obj = ", obj);
        res_list.push(obj);
      }
      this.index_list_update(res_list);
      this.scoreboard_update();
      // Draw interactive plot
      this.interactive_plot = this.interactive_plot_();
      // initialize realtime data fetching
      if (this.realtime === 'on') {
        try {
          this.rt_update();
        } catch (e) {
          console.log(e);
        }
      }
      /*
        * END INTERACTIVE CHART
      */
    })
    //REALTIME TOGGLE
    var that = this;
    $('#realtime .btn').click(function () {
      if ($(this).data('toggle') === 'on') {
        that.realtime = 'on'
        that.rt_update()
      } else {
        that.realtime = 'off'
      }
    });
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
  scoreboard_update() {
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
    return axios_instance.get(this.p_config_gui['gui_plugin_config'][table['name']]['index'].rt_plot.data_route)
  }
  
  // update the interactive plot
  rt_update() {
    // read values for the scoreboard and interactive plot
    this.scoreboard_update();
    var that = this;
    this.gymfx_online_plot_().then((response) => {
      //console.log("pre:" + JSON.stringify(response.data));
      that.xy_points_ = that.transform_plot_data(response.data);
      //console.log("update:" + JSON.stringify(this.xy_points_));
      try {
        //this.interactive_plot.setData(this.xy_points_);
        that.interactive_plot.setData([that.xy_points_]);
        //Since the axes don't change, we don't need to call plot.setupGrid()
        that.interactive_plot.draw();
      } catch (e) {
        console.log(e);
      }
      if (that.realtime === 'on')
        setTimeout(function () { this.rt_update(); }.bind(that), 1000);
    }, (error) => {
      console.log(error);
    });
  }

  interactive_plot_() {
    return $.plot('#interactive', [{ data: this.xy_points_ }], {
      grid: {
        borderColor: '#f3f3f3',
        borderWidth: 1,
        tickColor: '#f3f3f3'
      },
      axisLabels: {
        show: true
      },
      series: {
        shadowSize: 1, // Drawing is faster without shadows
        color: '#3c8dbc',
        lines: {
          line_width: 2,
          fill: true, // Converts the line chart to area chart
          show: true
        }
      },
      yaxes: [{
        axisLabel: 'Score: (Profit-Risk)/InitialCapital',
        min: this.plot_min,
        max: this.plot_max,
        show: true
      }],
      xaxes: [{
        axisLabel: 'Iteration Number',
        showTicks: true,
        gridLines: true,
        show: true
      }],
      selection: {
        mode: "x"
      }
    })
  }
  
  // This function transforms the response json [{"x":x0, "y":y0},...] to a 2D array [[x0,y0],...]required  by flot.js
  transform_plot_data(response_data) {
    let xy_points = [];
    let min = 0;
    let max = 1;
    let prev_min = this.plot_min;
    let prev_max = this.plot_max;
    let x_max = 0;

    for (let i = 0; i < response_data.length; i++) {
      if (response_data[i].y > max) {
        max = response_data[i].y;
      }
      if (response_data[i].y < min) {
        min = response_data[i].y;
      }
      if (response_data[i].x > x_max) {
        x_max = response_data[i].x;
      }
      xy_points.push([response_data[i].x, response_data[i].y]);
    }
    //if ((prev_min != min) || (prev_max != max)) {
    try {
      // console.log("update yaxis");
      this.interactive_plot.getAxes().yaxis.options.min = this.plot_min;
      this.interactive_plot.getAxes().yaxis.options.max = this.plot_max;
      this.interactive_plot.getAxes().xaxis.options.min = x_max - this.num_points;
      this.interactive_plot.getAxes().xaxis.options.max = x_max;
      this.interactive_plot.setupGrid();
      this.interactive_plot.draw();
    }
    catch (e) {
      console.log(e);
    }
    this.plot_max = max;
    this.plot_min = min;
    return xy_points;
  }

  // returns an axios instance with configured basic authentication
  // TODO: change to use current user
  axios_auth_instance() {
    let axios_instance = this.axiosBasicAuth("test", "pass");
    return axios_instance;
  }

}

