// common auth functions

// returns an axios instance for basic authentication
function axiosBasicAuth(username, password) {
  let buffer_auth = buffer.Buffer.from(username + ':' + password);
  let b64 = buffer_auth.toString('base64');
  return axios.create({
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${b64}`,
    }
  });
}

// returns an axios instance with configured basic authentication
// TODO: change to use current user
function axios_auth_instance(){
  let axios_instance = this.axiosBasicAuth("test", "pass");
  return axios_instance; 
}
// returns a list of lists containing the last num_points, x,y = [date, mse] points for the best online process
function online_mse_list(num_points){
  let axios_instance = this.axios_auth_instance();
    // use the response of api request
    axios_instance.get('/online_mse_list', { params: { max_points: num_points } })
    .then((response) => {
      console.log(response.data);
      return response.data;
    }, (error) => {
      console.log(error);
      return 0;
    });        
}