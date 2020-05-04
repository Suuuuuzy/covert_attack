var fs = require('fs');
var robot = require("robotjs");
// set no delay after keypress
robot.setKeyboardDelay(0);
robot.setMouseDelay(2);
var path = require('path');

// endcoding:
// do nothing: 0
// small pic: 1
// big pic: 2
// video: 3

var no_x = 730;
var y = 140;
var small_pic_x = no_x+150;
var big_pic_x = small_pic_x+150;
var video_x = big_pic_x+150;

var arguments = process.argv.splice(2);
var refreshSpeed = arguments[0]
var codelen = arguments[1] // 指定生成长度
var code = new Array();
for (var i=0; i<codelen; i++){
    code[i] = parseInt(Math.random()*2);
    // code[i] = parseInt(Math.random()*3);
}
console.log(code);
//0123组成的串 长度为codelen 太长了，自动生成算了

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function Main(){
    var refresh = [];

    var mouse = robot.getMousePos();
    console.log('mouse position', mouse);

    // switch to left
    await robot.moveMouse(20, 700);
    await robot.mouseClick();
    await sleep(1000);
    // start recording
    // send signal to aq server! // 25, 550
    await robot.moveMouse(25, 550);
    await robot.mouseClick();
    await sleep(1000);
    // switch to right
    await robot.moveMouse(700, 700);
    await robot.mouseClick();
    await sleep(1000);
    
    for(var i=0; i<codelen; i++){
        switch (code[i]){
            case 0:
                await robot.moveMouse(no_x, y);
                break;
            case 1:
                await robot.moveMouse(small_pic_x, y);
                break;
            case 2:
                await robot.moveMouse(big_pic_x, y);
                break;
            case 3:
                await robot.moveMouse(video_x, y);
                break;
        }
        await robot.mouseClick();
        await refresh.push(Date.now());
        await sleep(refreshSpeed);
    }

    // switch to left
    await robot.moveMouse(20, 700);
    await robot.mouseClick();
    await sleep(1000);
    // stop recording
    // send signal to aq server! // 125, 550
    await robot.moveMouse(125, 550);
    await robot.mouseClick();
    await sleep(1000);

    // save refresh file
    path = 'data/' 
    if(!fs.existsSync(path))
      fs.mkdirSync(path) 
    fs.writeFile( path + '/' + refresh[0] + '_' + refreshSpeed + '.txt', refresh + '$' + refreshSpeed + '$' + codelen + '$' + code , (err) => {
      if (err) throw err;
      // console.log(LETTER.join('') + ' ' + i + ' ' + Date.now());
    });


}

Main();









