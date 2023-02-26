// dashboard vue Module implementation

export default {
    data() {
        return { 
            xy_points_: [],
            points: [],
            process_list: [0,1,2,3],
            process: 0,
            status : 'Halted',
            gymfx_best_online: 1,
            gymfx_max_training_score: 0.0,
            gymfx_best_offline : 1,
            gymfx_max_validation_score : 0.0,
            plot_max : 10000,
            plot_min : 0.0,
            //Fetch data ever x milliseconds
            realtime : 'on', //If == to on then fetch data every x seconds. else stop fetching
            updateInterval : 1000 * window.interval,
            data_ :[],
            totalPoints : 10
           
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
      this.interactive_plot = $.plot('#interactive',[ { data : this.xy_points_ } ], {
        grid: {
            borderColor: '#f3f3f3',
            borderWidth: 1,
            tickColor: '#f3f3f3'
        },
        series: {
            shadowSize: 1, // Drawing is faster without shadows
            color: '#3c8dbc',
            lines: {
              line_width: 2,
              fill: true, // Converts the line chart to area chart
              show: true
            }
       },
        yaxis: {
            min : this.plot_min,
            max : this.plot_max,
            show: true
        },
        //xaxis: {
         //   mode: "time", 
          //  timeformat:"%y/%m/%d %H:%M:%S"        
      //  }
          xaxis: {
            show: true
        }
    })

      
            var that = this;
            //INITIALIZE REALTIME DATA FETCHING
            if (this.realtime === 'on') {
              try {
                this.update();
              } catch (e) {  
                console.log(e);
              }

            }
            var that = this;
            //REALTIME TOGGLE
            $('#realtime .btn').click(function () {
                if ($(this).data('toggle') === 'on') {
                  that.realtime = 'on'
                  that.update()
                } else {
                  that.realtime = 'off'
                }     
            })
        /*
          * END INTERACTIVE CHART
          */

        /*-----------
        * LINE CHART
        * ----------*/
      
        //Flot Line plot for the balance, equity and order_status vs date for the gym_fx_validation table's best reward_v config_id registers
       
        var max_points = "{{ p_config['gui_plugin_config']['dashboard']['val_plot']['max_points'] }}"
        var use_latest = true

        // setup the first and the last index of the arrays to be plotted
        var  first=0, last=max_points
        if (last>(v_original.length)) {
            last=v_original.length
        }

        // TODO: Posible error por mal cálculo del first
        if (use_latest){
          last = v_original.length
          first = last - max_points
          if (first<0) {
              first=0
          }
        }

        // prepare plotted arrays    
        for (var i = first; i < last; i++) {
          original.push([i, v_original[i]])
          predicted.push([i, v_predicted[i]])
        }

        var line_data1 = {
          data : original,
          color: '#3c8dbc'
        }

        var line_data2 = {
          data : predicted,
          color: '#00c0ef'
        }

        $.plot('#line-chart', [line_data1, line_data2], {
          grid  : {
            hoverable  : true,
            borderColor: '#f3f3f3',
            borderWidth: 1,
            tickColor  : '#f3f3f3'
          },
          series: {
            shadowSize: 0,
            lines     : {
              show: true
            },
            points    : {
              show: true
            }
          },
          lines : {
            fill : false,
            color: ['#3c8dbc', '#f56954']
          },
          yaxis : {
            show: true
          },
          xaxis : {
            show: true
          }
        })
        //Initialize tooltip on hover
        $('<div class="tooltip-inner" id="line-chart-tooltip"></div>').css({
          position: 'absolute',
          display : 'none',
          opacity : 0.8
        }).appendTo('body')
        $('#line-chart').bind('plothover', function (event, pos, item) {

          if (item) {
            var x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2)

            $('#line-chart-tooltip').html(item.series.label + ' of ' + x + ' = ' + y)
              .css({
                top : item.pageY + 5,
                left: item.pageX + 5
              })
              .fadeIn(200)
          } else {
            $('#line-chart-tooltip').hide()
          }

        })
        /* END LINE CHART */

    },
    // initialize values
    created() {
        //this.get_process_list();
        //this.get_process();
        //this.get_status();
        this.gymfx_best_online_();
        this.gymfx_max_training_score_();
        this.gymfx_best_offline_();
        this.gymfx_max_validation_score_();
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
            this.gymfx_best_online = response.data;
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
              this.gymfx_max_training_score = response.data;
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
            this.gymfx_best_offline = response.data;
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
            this.gymfx_max_validation_score = response.data;
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
        gymfx_validation_plot_() {
          // setup authentication
          let axios_instance = this.axios_auth_instance();
          // use the result of api request
          return axios_instance.get('/gymfx_validation_plot_', {responseType: 'text',  transformResponse: []})
        },

      // This function transforms the response json [{"x":x0, "y":y0},...] to a 2D array [[x0,y0],...]required  by flot.js
      transform_plot_data(response_data) {  
        let xy_points = [];
        let min=0;
        let max=1;
        let prev_min = this.plot_min;
        let prev_max = this.plot_max;
        let x_max = 0;

        for (let i = 0; i < response_data.length; i++) {
          if (response_data[i].y > max) {
            max = response_data[i].y;
          }
          if (response_data[i].y < min) {
            min = response_data[i].y;
          }
          if (response_data[i].x > x_max) {
            x_max = response_data[i].x;
          }
          xy_points.push([response_data[i].x, response_data[i].y]);
        }
        //if ((prev_min != min) || (prev_max != max)) {
          try{
            console.log("update yaxis");
            
          this.interactive_plot.getAxes().yaxis.options.min = this.plot_min;
          this.interactive_plot.getAxes().yaxis.options.max = this.plot_max;
          this.interactive_plot.getAxes().xaxis.options.min = x_max-10;
          this.interactive_plot.getAxes().xaxis.options.max = x_max;
          this.interactive_plot.setupGrid();
          this.interactive_plot.draw();
          
          }
          catch(e){
            console.log(e);
          }
        //}


        this.plot_max = max;
        this.plot_min = min;
        return xy_points;
      },
      update() {
          this.gymfx_online_plot_().then((response) => {
              this.xy_points_ = this.transform_plot_data(JSON.parse(response.data));
              console.log("update:" + JSON.stringify(this.xy_points_)); 
            try {
              //this.interactive_plot.setData(this.xy_points_);
              this.interactive_plot.setData([this.xy_points_]);
              //Since the axes don't change, we don't need to call plot.setupGrid()
              this.interactive_plot.draw();
            } catch (e) {
              console.log(e);
            }  
            if (this.realtime === 'on')
            setTimeout  (function () { this.update();}.bind(this), 1000);
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
