import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.118.1/build/three.module.js';

import {
    FBXLoader
} from 'https://cdn.jsdelivr.net/npm/three@0.118.1/examples/jsm/loaders/FBXLoader.js';

import {
    SkeletonUtils 
} from 'https://cdn.jsdelivr.net/npm/three@0.118.1/examples/jsm/utils/SkeletonUtils.js';

/*
import {
    GLTFLoader
} from 'https://cdn.jsdelivr.net/npm/three@0.136.0/examples/jsm/loaders/GLTFLoader.js';

import {
    OBJLoader
} from 'https://cdn.jsdelivr.net/npm/three@0.136.0/examples/jsm/loaders/OBJLoader.js';
*/

import {
    OrbitControls
} from 'https://cdn.jsdelivr.net/npm/three@0.118.1/examples/jsm/controls/OrbitControls.js';

class DTwinBase {
    constructor(params) {
        this._Init(params);
    }

    _Init(params) {
        this._params = params;
        this._threejs = new THREE.WebGLRenderer({
            antialias: true,
        });
        this._threejs.shadowMap.enabled = true;
        this._threejs.shadowMap.type = THREE.PCFSoftShadowMap;
        this._threejs.setPixelRatio(window.devicePixelRatio);

        this.dtwin = document.getElementById('dtwin');
        this.height = parseInt(this.dtwin.offsetWidth * 9 / 16);

        this._threejs.setSize(this.dtwin.offsetWidth, this.height);

        this.dtwin.append(this._threejs.domElement);
        window.addEventListener('resize', () => {
            this._OnWindowResize();
        }, false);

        const fov = 60;
        const aspect = this.dtwin.offsetWidth / this.height;
        const near = 1.0;
        const far = 1000.0;
        this._camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
        this._camera.position.set(90, 50, 0);

        this._scene = new THREE.Scene();
        this._truckCount = 0;
        this._truck = []; // trucks
        this._packet = []; // packets
        this._worker = []; //  worker/agents
        this._workerPath = []; // worker path
        this._workerCount = 0; 
        this._mixers = []; // for worker animation mixer

        let light = new THREE.DirectionalLight(0x8F8F8F, 1.0);
        light.position.set(0, 200, 10);
        light.target.position.set(0, 0, 0);
        light.castShadow = true;
        light.shadow.bias = -0.001;
        light.shadow.mapSize.width = 2048;
        light.shadow.mapSize.height = 2048;
        light.shadow.camera.near = 0.1;
        light.shadow.camera.far = 500.0;
        light.shadow.camera.near = 0.5;
        light.shadow.camera.far = 500.0;
        light.shadow.camera.left = 100;
        light.shadow.camera.right = -100;
        light.shadow.camera.top = 100;
        light.shadow.camera.bottom = -100;
        this._scene.add(light);

        light = new THREE.AmbientLight(0xf0f0f0, 0.7);
        this._scene.add(light);

        const controls = new OrbitControls(
            this._camera, this._threejs.domElement);
        controls.target.set(0, 10, 0);
        controls.update();

        const loader = new THREE.CubeTextureLoader();
        const texture = loader.load([
            '/static/assets/img/dtwinfield/posx.jpg',
            '/static/assets/img/dtwinfield/negx.jpg',
            '/static/assets/img/dtwinfield/posy.jpg',
            '/static/assets/img/dtwinfield/negy.jpg',
            '/static/assets/img/dtwinfield/posz.jpg',
            '/static/assets/img/dtwinfield/negz.jpg',
        ]);
        this._scene.background = texture;
        const plane = new THREE.Mesh(
            new THREE.PlaneGeometry(300, 300, 10, 10),
            new THREE.MeshStandardMaterial({
                color: 0x606060,
            }));
        plane.castShadow = false;
        plane.receiveShadow = true;
        plane.rotation.x = -Math.PI / 2;
        this._scene.add(plane);

        //        this._Load3DModel();
        this._vx = 0.0;
        this._vy = 0.0;
        this._LoadGeoJson(ptokai_base, 0x008800, 1.0);
        this._LoadGeoJson(pt_area, 0x008800, 1.0);

        this._LoadGeoJson(ptokai_base, 0x00cc00, 10.0); //2nd floor
        this._LoadGeoJson(pt_area, 0x00cc00, 10.0);

        this._LoadGeoJson(ptokai_base, 0x00ff00, 19.0); //3rd floor
        this._LoadGeoJson(pt_area, 0x00ff00, 19.0);

        this._LoadGeoJsonWall(ptokai_piller, 0x00ccdd);
        this._LoadFBXWorker(); // load worker model




        this._LoadElevators(pt_elv, 0xcc3300);

        this._LoadFBXModels();

        this._LoadFBXModels2(); // load packet and agent.


        //        this._LoadWarehouseModel();
        this._LoadWarehouseModel();


        this._RAF();

    }

    _LoadGeoJson(js, color, ht) {
        const fs = js.features;
        for (var i = 0; i < fs.length; i++) {
            const gmcd = fs[i].geometry.coordinates[0][0];
            var vx = this._vx,
                vy = this._vy;
            if (vx == 0.0) {
                vx = vy = 0.0;
                for (var j = 1; j < gmcd.length; j++) { // 最後は含まない
                    vx += gmcd[j][0];
                    vy += gmcd[j][1];
                }
                vx /= gmcd.length - 1;
                vy /= gmcd.length - 1;
                this._vx = vx;
                this._vy = vy;
            }

            const scale = 1.0; // 0.75;
            const vz = ht;
            //            console.log("vx,vy", vx, vy, gmcd.length);
            //           console.log("center x,y", vx, vy);
            const points = [];
            var x = (gmcd[0][0] - vx) * scale;
            var y = (gmcd[0][1] - vy) * scale;
            var xn = x;
            var yn = y;
            points.push(new THREE.Vector3(-yn, vz, -xn));
            for (var j = 1; j < gmcd.length; j++) { // 最後は含まない
                x = (gmcd[j][0] - vx) * scale;
                y = (gmcd[j][1] - vy) * scale;
                //                console.log("x,y", x, y);
                points.push(new THREE.Vector3(-y, vz, -x));
                xn = y;
                yn = y;
            }
            const geom = new THREE.BufferGeometry().setFromPoints(points);

            const material = new THREE.LineBasicMaterial({
                color
            });
            material.transparent = true;
            material.opacity = 0.4;
            const mesh = new THREE.Line(geom, material);
            //            mesh.position.set(0, 30, 0);
            //            console.log("mesh",mesh.position);
            this._scene.add(mesh);
        }

    }
    toggleVisibleLayer() {
        if (this._WHmodel.visible) {
            this._WHmodel.visible = false;
        } else {
            this._WHmodel.visible = true;
        }
    }

    _LoadGeoJsonWall(js, color) {
        const fs = js.features;
        for (var i = 0; i < fs.length; i++) {
            const gmcd = fs[i].geometry.coordinates[0][0];
            var vx = this._vx,
                vy = this._vy;
            const scale = 1.0;; //0.75;
            const vz = 1.0;
            const vh = 7.0;
            const geom = new THREE.BufferGeometry();
            const x = [],
                y = [];
            for (var j = 0; j < gmcd.length - 1; j++) {
                x.push((gmcd[j][0] - vx) * scale);
                y.push((gmcd[j][1] - vy) * scale);
            }
            const vertxs = [
                // 0
                {
                    pos: [-y[0], vz, -x[0]]
                },
                {
                    pos: [-y[1], vz, -x[1]]
                },
                {
                    pos: [-y[1], vh, -x[1]]
                },

                {
                    pos: [-y[1], vh, -x[1]]
                },
                {
                    pos: [-y[0], vh, -x[0]]
                },
                {
                    pos: [-y[0], vz, -x[0]]
                },

                // 1
                {
                    pos: [-y[1], vz, -x[1]]
                },
                {
                    pos: [-y[2], vz, -x[2]]
                },
                {
                    pos: [-y[2], vh, -x[2]]
                },

                {
                    pos: [-y[2], vh, -x[2]]
                },
                {
                    pos: [-y[1], vh, -x[1]]
                },
                {
                    pos: [-y[1], vz, -x[1]]
                },

                // 2
                {
                    pos: [-y[2], vz, -x[2]]
                },
                {
                    pos: [-y[3], vz, -x[3]]
                },
                {
                    pos: [-y[3], vh, -x[3]]
                },

                {
                    pos: [-y[3], vh, -x[3]]
                },
                {
                    pos: [-y[2], vh, -x[2]]
                },
                {
                    pos: [-y[2], vz, -x[2]]
                },

                // 3
                {
                    pos: [-y[3], vz, -x[3]]
                },
                {
                    pos: [-y[0], vz, -x[0]]
                },
                {
                    pos: [-y[0], vh, -x[0]]
                },

                {
                    pos: [-y[0], vh, -x[0]]
                },
                {
                    pos: [-y[3], vh, -x[3]]
                },
                {
                    pos: [-y[3], vz, -x[3]]
                },

            ];
            const positions = [];
            const normals = [];
            const uvs = [];
            for (const vertex of vertxs) {
                positions.push(...vertex.pos);
                //                normals.push(...vertex.norm);
                //                uvs.push(...vertex.uv);
            }
            const positionNumComponents = 3;
            const normalNumComponents = 3;
            const uvNumComponents = 2;
            geom.setAttribute(
                'position',
                new THREE.BufferAttribute(new Float32Array(positions), positionNumComponents));
            //            geometry.setAttribute(
            //                'normal',
            //                new THREE.BufferAttribute(new Float32Array(normals), normalNumComponents));
            //           geometry.setAttribute(
            //                'uv',
            //                new THREE.BufferAttribute(new Float32Array(uvs), uvNumComponents));

            const material = new THREE.MeshPhongMaterial({
                color,
                side: THREE.DoubleSide,
            });
            material.transparent = true;
            material.opacity = 0.4;
            const mesh = new THREE.Mesh(geom, material);
            //            mesh.position.set(0, 30, 0);
            //            console.log("mesh",mesh.position);
            this._scene.add(mesh);
        }

    }

    _LoadElevators(js, color) {
        const fs = js.features;
        this._elv = [];

        for (var i = 0; i < fs.length; i++) {
            const gmcd = fs[i].geometry.coordinates[0][0];
            var vx = this._vx,
                vy = this._vy;
            const scale = 1.0;
            const vz = 1.0;
            const vh = 3.3;
            const geom = new THREE.BufferGeometry();
            const x = [],
                y = [];
            for (var j = 0; j < gmcd.length - 1; j++) {
                x.push((gmcd[j][0] - vx) * scale);
                y.push((gmcd[j][1] - vy) * scale);
            }
            const vertxs = [
                // 0
                {
                    pos: [-y[0], vz, -x[0]]
                },
                {
                    pos: [-y[1], vz, -x[1]]
                },
                {
                    pos: [-y[1], vh, -x[1]]
                },

                {
                    pos: [-y[1], vh, -x[1]]
                },
                {
                    pos: [-y[0], vh, -x[0]]
                },
                {
                    pos: [-y[0], vz, -x[0]]
                },

                // 1
                {
                    pos: [-y[1], vz, -x[1]]
                },
                {
                    pos: [-y[2], vz, -x[2]]
                },
                {
                    pos: [-y[2], vh, -x[2]]
                },

                {
                    pos: [-y[2], vh, -x[2]]
                },
                {
                    pos: [-y[1], vh, -x[1]]
                },
                {
                    pos: [-y[1], vz, -x[1]]
                },

                // 2
                {
                    pos: [-y[2], vz, -x[2]]
                },
                {
                    pos: [-y[3], vz, -x[3]]
                },
                {
                    pos: [-y[3], vh, -x[3]]
                },

                {
                    pos: [-y[3], vh, -x[3]]
                },
                {
                    pos: [-y[2], vh, -x[2]]
                },
                {
                    pos: [-y[2], vz, -x[2]]
                },

                // 3
                {
                    pos: [-y[3], vz, -x[3]]
                },
                {
                    pos: [-y[0], vz, -x[0]]
                },
                {
                    pos: [-y[0], vh, -x[0]]
                },

                {
                    pos: [-y[0], vh, -x[0]]
                },
                {
                    pos: [-y[3], vh, -x[3]]
                },
                {
                    pos: [-y[3], vz, -x[3]]
                },

            ];
            const positions = [];
            const normals = [];
            const uvs = [];
            for (const vertex of vertxs) {
                positions.push(...vertex.pos);
                //                normals.push(...vertex.norm);
                //                uvs.push(...vertex.uv);
            }
            const positionNumComponents = 3;
            const normalNumComponents = 3;
            const uvNumComponents = 2;
            geom.setAttribute(
                'position',
                new THREE.BufferAttribute(new Float32Array(positions), positionNumComponents));
            //            geometry.setAttribute(
            //                'normal',
            //                new THREE.BufferAttribute(new Float32Array(normals), normalNumComponents));
            //           geometry.setAttribute(
            //                'uv',
            //                new THREE.BufferAttribute(new Float32Array(uvs), uvNumComponents));

            const material = new THREE.MeshBasicMaterial({
                color,
                side: THREE.DoubleSide,
            });
            material.transparent = true;
            material.opacity = 0.4;
            const mesh = new THREE.Mesh(geom, material);
            //            mesh.position.set(0, 30, 0);
            //            console.log("mesh",mesh.position);
            this._elv[i] = mesh;
            this._scene.add(mesh);
        }

    }
    _AddRoad(i, p) {
        const points = [];
        points.push(new THREE.Vector3(p[0][1], 0, -p[0][0]));
        points.push(new THREE.Vector3(p[1][1], 0, -p[1][0]));
        const geom = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({
            color: 0x000000
        });
        const mesh = new THREE.Line(geom, material);
        this._scene.add(mesh);
    }

    _MoveElevator(i, h) {
        //        console.log("MoveElv",i,h);
        this._elv[i].position.set(0, h, 0);
    }


    // we need to reuse scene graph... umm.
    _MoveTruck(i, pos) {
        //        console.log("MoveElv",i,h);
        if (this._truck.length >= i + 1) {
            this._truck[i].visible = true; //always
            this._truck[i].position.set(pos[1], pos[2], -pos[0]);
            this._truck[i].rotation.set(-Math.PI * 0.5, 0, -pos[3] + Math.PI * .5);
        } else {
            const fbx = this._baseTrack.clone(true); // sceneGraph recursive clone            
            fbx.position.set(pos[1], pos[2], -pos[0]);
            fbx.rotation.set(-Math.PI * 0.5, 0, Math.PI / 180 * 6 + pos[3] + Math.PI * .5);
            this._truck.push(fbx);
            this._scene.add(this._truck[this._truckCount]);
            this._truckCount += 1;
            this._truck.push()
            console.log("Add Truck", i, pos)
        }
    }

    _HideTruck(i) {
        if (this._truck.length >= i + 1) {
            this._truck[i].visible = false;
        }
    }


    _MovePacket(i, pos) {
        //        console.log("MovePacket",i,pos);
        if (this._packet.length >= i + 1) {
            this._packet[i].visible = true; //always
            //                                   Y         Z        X 
            this._packet[i].position.set(pos[1] + 18.7, pos[2] + 20.5, -pos[0] + 36);
            this._packet[i].rotation.set(0, Math.PI * 0.5, -pos[3] - Math.PI / 180 * 6); //+Math.PI*.5);
        } else {
            const fbx = this._basePacket.clone(true); // sceneGraph recursive clone
//            console.log(fbx);
            fbx.position.set(pos[1], pos[2], -pos[0]);
            fbx.rotation.set(-Math.PI * 0.5, 0, Math.PI / 180 * 6 + pos[3] + Math.PI * .5);
            this._packet.push(fbx);
            this._scene.add(fbx);
            this._packetCount += 1;
            //            console.log("Add Packet", i,pos)
        }
    }

    _MoveWorker(i, pos) {
//        console.log("MoveWorker",i,pos);
        if (this._worker.length > i ) {
       //                                   Y         Z        X
            this._worker[i].position.set(pos[1] , pos[2] , pos[0] );
            this._worker[i].rotation.set(0,-Math.PI / 180 * 6 +  pos[3]+Math.PI/2, 0); //+Math.PI*.5);
        } else { // new worker
            // male or female
            var fbx;// =  SkeletonUtils.clone(this._workerModel); // sceneGraph recursive clone

            if (Math.random() < 0.5){
                fbx =  SkeletonUtils.clone(this._workerModel); // sceneGraph recursive clone
            }else{
                fbx =  SkeletonUtils.clone(this._femaleModel); // sceneGraph recursive clone
            }

//            const geom = new THREE.BoxGeometry(1,1,1);
//            const mat = new THREE.MeshBasicMaterial({color: 0x00ff00});
//            const fbx = new THREE.Mesh(geom, mat);
//            fbx.matrixAutoUpdate = false;
//            console.log(fbx);\
//            console.log("Set new worker",i,pos)

//            fbx.position.set(0, 20, 0);
            
            fbx.position.set(pos[1], pos[2], pos[0]);
//            fbx.rotation.set(-Math.PI * 0.5, 0, Math.PI / 180 * 6 + pos[3] + Math.PI * .5);
            fbx.rotation.set(0, Math.PI / 180 * 6 + pos[3], 0); //+Math.PI*.5);
            this._scene.add(fbx);
            this._workerCount += 1;
            this._worker.push(fbx);

            // for animation
            const mixer = new THREE.AnimationMixer(fbx);

            // walk or push
            var action;
            if (Math.random() < 0.8){
                const clip = this._walkAnimation.animations[0];
                action = mixer.clipAction(clip);
            }else{
                const clip = this._pushAnimation.animations[0];
                action = mixer.clipAction(clip);
            }
            this._mixers.push(mixer);
            const rtime = Math.random()*2.0; // within 2sec

            action.startAt(rtime).play();


            if (pos.length > 4) { // with route information.
                const points = [];
                for ( let i = 0; i< pos[4].length; i++){
                    points.push( new THREE.Vector3(pos[4][i][1], 20,pos[4][i][0]));
                }
                const gg = new THREE.BufferGeometry().setFromPoints(points);
                const line = new THREE.Line( gg, new THREE.LineBasicMaterial({color: 0xcc00aa}));
                this._scene.add(line);
                this._workerPath.push(line);
            }
        }
    }




    _LoadAnimatedModel() {
        const params = {
            camera: this._camera,
            scene: this._scene,
        }
        //       this._controls = new BasicCharacterController(params);
    }

    _LoadModel() {
        const loader = new GLTFLoader();
        loader.load('/static/assets/3dmodel/scene.gltf', (gltf) => {
            gltf.scene.traverse(c => {
                c.castShadow = true;
            });
            this._scene.add(gltf.scene);
        });
    }

    _LoadWarehouseModel() {
        const loader = new FBXLoader();
        var wall_material = new THREE.MeshBasicMaterial({
            color: 0xcccccc
        });
        wall_material.transparent = true;
        wall_material.opacity = 0.5;

        loader.setPath('/static/assets/3dmodel/ptokai/');
        loader.load('p_tokai.fbx', (fbx) => {
            fbx.scale.setScalar(0.01015);
            fbx.rotation.set(0, Math.PI - Math.PI / 180 * 5.7, 0);
            fbx.position.set(20.5, 18.9, 11.6);
            //            fbx.rotation.set(-Math.PI*0.5,0, -Math.PI/180*5.7);
            fbx.traverse(c => {
                c.castShadow = true;
                if (c.type == "Mesh") {
                    //                    console.log("Mesh",c);
                    c.material = wall_material;
                }
            });
            //            fbx.material.transparent = true;
            //            fbx.material.opacity = 0.4;

            this._WHmodel = fbx;
            this._scene.add(fbx);
        });
    }
    _LoadWarehouseModel0() {
        const loader = new OBJLoader();
        loader.setPath('/static/assets/3dmodel/ptokai/');
        var wall_material = new THREE.MeshBasicMaterial({
            color: 0xccddcc
        });
        wall_material.transparent = true;
        wall_material.opacity = 0.5;

        loader.load('p_tokai_simple_joined.obj', (fbx) => {
            //            fbx.scale.setScalar(0.010);
            fbx.rotation.set(0, Math.PI - Math.PI / 180 * 5.7, 0);
            fbx.position.set(20, 18.8, 11.5);
            //            fbx.rotation.set(-Math.PI*0.5,0, -Math.PI/180*5.7);
            fbx.traverse(c => {
                //                c.material.transparent = true;
                //                c.material.opacity = 0.4;
                if (c instanceof THREE.Mesh) {
                    c.material = wall_material;
                    console.log("Set material", c);
                } else if (c.type == "Mesh") {
                    console.log("Mesh");
                    c.material = wall_material;
                    c.material.tranparent = true;
                    c.material.opacity = 0.3;
                } else {
                    console.log("load", c.type, c.id);
                }
                c.castShadow = true;
                //                console.log('C',c,c.id);
            });
            //            fbx.material.transparent = true;
            //            fbx.material.opacity = 0.4;

            this._WHmodel = fbx;
            this._scene.add(fbx);
        });
    }




    _LoadFBXModels() {
        const loader = new FBXLoader();
        loader.setPath('/static/assets/3dmodel/90-light-commercial-truck-low-poly-model/');
        loader.load('lct3000.fbx', (fbx) => {
            fbx.scale.setScalar(0.025);
            fbx.position.set(29, 0, -0.5);
            fbx.rotation.set(-Math.PI * 0.5, 0, -Math.PI / 180 * 6);
            fbx.traverse(c => {
                c.castShadow = true;
            });
            this._baseTrack = fbx;
        });
    }
    _LoadFBXModels2() {
        console.log("Loading packet");
        const loader = new FBXLoader();
        loader.setPath('/static/assets/3dmodel/cardboard/');
        loader.load('cardboard.fbx', (fbx) => {
            fbx.scale.setScalar(0.006);
            //          fbx.rotation.set(0,0,0);//Math.PI*0.5);
            //           fbx.position.set(0,0, 0);
            fbx.traverse(c => {
                c.castShadow = true;
            });
            this._basePacket = fbx;

        });
    }

    _LoadFBXWorker() {
        console.log("Loading Worker");
        const loader = new FBXLoader();
        loader.setPath('/static/assets/3dmodel/human/');
        loader.load('human.fbx', (fbx) => {
            console.log("Scale", fbx.scale)
            fbx.scale.setScalar(0.009);
            fbx.position.set(0,19,0);
            fbx.rotation.set(0, Math.PI / 2,0);
            fbx.traverse(c => {
                c.castShadow = true;
                if (c.isMesh) {
                    c.scale.setScalar(0.01);
                    if (c.material) {
                        c.material.transparent = false
                    }
                }
            });
            this._workerModel = fbx;
        });
        // load walk animation

        loader.load('walk.fbx', (fbx) => {
            this._walkAnimation = fbx;
        });

        loader.load('female.fbx', (fbx) => {
            console.log("Scale", fbx.scale)
            fbx.scale.setScalar(0.009);
            fbx.position.set(0,19,0);
            fbx.rotation.set(0, Math.PI / 2,0);
            fbx.traverse(c => {
                c.castShadow = true;
                if (c.isMesh) {
                    c.scale.setScalar(0.01);
                    if (c.material) {
                        c.material.transparent = false
                    }
                }
            });
            this._femaleModel = fbx;
        });

        loader.load('run.fbx', (fbx) => {
            this._pushAnimation = fbx;
        });

    }


    _OnWindowResize() {
        this.height = parseInt(this.dtwin.offsetWidth * 9 / 16);
        this._camera.aspect = this.dtwin.offsetWidth / this.height;
        this._camera.updateProjectionMatrix();
        this._threejs.setSize(this.dtwin.offsetWidth, this.height);
    }


    _RAF() {
        requestAnimationFrame((t) => {
            if (this._previousRAF === null) {
                this._previousRAF = t;
            }

            this._RAF();

            this._threejs.render(this._scene, this._camera);
            this._Step(t - this._previousRAF);
            this._previousRAF = t;
        });
    }

    _Step(timeElapsed) {
        const timeElapsedS = timeElapsed * 0.001;
        if (this._mixers) {
            this._mixers.map(m => m.update(timeElapsedS));
        }

        //   if (this._controls) {
        //     this._controls.Update(timeElapsedS);
        //   }
    }

}


var _APP = null;

window.addEventListener('DOMContentLoaded', () => {
    console.log("Start! ThreeJS");
    _APP = new DTwinBase();
    //    console.log("App",_APP);
});

function GetApp() {
    //    console.log("GetApp",_APP)
    return _APP;
}

export default GetApp;