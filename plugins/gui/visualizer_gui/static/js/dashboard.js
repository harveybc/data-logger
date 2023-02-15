// dashboard vue Module implementation

export default {
    data() {
        return { 
            xy_points_: [],
            points: [],
            process_list: [0,1,2,3],
            process: 0,
            status : 'Halted',
            best_online_: 1,
            min_training_mse_: 0.0,
            best_config_ : 1,
            min_validation_mse_ : 0.0
        }
    }, 
    mounted() {
      this.gymfx_online_plot_().then((response) => {
        //console.log(response.data);
        this.xy_points_ = response.data;
        console.log("after:" + this.xy_points); 
      }, (error) => {
        console.log(error);
      });
       // returns the last points from the best_online process
       function getPerformanceData() {
        // get a list of lists containing the x,y = [date, mse] points for the best online process
        xy_points = [];
        window.vm.$refs.vue_component.gymfx_online_plot_().then((result) => {
          xy_points = window.vm.$refs.vue_component.xy_points;
        })
        console.log("after:" + xy_points); 
        return xy_points;
    }
      
    // Interactive plot
            var interactive_plot = $.plot('#interactive',[ [] ], {
                grid: {
                    borderColor: '#f3f3f3',
                    borderWidth: 1,
                    tickColor: '#f3f3f3'
                },
                series: {
                    shadowSize: 0, // Drawing is faster without shadows
                    color: '#3c8dbc'
                },
                lines: {
                    fill: true, // Converts the line chart to area chart
                    color: '#3c8dbc'
                },
                yaxis: {
                    min : 0.0,
                    max : 0.5,
                    show: true
                },
                xaxis: {
                    mode: "time", 
                    timeformat:"%y/%m/%d %H:%M:%S"        
                }
                //  xaxis: {
                //    show: true
                //}
            })
            
            var updateInterval = 1000 * window.interval;
            //Fetch data ever x milliseconds
            var realtime = 'on' //If == to on then fetch data every x seconds. else stop fetching
            function update() {
                xy_points=getPerformanceData();
                // xy_points=getRandomData();
                //total_points = xy_points.length;
                //var tmp = getRandomData();
                // app.best_online();
                interactive_plot.setData(xy_points);
                //document.getElementById("testFrame").innerHTML = xy_points.toString();
                // Since the axes don't change, we don't need to call plot.setupGrid()
                //document.getElementById("otherTestFrame").innerHTML = tmp.toString();
                interactive_plot.draw();
                if (realtime === 'on')
                    setTimeout(update, updateInterval);
            }
            //INITIALIZE REALTIME DATA FETCHING
            if (realtime === 'on') {
                update()
            }
            //REALTIME TOGGLE
            $('#realtime .btn').click(function () {
                if ($(this).data('toggle') === 'on') {
                    realtime = 'on'
                } else {
                    realtime = 'off'
                }
                update()
            })
            /*
             * END INTERACTIVE CHART
             */

    },
    // initialize values
    created() {
        //this.get_process_list();
        //this.get_process();
        //this.get_status();
        this.gymfx_best_online_ = this.gymfx_best_online_();
        this.gymfx_max_training_score_ = this.gymfx_max_training_score_();
        this.gymfx_best_offline_ = this.gymfx_best_offline_();
        this.gymfx_max_validation_score_ = this.gymfx_max_validation_score_();
        //this.gymfx_online_plot_ = this.gymfx_online_plot_();
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
          axios_instance.get('/gymfx_best_online_')
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
        gymfx_best_offline_() {
          // setup authentication
          let axios_instance = this.axios_auth_instance();
          // use the result of api request
          axios_instance.get('/gymfx_best_offline_')
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
        gymfx_online_plot_() {
          // setup authentication
          let axios_instance = this.axios_auth_instance();
          // use the result of api request
          return axios_instance.get('/gymfx_online_plot_');
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
