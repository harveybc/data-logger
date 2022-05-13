// dashboard vue Module implementation
export default {
    data() {
        return { 
            count: 0
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
        }
    },
    compilerOptions: {
        // Initialize vue to have different delimiters to the ones used by jinja in flask: [[ , ]] 
        delimiters: ["[[", "]]"]
    }
}
