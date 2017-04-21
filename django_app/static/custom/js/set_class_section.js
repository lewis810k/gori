function set_class_section(){
  var url = 'https://mozzi.co.kr/api/talent/list/';

  // var url = 'http://localhost:8000/api/talent/list/';
  $.ajax({
    url: url,
    method: "GET",
    dataType: "json",
  })
  .done(function(data){
    console.log('done');
    console.log(data)
    length = data.results.length;
    results = data.results;
    // length만큼 반복
    for(i = 0; i < length; i++){
      // wrapper div를 새로 만든다.
      var newDom = $('<div class="col-md-4 col-sm-6 class-item"></div>');
      newDom.append('<a href="" class="item-container"></a>');
      var item_container = newDom.find('.item-container');

      //image, 좌측하단에 시간당 가격
      item_container.append('<div class="item-top"></div>');
      item_container.find('.item-top').append('<img class="item-image" src="" alt="" />');
      //image
      item_container.find('.item-image').attr("src", results[i].cover_image);
      //시간당 가격
      item_container.find('.item-top').append('<div class="item-price"></div>');
      var item_price = item_container.find('.item-price');

      item_price.append('<img class="item-price-img" src="" alt="" />');
      item_price.append('<div class="item-price-text"></div>');
      item_price.find('.item-price-text').text(results[i].price_per_hour);



      //제목, 튜터
      item_container.append('<div class="item-mid"></div>');
      var item_mid = item_container.find('.item-mid');
        //제목 추가
      item_mid.append('<div class="item-title-container"></div>');
      item_mid.find('.item-title-container').append('<div class="item-title"></div>');
      item_mid.find('.item-title').text(results[i].title);
        //튜터 정보 추가
      item_mid.append('<div class="item-tutor-container"></div>');
      item_mid.find('.item-tutor-container').append('<div class="item-tutor"></div>');
      item_mid.find('.item-tutor').text(results[i].tutor.name);
      item_mid.find('.item-tutor-container').append('<img class="item-tutor-pic" src="" alt="" />');
      item_mid.find('.item-tutor-pic').attr("src", results[i].tutor.profile_image);

      //수업형태, 평점, 지역
      item_container.append('<div class="item-bot"></div>');
      var item_bot = item_container.find('.item-bot');
      item_bot.append('<div class="col-md-3 col-sm-3 col-xs-3 item-bot-common item-group-type"></div>');
      item_bot.append('<div class="col-md-4 col-sm-4 col-xs-4 item-bot-common item-rate"></div>');
      //평점 이미지 작업
      item_bot.find('.item-rate').append('<div class="item-rate-img"></div>');
      var item_rate_img = item_bot.find('.item-rate-img');
      var average_rate = results[i].average_rate;
      // console.log(average_rate);
      //리뷰가 없을 경우 NEW 이미지로
      if (results[i].review_count == 0) {
        item_rate_img.append('<img class="new-img" src="" alt="" />');
      }
      else {
        //값을 반올림처리하여 별점 이미지 반영
        var rounded_rate = Math.round(average_rate);
        for (k = 1; k <= 5; k++){
          if (rounded_rate >= k) {
            item_rate_img.append('<img class="star-on-img" src="" alt="" />');
          }
          else {
            item_rate_img.append('<img class="star-off-img" src="" alt="" />');
          }
        }
        //평점
        item_bot.find('.item-rate-img').append('<div class="item-review-count"></div>');
        item_bot.find('.item-review-count').text("("+ results[i].review_count + ")");
      }

      item_bot.append('<div class="col-md-5 col-sm-5 col-xs-5 item-bot-common item-location"></div>');
      //수업형태
      item_bot.find('.item-group-type').text(results[i].type);

      //장소
      var regions = '';
      for (j = 0; j < results[i].regions.length; j++) {
        if (j == 2){
          regions += results[i].regions[j];
          break;
        }

        if (j == (results[i].regions.length) - 1) {
          regions += results[i].regions[j];
        }
        else {
          regions += results[i].regions[j] + ', ';
        }
      }
      item_bot.find('.item-location').text(regions);

      $('.class-row').append(newDom);
    }
  })
  .fail(function(data){
    console.log('fail');
  });
}
