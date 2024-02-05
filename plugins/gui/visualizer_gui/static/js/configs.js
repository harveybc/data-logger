// dashboard vue Module implementation
export class Configs {
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
    that = this
    // get gymfx_process_list data from the server
    this.gymfx_configs_list_().then((response) => {
      var configs_list = JSON.parse(response.data);
      console.log("configs_list = " + configs_list);
      that.configs_list_update(0, 20, process_list);
    })

    /* END LINE CHART */

    //this.process_list_update();
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

  gymfx_configs_list_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    // use the result of api request
    return axios_instance.get('/gymfx_process_list_', { responseType: 'text', transformResponse: [] })
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

