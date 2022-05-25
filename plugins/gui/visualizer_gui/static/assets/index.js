// dashboard vue Module implementation

export default {
    data() {
        return { 
            process_list: [0,1,2,3],
            status : 'Halted'
        }
    }, 
    methods: {
        // returns the máximum value for a given table and column
        column_max(table, column) {
            // use the result of api request
            axios.post('/column_max', {
                table: table,
                column: column
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
            axios.post('/count_rows', {
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
