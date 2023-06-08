// RESTAURENT SPECIAL PRODUCT SLIDING EFFECT
const procontainer=[...document.querySelectorAll('.pro-container')];
const prebtn=[...document.querySelectorAll('.pre-btn')];
const nxtbtn=[...document.querySelectorAll('.nxt-btn')];
procontainer.forEach((item,i)=>{
  let containerdimension =item.getBoundingClientRect();
  let containerwidth=containerdimension.width;
  nxtbtn[i].addEventListener('click',()=>{
    item.scrollLeft += containerwidth;
  })
  prebtn[i].addEventListener('click',()=>{
    item.scrollLeft -=containerwidth;
  })
})
// RESTAURENT SPECIAL PRODUCT SLIDING EFFECT

//CART PAGE FUNCTIONS

//CART PAGE FUNCTIONS