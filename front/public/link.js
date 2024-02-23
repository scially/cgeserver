function testPre(val) {
  if (val.indexOf('http://') > -1) {
    return val
  } else {
    return "http://" + val
  }
}
window.link = {
  playerWs: "8080", // ue拉流接口
  dataWs: "9091", // ue交互接口
  hostname: 'localhost',//ue连接地址
  openTime: 1000, // 延迟开启
}