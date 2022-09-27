// dashboard vue Module implementation

export default {
    data() {
        return { 
            process_list: [0,1,2,3],
            process: 0,
            status : 'Halted',
            _best_online: 1,
            _min_training_mse: 0.0,
            _best_config:1,
            _min_validation_mse: 0.0


        }
    }, 
    // initialize values
    created() {
        //this.get_process_list();
        //this.get_process();
        //this.get_status();
        this._best_online = this.best_online();
        this._min_training_mse = this.min_training_mse();
        this._best_config = this.best_config();
        this._min_validation_mse = this.min_validation_mse();
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

        // returns an axions instance with configured basic authentication
        // TODO: change to use current user
        axios_auth_instance(){
          let axios_instance = this.axiosBasicAuth("test", "pass");
          return axios_instance; 
        },
        // call request that returns the config id for the best mse from table fe_training_error that has config.active == true
        best_online() {
          // setup authentication
          let axios_instance = this.axios_auth_instance();
          // use the result of api request
          axios_instance.get('/best_online')
          .then((response) => {
            return response;
          }, (error) => {
            console.log(error);
            return 0;
          });
        },
        // call request that returns the best mse from table fe_training_error that has config.active == true
        min_training_mse(){
          let axios_instance = this.axios_auth_instance();
            // use the response of api request
            axios_instance.get('/min_training_mse')
            .then((response) => {
              return response;
            }, (error) => {
              console.log(error);
              return 0;
            });        
        },
        // call request that returns the config id for the best mse from table fe_validation_error that has config.active == false
        best_config() {
          // setup authentication
          let axios_instance = this.axios_auth_instance();
          // use the result of api request
          axios_instance.get('/best_config')
          .then((response) => {
            return response;
          }, (error) => {
            console.log(error);
            return 0;
          });
        },
        // call request that returns the best mse from table fe_validation_error that has config.active == false
        min_validation_mse(){
          let axios_instance = this.axios_auth_instance();
          // use the response of api request
          axios_instance.get('/min_validation_mse')
          .then((response) => {
            return response;
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
