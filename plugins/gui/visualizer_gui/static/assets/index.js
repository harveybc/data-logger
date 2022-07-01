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
        // returns the fe_config.id for the minimum fe_training_error.mse for the current process
        max_training_mse(){},
        // returns the fe_config.id for the minimum fe_training_error.mse for the current process
        max_validation_mse(){},
        // returns the fe_config.id for the minimum fe_training_error.mse for the current process
        max_training_mse(){},



        // returns the máximum value for a given table and column for the processes of the current user
        user_column_max(username, table, column) {

            // use the result of api request
            axios.get('/column_max', {
                //table: table,
                //column: column
                params :{
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
        // returns the number of processes of the current user
        process_count() {
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
