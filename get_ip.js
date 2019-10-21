var fs = require('fs-extra')
var appsData = fs.readJSONSync('./app.json')


var ip = '10.155.45.36'
var malcode = 'LSW'

var res_malcode = []
var res_ip = []

//Mapping ip to malcode
for(var app in appsData){
    var app1 = appsData[app]
    for(var apps in app1){
        var app2 = app1[apps]
        app2 = app2['IP']
        for(var i = 0; i <  app2.length; i++){
            if(ip == app2[i]){
                res_malcode.push(apps)
            }
        }
    }
}

//Mapping malcode to ip
for(var app in appsData){
    var app1 = appsData[app]
    if(app == 'DEV'){
        for(var apps in app1){
            if(apps == malcode){
                var app2 = app1[apps]
                app2 = app2['IP']
                res_ip = res_ip.concat(app2)
            }
        }
    }
}

console.log(res_malcode)
console.log(res_ip)
