// dashboard vue Module implementation
export class Dashboard {
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
    // Interactive plot
    this.interactive_plot = $.plot('#interactive', [{ data: this.xy_points_ }], {
      grid: {
        borderColor: '#f3f3f3',
        borderWidth: 1,
        tickColor: '#f3f3f3'
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
      yaxis: {
        min: this.plot_min,
        max: this.plot_max,
        show: true
      },
      //xaxis: {
      //   mode: "time", 
      //  timeformat:"%y/%m/%d %H:%M:%S"        
      //  }
      xaxis: {
        show: true
      }
    })


    var that = this;
    //INITIALIZE REALTIME DATA FETCHING
    if (this.realtime === 'on') {
      try {
        this.update();
      } catch (e) {
        console.log(e);
      }

    }
    var that = this;
    //REALTIME TOGGLE
    $('#realtime .btn').click(function () {
      if ($(this).data('toggle') === 'on') {
        that.realtime = 'on'
        that.update()
      } else {
        that.realtime = 'off'
      }
    })
    /*
      * END INTERACTIVE CHART
      */

    /*-----------
    * LINE CHART
    * ----------*/

    //Flot Line plot for the balance, equity and order_status vs date for the gym_fx_validation table's best reward_v config_id registers

    var max_points = this.val_plot_num_points
    var use_latest = true
    var d = [[1196463600000, 0], [1196550000000, 0], [1196636400000, 0], [1196722800000, 77], [1196809200000, 3636], [1196895600000, 3575], [1196982000000, 2736], [1197068400000, 1086], [1197154800000, 676], [1197241200000, 1205], [1197327600000, 906], [1197414000000, 710], [1197500400000, 639], [1197586800000, 540], [1197673200000, 435], [1197759600000, 301], [1197846000000, 575], [1197932400000, 481], [1198018800000, 591], [1198105200000, 608], [1198191600000, 459], [1198278000000, 234], [1198364400000, 1352], [1198450800000, 686], [1198537200000, 279], [1198623600000, 449], [1198710000000, 468], [1198796400000, 392], [1198882800000, 282], [1198969200000, 208], [1199055600000, 229], [1199142000000, 177], [1199228400000, 374], [1199314800000, 436], [1199401200000, 404], [1199487600000, 253], [1199574000000, 218], [1199660400000, 476], [1199746800000, 462], [1199833200000, 448], [1199919600000, 442], [1200006000000, 403], [1200092400000, 204], [1200178800000, 194], [1200265200000, 327], [1200351600000, 374], [1200438000000, 507], [1200524400000, 546], [1200610800000, 482], [1200697200000, 283], [1200783600000, 221], [1200870000000, 483], [1200956400000, 523], [1201042800000, 528], [1201129200000, 483], [1201215600000, 452], [1201302000000, 270], [1201388400000, 222], [1201474800000, 439], [1201561200000, 559], [1201647600000, 521], [1201734000000, 477], [1201820400000, 442], [1201906800000, 252], [1201993200000, 236], [1202079600000, 525], [1202166000000, 477], [1202252400000, 386], [1202338800000, 409], [1202425200000, 408], [1202511600000, 237], [1202598000000, 193], [1202684400000, 357], [1202770800000, 414], [1202857200000, 393], [1202943600000, 353], [1203030000000, 364], [1203116400000, 215], [1203202800000, 214], [1203289200000, 356], [1203375600000, 399], [1203462000000, 334], [1203548400000, 348], [1203634800000, 243], [1203721200000, 126], [1203807600000, 157], [1203894000000, 288]];

    var options = {
      xaxis: {
        mode: "time",
        timeBase: "milliseconds",
        tickLength: 5,
        gridLines: false
      },
      selection: {
        mode: "x"
      },
      grid: {
        //markings: this.order_status_areas
      }
    };
    //console.log("befoplot 1:" + response.data);
    this.validation_plot = $.plot("#placeholder", [d], options);
    var plot = this.validation_plot;
    this.overview = $.plot("#overview", [d], {

      series: {
        lines: {
          show: true,
          lineWidth: 1
        },
        shadowSize: 0
      },
      xaxis: {
        ticks: [],
        mode: "time"
      },
      yaxis: {
        ticks: [],
        min: 0,
        autoScaleMargin: 0.1
      },
      selection: {
        mode: "x"
      }
    });
    var overview = this.overview;

    // get the data from the server
    this.gymfx_validation_plot_().then((response) => {
      var plot_data = JSON.parse(response.data);
      console.log("plot_data = " + plot_data);
      // prepare the data  
      that.data_ = that.transform_validation_plot_data(plot_data);
      console.log("that.data_.xy_equity = " + that.data_.xy_equity);
      // TODO: update validation_plot_data and options.grid.markings function
      try {
        // that.interactive_plot.setData(that.xy_points_);
        that.validation_plot.setData([that.data_.xy_equity]);
        that.overview.setData([that.data_.xy_equity]);
        that.validation_plot.getOptions().grid.markings = that.order_status_areas
        plot = that.validation_plot;
        overview = that.overview;
        // Since the axes don't change, we don't need to call plot.setupGrid()
        that.validation_plot.setupGrid();
        that.validation_plot.draw();
        that.overview.draw();
      } catch (e) {
        console.log(e);
      }


      // Add the Flot version string to the footer
      //$("#footer").prepend("Flot " + $.plot.version + " &ndash; ");
    })
    // now connect the two
    $("#placeholder").bind("plotselected", function (event, ranges) {
      console.log("plotselected");
      // do the zooming
      $.each(plot.getXAxes(), function (_, axis) {
        var opts = axis.options;
        opts.min = ranges.xaxis.from;
        opts.max = ranges.xaxis.to;
      });
      $("#placeholder").setupGrid();
      $("#placeholder").draw();
      $("#placeholder").clearSelection();
      // don't fire event on the overview to prevent eternal loop
      overview.setSelection(ranges, true);
    });

    $("#overview").bind("plotselected", function (event, ranges) {
      console.log("plotselected");
      $("#placeholder").setSelection(ranges);
    });

    /* END LINE CHART */
    //$("body").on("mouseover-highlight", this.onMouseover)    
    this.order_status_areas = this.order_status_areas.bind(this); 
    
  }

  // helper for returning the order status color areas for the validation plot
  order_status_areas(axes) {
    var markings = [];
    // for each this.data_.xy_order_status[i][1], create a region red if thre order status is -1 and green if 1
    var from = 0;
    var to = 0;
    var color = "#4f4f4f";

    for (var i = 1; i < this.data_.xy_order_status.length; ++i) {
      var x = this.data_.xy_order_status[i][0];
      // sell order when order_status == -1
      if (i > 0 && this.data_.xy_order_status[i][1] == -1 && this.data_.xy_order_status[i - 1][1] == 0) {
        from = x;
      }
      if (i > 0 && this.data_.xy_order_status[i][1] == 0 && this.data_.xy_order_status[i - 1][1] == -1) {
        to = x;
        color = "#ff4f4f";
        markings.push({ xaxis: { from: from, to: to }, color: color });
      }
      // buy order when order_status == 1
      if (i > 0 && this.data_.xy_order_status[i][1] == 1 && this.data_.xy_order_status[i - 1][1] == 0) {
        from = x;
      }
      if (i > 0 && this.data_.xy_order_status[i][1] == 0 && this.data_.xy_order_status[i - 1][1] == 1) {
        to = x;
        color = "#4f4fff";
        markings.push({ xaxis: { from: from, to: to }, color: color });
      }
    }
    return markings;
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
  // This function updates the interactive plot with new data and update the plot axises
  transform_validation_plot_data(response_data) {
    let timestamps = [];
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

