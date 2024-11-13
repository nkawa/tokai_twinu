import GetApp from '/static/assets/js/dtwinfield.js';

//    const sio = io();
const sio = io('ws://' + document.domain + ':' + location.port, {
    transports: ['websocket']
});

function sendEvent(txt) {
    console.log("Emit", txt);
    sio.emit("MyEvent", txt);
}

sio.on('connect', () => {
    console.log("Connected!")
});

sio.on('disconnect', () => {
    console.log("Disconnected!")
});

// event contains info from Django/Daphne Websocket Server
sio.on('events', (data) => {
//    console.log("Events!", data);
    var app = GetApp();
    //        console.log("check",app);
    //        console.log("check",app._MoveElevator);
    for (var d of data) {
        if (d.type == 'elv'){
            var n = parseInt(d.id,10);
            app._MoveElevator(n, d.pos[2]);
        }else if (d.type =='truck'){
            var n = parseInt(d.id,10);
            app._MoveTruck(n, d.pos);
        }else if (d.type =='no-truck'){
            var n = parseInt(d.id,10);
            app._HideTruck(n);
        }else if (d.type =='road'){
            var n = parseInt(d.id,10);
            app._AddRoad(n, d.pos);
        }else if (d.type == 'packet'){
            var n = parseInt(d.id,10);
            app._MovePacket(n, d.pos);
        }else if (d.type == 'worker'){
            var n = parseInt(d.id,10);
            app._MoveWorker(n, d.pos);
        }
    }
});

document.getElementById('doit').addEventListener("click",
    () => {
        sendEvent("Doit");
    }
);

document.getElementById('stop').addEventListener("click",
    () => {
        sendEvent("stop");
    }
);

document.getElementById('addTruck').addEventListener("click",
    () => {
        sendEvent("addTruck");
    }
);

document.getElementById('showRoads').addEventListener("click",
    () => {
        sendEvent("showRoads");
    }
);
document.getElementById('layer').addEventListener("click",
    () => {
        GetApp().toggleVisibleLayer();
    }
);
