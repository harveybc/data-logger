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
        increment() {
            this.count++
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
