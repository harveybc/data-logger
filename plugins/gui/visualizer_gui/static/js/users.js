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
    this.users_list_().then((response) => {
      this.data_ = JSON.parse(response.data); 
      this.users_list_update(0, this.data_);
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

  users_list_() {
    // setup authentication
    let axios_instance = this.axios_auth_instance();
    // use the result of api request
    axios_instance.get('/users_list_')
      .then((response) => {
        //console.log(response.data);
        that.gymfx_users = response.data;
        return response.data;
      }, (error) => {
        console.log(error);
        return 0;
      });
  }

  users_list_update(start, data_) {
    var users_list = "";s
    for (let i = start; i < data_.length; i++) {
      users_list += (`
      <tr>
        <!-- id, max, active -->
        <td>${data_[i].id}</td>
        <td>${data_[i].username}</td>
        <td>${data_[i].admin}</td>
        <td><a href="/users/edit/${data_[i].id}" class="btn btn-sm btn-info"><i class="nav-icon fas fa-pen-to-square"></i></a></td>
        <td><a href="/users/view/${data_[i].id}" class="btn btn-sm btn-info"><i class="nav-icon fas fa-eye"></i></a></td>
        <td><a href="/users/delete/${data_[i].id}" class="btn btn-sm btn-info"><i class="nav-icon fas fa-trash"></i></a></td>
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

