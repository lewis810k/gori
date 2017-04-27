


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
  .done(function(data) {
    console.log('done obtainAuthToken')
    var token = data.token;
    console.log('token is '+token);
    setCookie('Token',token);

  })
  .fail(function(data){
    console.log('no token. fail!')
  })
}

// LOAD USER INFO
function createUserInfo(response){
  console.log("bname",response.name)
  $('#user-name').html(response.name);
  $('#nickname').html(response.nickname);
  $('#received_registrations').html(response.received_registrations);
  $('#sent_registrations').html(response.sent_registrations);
  $('#wish_list_count').html(response.wish_list);
  $('#user-prof-image').attr("src", response.profile_image);
  $('#user-cell').html(autoHypenPhone(response.cellphone));
  $('#user-email').html(response.user_id);

  if (response.user_type=="Django") {
    $('#user-type').html("이메일 로그인 사용중");
  }
  else {
    $('#user-type').html("페이스북 로그인 사용중");
  }
}

// LOAD WISHLIST INFO

function createWishList(response){
  var results = response.results
  $('#info-box').empty();
  for (i = 0; i < results.length; i++) {
    var result = results[i];
    var newDom  = $('<div class="wish-talent col-sm-12 container"></div>');
    newDom.append('<div class="cover-img col-sm-4 container"></div>')
    newDom.append('<div class="col-sm-8 wish-info-box row"></div>')
    var newDomCovImage = newDom.find('.cover-img');
    newDomCovImage.append('<img src="" alt="" class="cov-image">')
    newDomCovImage.find('img').attr('src',result.cover_image);
    var newDomInfo = newDom.find('div.wish-info-box');
    newDomInfo.append('<div class="regions"></div>')
    var regions = result.regions;
    newDomInfo.find('.regions').append('<img src="" alt="" class="loca-pin">')
    newDomInfo.find('img').attr('src','../../static/images/loca_pin.jpg');
    for (j=0; j < regions.length; j++){
      newDomInfo.find('.regions').text(regions[j])
    }
    newDomInfo.append('<div class="title"></div>')
    newDomInfo.find('.title').text(result.title)
    newDomInfo.append('<div class="type-review"></div>')
    newDomInfo.find('.type-review').text(result.type+' | '+result.average_rate+' '+'('+result.review_count+')')
    newDomInfo.append('<div class="price"></div>')
    newDomInfo.find('.price').text('￦ '+result.price_per_hour+'원')
    newDomInfo.append('<div class="regis-count"></div>')
    newDomInfo.find('.regis-count').text('참여인원 '+result.registration_count+'명')
    $('#info-box').append(newDom);
  }
}

function createRegisList(response){
  var results = response.results
  $('#info-box').empty();
  for (i = 0; i < results.length; i++) {
    var result = results[i].talent;
    var newDom  = $('<div class="wish-talent col-sm-12 container"></div>');
    newDom.append('<div class="cover-img col-sm-4 container"></div>')
    newDom.append('<div class="col-sm-8 wish-info-box row"></div>')
    var newDomCovImage = newDom.find('.cover-img');
    newDomCovImage.append('<img src="" alt="" class="cov-image">')
    newDomCovImage.find('img').attr('src',result.cover_image);
    var newDomInfo = newDom.find('div.wish-info-box');
    newDomInfo.append('<div class="regions"></div>')
    var regions = result.regions;
    newDomInfo.find('.regions').append('<img src="" alt="" class="loca-pin">')
    newDomInfo.find('img').attr('src','../../static/images/loca_pin.jpg');
    for (j=0; j < regions.length; j++){
      newDomInfo.find('.regions').text(regions[j])
    }
    newDomInfo.append('<div class="title"></div>')
    newDomInfo.find('.title').text(result.title)
    newDomInfo.append('<div class="type-review"></div>')
    newDomInfo.find('.type-review').text(result.type+' | '+result.average_rate+' '+'('+result.review_count+')')
    newDomInfo.append('<div class="price"></div>')
    newDomInfo.find('.price').text('￦ '+result.price_per_hour+'원')
    newDomInfo.append('<div class="regis-count"></div>')
    newDomInfo.find('.regis-count').text('참여인원 '+result.registration_count+'명')
    $('#info-box').append(newDom);
  }
}



// AJAX - get - USER PROFILE
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
    createUserInfo(response);
    var wishlist = response.nickname;
    console.log(wishlist)
  })
  .fail(function(response) {
    console.log(response);
  })
}




function getUserWishList(){
  var token = 'Token ' + getCookie('Token');
  $.ajax({
    url: 'https://mozzi.co.kr/api/member/wish-list/',
    type: 'GET',
    headers: {
      Authorization: token,
    }
  })
  .done(function(response) {
    console.log(response)
    createWishList(response);
    // var wishlist = response.nickname;
    // console.log(wishlist)
  })
  .fail(function(response) {
    console.log(response);
  });
}

function getUserEnrollList(){
  var token = 'Token ' + getCookie('Token');
  $.ajax({
    url: 'https://mozzi.co.kr/api/member/enrollment/',
    type: 'GET',
    headers: {
      Authorization: token,
    }
  })
  .done(function(response) {
    console.log(response)
    createRegisList(response);
  })
  .fail(function(response) {
    console.log(response);
  });
}
