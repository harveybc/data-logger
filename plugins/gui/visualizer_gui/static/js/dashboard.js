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
        console.log("before:" + response.data);
        this.xy_points_ = JSON.parse(response.data);
        console.log("after:" +  JSON.stringify(this.xy_points_)); 
      }, (error) => {
        console.log(error);
      });
          
    // Interactive plot
        this.interactive_plot = $.plot('#interactive',[ [] ], {
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
            
            this.updateInterval = 1000 * window.interval;

            //Fetch data ever x milliseconds
            this.realtime = 'on' //If == to on then fetch data every x seconds. else stop fetching
           
            var that = this;
            //INITIALIZE REALTIME DATA FETCHING
            if (this.realtime === 'on') {
              try {
                that.update();
              } catch (e) {  
                console.log(e);
              }

            }
            
            //REALTIME TOGGLE
            $('#realtime .btn').click(function () {
                if ($(that).data('toggle') === 'on') {
                  that.realtime = 'on'
                } else {
                  that.realtime = 'off'
                }
                that.update()
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
        //this.update = this.update();
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
          return axios_instance.get('/gymfx_online_plot_', {responseType: 'text',  transformResponse: []})
        },

      // This function transforms the response json [{"x":x0, "y":y0},...] to a 2D array [[x0,y0],...]required  by flot.js
      transform_plot_data(response_data) {  
        let xy_points = [];
        for (let i = 0; i < response_data.length; i++) {
          xy_points.push([response_data[i].x, response_data[i].y]);
        }
        return xy_points;
      },
      update() {
          this.gymfx_online_plot_().then((response) => {
            console.log("before:" + response.data);
              this.xy_points_ = this.transform_plot_data(JSON.parse(response.data));
              console.log("update:" + JSON.stringify(this.xy_points_)); 
            try {
              this.interactive_plot.setData(this.xy_points_);
              //Since the axes don't change, we don't need to call plot.setupGrid()
              this.interactive_plot.draw();
            } catch (e) {
              console.log(e);
            }  
            var that = this;
            if (this.realtime === 'on')
            setTimeout  (function () { that.update();}, 1000);
          }, (error) => {
            console.log(error);
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
