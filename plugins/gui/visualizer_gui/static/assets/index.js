// dashboard vue Module implementation
export default {
    data() {
        return { 
            count: 0,
            process_list: [0,1,2,3],
            status : 'Halted'
        }
    }, 
    methods: {
        // returns the máximum value for a given table and column
        column_max(table, column) {
            return 0;
        },
        // returns the máximum value for a given table and column
        count(table) {
            return 0;
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
