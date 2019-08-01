//index.js
const app = getApp();

Page({
  data: {
    str: 1,
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    }
    
  },
  changeSlider1(e) {
    this.setData({ str: e.detail.value })
  },

  jumpToRecommendation: function (options) {
    wx.navigateTo({
      url: '../recommendation/recommendation'
    })
  },
})
