// dashboard vue Module implementation

export default {
    data() {
        return { 
            process_list: [0,1,2,3],
            process: 0,
            status : 'Halted'
        }
    }, 
    methods: {
        // returns an axios instance for basic authentication
        axiosBasicAuth(username, password) {
          const buffer_auth = buffer.Buffer.from(username + ':' + password);
          const b64 = buffer_auth.toString('base64');
          return axios.create({
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Basic ${b64}`,
            }
          });
        },
        // returns the minimum mse with an active config_id (do not include stopped processes)
        // TODO: create a min mse training and validation functions for inactive config_id                                                                                                                                                                                                                                                                                                                                              

        min_training_mse(){
            const axios_instance = this.axiosBasicAuth("test", "pass");
            // use the response of api request
            axios_instance.get('/min_training_mse')
            .then((response) => {
              return response;
            }, (error) => {
              console.log(error);
              return 0;
            });        
        },
        // returns the fe_config.id for the minimum fe_training_error.mse for the current process
        min_validation_mse(){
          // use the response of api request
          axios.get('/min_validation_mse', {
            params :{
            }
          })
          .then((response) => {
            return response;
          }, (error) => {
            console.log(error);
            return 0;
          });
        },
        // returns the máximum value for a given table and column for the processes of the current user
        user_column_max(username, table, column) {
            // use the result of api request
            axios.get('/user_column_max', {
              //table: table,
              //column: column
              params : {
                table: 'fe_training_error',
                column: 'mse'
              }    
            })
            .then((response) => {
              return response;
              //console.log(response);
            }, (error) => {
              console.log(error);
              return 0;
            });
          
        },
        // returns the number of users for the processes of the user
        process_count_users() {
          // use the result of api request
          axios.get('/process_count_users', {
              table: table
            })
            .then((response) => {
              return response;
              //console.log(response);
            }, (error) => {
              console.log(error);
              return 0;
            });
        },
        // returns the number of processes of the current user
        process_count() {
          // use the result of api request
          axios.get('/process_count', {
              table: table
            })
            .then((response) => {
              return response;
              //console.log(response);
            }, (error) => {
              console.log(error);
              return 0;
            });
        },

        // returns the number of rows for a given table and column
        count_rows(table) {
            // use the result of api request
            axios.get('/count_rows', {
                table: table
              })
              .then((response) => {
                return response;
                //console.log(response);
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
