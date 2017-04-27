
function addArticle(curPost) {
  var newDom = $('<article class="post"></article>')
  newDom.append('<header class="post-header"></header>')
  var newDomPostHeader = newDom.find('header.post-header');
  newDomPostHeader.append('<span class="header-username"></span>')
  newDom.find('span.header-username').text(curPost.author.username)
  // var day = moment(curPost.created_date);
  // var strDay = moment(day).format('YYYY년 M월 D일');
  newDomPostHeader.append('<span class="header-date"></span>')

  newDom.find('span.header-date').text(curPost.created_date);

  newDomPostHeader.append('<span class="post-delete clearfix"></span>')

  newDom.append('<form class="post-delete-form"></form>')
  newDom.append('<div class="post-image-container"></div>')
  newDom.find('.post-image-container').append('<div class="swiper-container"></div>')
  newDom.find('.swiper-container').append('<div class="swiper-wrapper"></div>')
  var newDomSwiperWrapper = newDom.find('.swiper-wrapper');
  for(var j =0; j< curPost.photo_list.length; j++){
    var curPhotos=curPost.photo_list[j];
    var newSwiperSlide=$('<div class="swiper-slide"></div>');
    newSwiperSlide.append('<img src="" alt=""/ class="post-image">')
    newSwiperSlide.find('img').attr('src',curPhotos.photo);
    newDomSwiperWrapper.append(newSwiperSlide)

  }

  newDom.append('<div class="post-bottom-container"</div>')
  $("div.post-list-container").append(newDom);

  newDom.find('.swiper-container').attr('id','post-swiper-'+curPost.pk);
  new Swiper('.swiper-container')
}
