// dashboard vue Module implementation
export class Users {
  xy_points_ = [];
  points = [];
  process_list = [0, 1, 2, 3];
  process = 0;
  status = 'Halted';
  gymfx_best_online = 1;
  gymfx_max_training_score = 0.0;
  gymfx_best_offline = 1;
  gymfx_max_validation_score = 0.0;
  plot_min = 0.0;
  plot_max = 10000;
  v_plot_min = 0;
  v_plot_max = 10000;
  //Fetch data ever x milliseconds
  realtime = 'on'; //If == to on then fetch data every x seconds. else stop fetching
  updateInterval = 1000 * window.interval;
  data_ = [];
  totalPoints = 10;
  val_plot_num_points = window.val_plot_num_points

  constructor() {
        this.gymfx_online_plot_().then((response) => {
      console.log("before:" + response.data);
      this.xy_points_ = JSON.parse(response.data);
      console.log("after:" + JSON.stringify(this.xy_points_));
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

  // returns an axios instance with configured basic authentication
  // TODO: change to use current user
  axios_auth_instance() {
    let axios_instance = this.axiosBasicAuth("test", "pass");
    return axios_instance;
  }

  // call request that returns the config id for the best mse from table fe_training_error that has config.active == true
  gymfx_best_online_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    // use the result of api request
    axios_instance.get('/gymfx_best_online_')
      .then((response) => {
        //console.log(response.data);
        that.gymfx_best_online = response.data;
        return response.data;
      }, (error) => {
        console.log(error);
        return 0;
      });
  }

  // call request that returns the best mse from table fe_training_error that has config.active == true
  gymfx_max_training_score_() {
    let axios_instance = this.axios_auth_instance();
    // use the response of api request
    axios_instance.get('/gymfx_max_training_score_')
      .then((response) => {
        that.gymfx_max_training_score = response.data;
        return response.data;
      }, (error) => {
        console.log(error);
        return 0;
      });
  }

  // call request that returns the config id for the best mse from table fe_validation_error that has config.active == false
  gymfx_best_offline_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    // use the result of api request
    axios_instance.get('/gymfx_best_offline_')
      .then((response) => {
        this.gymfx_best_offline = response.data;
        return response.data;
      }, (error) => {
        console.log(error);
        return 0;
      });
  }

  // call request that returns the best mse from table fe_validation_error that has config.active == false
  gymfx_max_validation_score_() {
    let axios_instance = this.axios_auth_instance();
    // use the response of api request
    axios_instance.get('/gymfx_max_validation_score_')
      .then((response) => {
        that.gymfx_max_validation_score = response.data;
        return response.data;
      }, (error) => {
        console.log(error);
        return 0;
      });
  }

  gymfx_online_plot_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    // use the result of api request
    return axios_instance.get('/gymfx_online_plot_', { responseType: 'text', transformResponse: [] })
  }

  gymfx_validation_plot_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    // use the result of api request
    return axios_instance.get('/gymfx_validation_plot_', { responseType: 'text', transformResponse: [] })
  }

  gymfx_process_list_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    // use the result of api request
    return axios_instance.get('/gymfx_process_list_', { responseType: 'text', transformResponse: [] })
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
      console.log("update yaxis");
      this.interactive_plot.getAxes().yaxis.options.min = this.plot_min;
      this.interactive_plot.getAxes().yaxis.options.max = this.plot_max;
      this.interactive_plot.getAxes().xaxis.options.min = x_max - 10;
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
  
  // This function updates the validation table and interactive plot with new data and update the plot axises
  transform_validation_plot_data(response_data) {
    let timestamps = [];
    let op_type = [];
    let op_profit = [];

    let xy_balance = [];
    let xy_equity = [];
    let xy_order_status = [];
    let y_min = 0;
    let y_max = 1;
    // TODO: change when loading timestamps from csv
    let x_max = response_data.length;
    let x_min = 0;
    // calculate the js timestamps from the tick_date column
    for (let i = 0; i < response_data.length; i++) {
      // calculate minimum and maximum x values from response_data[i].tick_timestamp
      if (response_data[i].tick_timestamp > x_max) {
        x_max = response_data[i].tick_timestamp;
      }
      if (response_data[i].tick_timestamp < x_min) {
        x_min = response_data[i].tick_timestamp;
      }

      timestamps.push(response_data[i].tick_timestamp);
      op_type.push(response_data[i].op_type);
      op_profit.push(response_data[i].op_profit);
      xy_balance.push([response_data[i].tick_timestamp, response_data[i].balance]);
      xy_equity.push([response_data[i].tick_timestamp, response_data[i].equity]);
      // TODO: create a region colored plot for order status like : https://www.flotcharts.org/flot/examples/visitors/index.html
      xy_order_status.push([response_data[i].tick_timestamp, response_data[i].order_status]);
      if (response_data[i].balance > y_max) {
        y_max = response_data[i].balance;
      }
      if (response_data[i].balance < y_min) {
        y_min = response_data[i].balance;
      }
      if (response_data[i].equity > y_max) {
        y_max = response_data[i].equity;
      }
      if (response_data[i].equity < y_min) {
        y_min = response_data[i].equity;
      }
    }
    //if ((prev_min != min) || (prev_max != max)) {
    try {
      // set validation plot borders
      this.validation_plot.getAxes().yaxis.options.min = y_min;
      this.validation_plot.getAxes().yaxis.options.max = y_max;
      this.validation_plot.getAxes().xaxis.options.min = x_min;
      this.validation_plot.getAxes().xaxis.options.max = x_max;
      this.validation_plot.setupGrid();
      this.validation_plot.draw();
      // set validation plot overview borders
      this.overview.getAxes().yaxis.options.min = y_min;
      this.overview.getAxes().yaxis.options.max = y_max;
      this.overview.getAxes().xaxis.options.min = x_min;
      this.overview.getAxes().xaxis.options.max = x_max;
      this.overview.setupGrid();
      this.overview.draw();
    }
    catch (e) {
      console.log(e);
    }
    //this.plot_max = max;
    //this.plot_min = min;
    return {
      timestamps: timestamps,
      xy_balance: xy_balance,
      xy_equity: xy_equity,
      xy_order_status: xy_order_status
    };
  }


  // update the interactive plot
  update() {
    this.gymfx_online_plot_().then((response) => {
      this.xy_points_ = this.transform_plot_data(JSON.parse(response.data));
      console.log("update:" + JSON.stringify(this.xy_points_));
      try {
        //this.interactive_plot.setData(this.xy_points_);
        this.interactive_plot.setData([this.xy_points_]);
        //Since the axes don't change, we don't need to call plot.setupGrid()
        this.interactive_plot.draw();
      } catch (e) {
        console.log(e);
      }
      if (this.realtime === 'on')
        setTimeout(function () { this.update(); }.bind(this), 1000);
    }, (error) => {
      console.log(error);
    });
  }

  // updates the validation list table
  // params: start: the starting index of the data_ array
  //         num_rows: the number of rows to be added to the table
  //         data_: the data array
  val_list_update(start, num_rows, data_) {
    var prev_num_closes = 0;
    var close_list ="";
    var row_count = 0;
    for (let i = start; i < data_.length; i++) {
      if (data_[i].num_closes != prev_num_closes) {
        row_count++;
        if (row_count <= num_rows) {
          prev_num_closes = data_[i].num_closes;
          close_list += (`
            <tr>
              <!-- id, balance, reward, date -->
              <td>${data_[i].num_closes}</td>
              <td>${data_[i].balance}</td>
              <td>${data_[i].reward}</td>
              <td>${data_[i].tick_timestamp}</td>
            </tr>
            `);
        }
      }
    }
    document.getElementById("val_list")
      .innerHTML += close_list;
  }

  // updates the validation list table
  // params: start: the starting index of the data_ array
  //         num_rows: the number of rows to be added to the table
  //         data_: the data array
  process_list_update(start, num_rows, data_) {
    var prev_num_closes = 0;
    var process_list = "";
    var row_count = 0;
    for (let i = start; i < data_.length; i++) {
      var active_str = ""
      if (data_[i].active) {
        active_str = '<span class="badge badge-danger">Stopped</span>'
      }
      else{
        active_str = '<span class="badge badge-success">Active</span>'
      }

      process_list += (`
      <tr>
        <!-- id, max, active -->
        <td>${data_[i].id}</td>
        <td>${data_[i].max}</td>
        <td>${active_str}</td>
        
      </tr>
      `);
    }

    document.getElementById("process_list")
      .innerHTML += process_list;
  }



  // define starting field values
  field_start_values() {
    return {
      count: 0
    }
  }
  get_value(a, b, c) {
    return 0
  }
}

