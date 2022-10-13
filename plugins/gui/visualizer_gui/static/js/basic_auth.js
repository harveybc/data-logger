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