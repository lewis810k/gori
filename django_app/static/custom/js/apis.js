


// <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>

function obtainAuthToken(username, password){
  var url='https://mozzi.co.kr/api/member/token-auth/';
  $.ajax({
    url: url,
    method: 'POST',
    data: {
      username: username,
      password: password
    }
  })
  .done(function(data){
    console.log('done obtainAuthToken')
    var token = data.token;
    console.log('token is '+token)
    setCookie('Token',token);

  })
  .fail(function(data){
    console.log('no token. fail!')
  })
}


function getUserProfile() {
  var token = 'Token ' + getCookie('Token');
  $.ajax({
    url: 'https://mozzi.co.kr/api/member/profile/user/',
    type: 'GET',
    headers: {
      Authorization: token,
    }
  })
  .done(function(response) {
    console.log(response)
    var wishlist = response.nickname;
    console.log(wishlist)
  })
  .fail(function(response) {
    console.log(response);
  });
}
