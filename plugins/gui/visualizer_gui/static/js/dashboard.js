// dashboard vue Module implementation

export default {
    data() {
        return { 
            xy_points_: [],
            process_list: [0,1,2,3],
            process: 0,
            status : 'Halted',
            best_online_: 1,
            min_training_mse_: 0.0,
            best_config_ : 1,
            min_validation_mse_ : 0.0


        }
    }, 
    // initialize values
    created() {
        //this.get_process_list();
        //this.get_process();
        //this.get_status();
        this.gymfx_best_online_ = this.gymfx_best_online_();
        this.gymfx_max_training_score_ = this.gymfx_max_training_score_();
        this.gymfx_best_config_ = this.gymfx_best_config_();
        this.gymfx_max_validation_score_ = this.gymfx_max_validation_score_();
    },  
    methods: {
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
        },
        // returns an axios instance with configured basic authentication
        // TODO: change to use current user
        axios_auth_instance(){
          let axios_instance = this.axiosBasicAuth("test", "pass");
          return axios_instance; 
        },
        // call request that returns the config id for the best mse from table fe_training_error that has config.active == true
        gymfx_best_online_() {
          // setup authentication
          let axios_instance = this.axios_auth_instance();
          // use the result of api request
          axios_instance.get('/gym_fx_best_online_')
          .then((response) => {
            //console.log(response.data);
            this.best_online_ = response.data;
            return response.data;
          }, (error) => {
            console.log(error);
            return 0;
          });
        },
        // call request that returns the best mse from table fe_training_error that has config.active == true
        gymfx_max_training_score_(){
          let axios_instance = this.axios_auth_instance();
            // use the response of api request
            axios_instance.get('/gymfx_max_training_score_')
            .then((response) => {
              this.min_training_mse_ = response.data;
              return response.data;
            }, (error) => {
              console.log(error);
              return 0;
            });        
        },
        // call request that returns the config id for the best mse from table fe_validation_error that has config.active == false
        gymfx_best_config_() {
          // setup authentication
          let axios_instance = this.axios_auth_instance();
          // use the result of api request
          axios_instance.get('/gymfx_best_config_')
          .then((response) => {
            this.best_config_ = response.data;
            return response.data;
          }, (error) => {
            console.log(error);
            return 0;
          });
        },
        // call request that returns the best mse from table fe_validation_error that has config.active == false
        gymfx_max_validation_score_(){
          let axios_instance = this.axios_auth_instance();
          // use the response of api request
          axios_instance.get('/gymfx_max_validation_score_')
          .then((response) => {
            this.min_validation_mse_ = response.data;
            return response.data;
          }, (error) => {
            console.log(error);
            return 0;
          });        
      },
        // define starting field values
        field_start_values(){
                return {
                count:0
            }
        },
        get_value(a,b,c){
            return 0
        }
    },
    delimiters: ["|{", "}|"]
}
