var arguments = process.argv.splice(2);
var codelen = arguments[0]
var code = arguments[1] // 0123组成的串

console.log(code);
console.log(codelen);


var code = new Array();
for (var i=0; i<codelen; i++){
    code[i] = parseInt(Math.random()*4);
}
console.log(code);

for (var i=0; i<20; i++)
console.log(parseInt(Math.random()*4));


var c = 0;

switch (c){
            case 0:
                break;
            case 1:
                break;
            case 2:
                break;
            case 3:
                break;
        }
    console.log('dsda');

