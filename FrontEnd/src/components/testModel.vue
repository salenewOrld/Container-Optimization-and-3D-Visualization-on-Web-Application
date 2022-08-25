<template>
  <div id="model"></div>
</template>

<script>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
export default {
  name: "testModel",
  data() {
    return {
      object: [],
      objectWall: [],
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      physics: null,
      clock: null,
      c: [0x4a31fb, 0x4be4db, 0xe859a],
      color: {
        S1: 0xf82525,
        S2: 0xf8be25,
        S3: 0xcef825,
        M1: 0x58f825,
        M2: 0x25f8ab,
        M3: 0x25cbf8,
        L1: 0x2558f8,
        L2: 0x6525f8,
        L3: 0xf525f8,
      },
      use: [0xff00ff, 0xffff00, 0x00ffff, 0xf0f0f0, 0xb5ee70],
      speed: 30,
      count: 0,
      box: [
        [
          //ชั้น 1
          ["S3"],
          ["M1", "M3"],
          ["S3"],
          ["S3"],
          ["M2"],
          ["M2"],
          ["S3"],
          ["S3"],
        ],
        [
          //ชั้น 2
          ["S3"],
          ["M1"],
          ["S3"],
          ["S3"],
          ["M1"],
          ["M1"],
          ["S3"],
          ["S3"],
        ],
      ],
      box3: [
        [
          //ชั้น 1
          ["M3"],
          ["M3"],
          ["S2", "S1", "S3"],
          ["M1", "M1", "S3"],
        ],
        [
          //ชั้น 2
        ],
      ],
      RESR: [
        [
          ["S3", "S1", "S3"],
          ["S1", "M2", "S2"],
          ["S1", "S2", "S2"],
          ["S1", "S1", "S1"],
          ["S1", "S3", "S1"],
          ["S3", "S1", "S1"],
          ["S1", "S1", "S2"],
          ["S1", "S1", "S3"],
          ["S2", "S1", "S2"],
          ["S1", "S1", "S1"],
        ],
        [
          ["S1", "S1", "S1"],
          ["S1", "M2", "S1"],
          ["S1", "S2", "S2"],
          ["S1", "S1", "S1"],
          ["S1", "S3", "S1"],
          ["S3", "S1", "S1"],
          ["S1", "S1", "S2"],
          ["S1", "S1", "S3"],
          ["S2", "S1", "S2"],
          ["S1", "S1", "S1"],
        ],
      ],
      box1: [
        [
          [1.1, 1.3, 1.4],
          [0.85, 0.95, 1.1],
          [1.1, 1.3, 1.4],
        ],
        [[1.85, 1.3, 2.1]],
        [
          [0.85, 0.95, 1.1],
          [0.92, 1.1, 1.3],
        ],
        [
          [0.85, 0.95, 1.1],
          [0.92, 1.1, 1.3],
          [0.92, 1.1, 1.3],
        ],
        [
          [0.85, 0.95, 1.1],
          [0.85, 0.95, 1.1],
          [0.85, 0.95, 1.1],
        ],
        [
          [0.85, 0.95, 1.1],
          [1.1, 1.3, 1.4],
          [0.85, 0.95, 1.1],
        ],
        [
          [1.1, 1.3, 1.4],
          [0.85, 0.95, 1.1],
          [0.85, 0.95, 1.1],
        ],
        [
          [0.85, 0.95, 1.1],
          [0.85, 0.95, 1.1],
          [0.92, 1.1, 1.3],
        ],
        [
          [0.85, 0.95, 1.1],
          [0.85, 0.95, 1.1],
          [1.1, 1.3, 1.4],
        ],
        [
          [0.92, 1.1, 1.3],
          [0.85, 0.95, 1.1],
          [0.92, 1.1, 1.3],
        ],
        [
          [0.85, 0.95, 1.1],
          [0.85, 0.95, 1.1],
          [0.85, 0.95, 1.1],
        ],
      ],
      size: {
        //กว้าง ยาว สูง ระยะห่าง
        S1: [0.85, 0.95, 0.95, 0.2],
        S2: [0.92, 0.95, 1.1, 0.2],
        S3: [1.1, 0.97, 1.3, 0.2],
        M1: [1.7, 1.05, 1.2, 0.4],
        M2: [1.85, 1.05, 1.3, 0.4],
        M3: [1.9, 1.05, 1.4, 0.4],
        L1: [2.1, 1.2, 2.2, 0.8],
        L2: [2.3, 1.3, 2.4, 0.8],
        L3: [2.8, 1.515, 2.4, 0.8],
      },
      t : [[['zero', 0], ['zero', 0]], [['m2', 20], ['m2', 20]], [['zero', 0], ['zero', 0]], [['zero', 0], ['zero', 0]], [['m1', 10], ['m1', 10]], [['zero', 0], ['zero', 0]], [['s3', 3], ['s3', 3]], [['zero', 0], ['zero', 0]], [['s3', 3], ['s3', 3]], [['s3', 3], ['s3', 3]], [['s3', 3], ['s3', 3]], [['zero', 0], ['zero', 0]], [['zero', 0], ['zero', 0]], [['zero', 0], ['zero', 0]], [['s3', 3], ['s3', 3]], [['m1', 10], ['m1', 10]], [['s3', 3], ['s3', 3]], [['s3', 3], ['s3', 3]], [['m1', 10], ['m1', 10]], [['zero', 0], ['zero', 0]], [['s3', 3], ['s3', 3]], [['zero', 0], ['zero', 0]], [['zero', 0], ['zero', 0]], [['m1', 10], ['m1', 10]], [['zero', 0], ['zero', 0]], [['m3', 30], ['m2', 20]], [['zero', 0], ['zero', 0]], [['zero', 0], ['zero', 0]], [['zero', 0], ['zero', 0]], [['zero', 0], ['zero', 0]], [['s3', 3], ['s3', 3]], [['zero', 0], ['zero', 0]], [['zero', 0], ['zero', 0]], [['s3', 3], ['s3', 3]], [['zero', 0], ['zero', 0]], [['m1', 10], ['m1', 10]], [['s3', 3], ['s3', 3]], [['zero', 0], ['zero', 0]], [['s3', 3], ['s3', 3]]],
      
      
    };
  },
  methods: {
    init() {
      console.log(this.t);
      this.clock = new THREE.Clock();
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0xf0f0f0);
      this.camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
      );
      this.camera.position.set(6, 3, 5);

      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
      document.getElementById("model").appendChild(this.renderer.domElement);

      // var wallGeometry = new THREE.BoxGeometry(20, 20, 1, 1, 1, 1);
      // var wallMaterial = new THREE.MeshBasicMaterial({ color: 0x8888ff });
      // //var wireMaterial = new THREE.MeshBasicMaterial( { color: 0x000000, wireframe:true } );
      // var wall = new THREE.Mesh(wallGeometry, wallMaterial);
      // wall.position.set(0, 0, 50);
      // this.scene.add(wall);
      // this.objectWall.push(wall);
      // console.log(this.box.length);

      // let x = 0.68;
      // for (let index = 0; index < 2; index++) {
      //   // แนวกว้าง
      //   let z = 2.45;
      //   let y = -1.45;
      //   for (let index = 0; index < 1; index++) {
      //     // แนวสูง
      //     for (let index = 0; index < 3; index++) {
      //       // แนวยาว
      //       const cube = new THREE.Mesh(
      //         new THREE.BoxGeometry(4, 4, 4),
      //         new THREE.MeshBasicMaterial({ color: this.use[index] })
      //       );
      //       cube.position.y = y;
      //       cube.position.x = x;
      //       cube.position.z = z;
      //       this.object.push(cube);
      //       this.objectWall.push(cube);
      //       this.scene.add(cube);
      //       // z = z - 1.012
      //       z -=
      //         Math.random() * 10 + Math.random() * 10 + Math.random() * 10 + 5;
      //     }
      //     y += 5;
      //     z = 2.45;
      //     this.changecolor();
      //   }
      //   x -= 5;
      // }
      console.log(this.box[0][0][0]);
      const planeBottom = new THREE.Mesh(
        new THREE.BoxGeometry(0.1, 5.895, 2.392),
        new THREE.MeshBasicMaterial({
          color: 0xb4b4b4,
          side: THREE.BackSide,
        })
      );
      planeBottom.position.y = 0;
      planeBottom.rotation.z = 1.571;
      this.scene.add(planeBottom);

      const cube = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["M2"][0],
          this.size["M2"][1],
          this.size["M2"][2]
        ),
        new THREE.MeshBasicMaterial({
          color: this.color["M2"],
          side: THREE.BackSide,
        })
      );
      cube.position.x = -2.24;
      cube.position.y = 0.4 + 0.2;
      cube.rotation.y = 1.571;
      this.object.push(cube);
      this.scene.add(cube);

      const cube2 = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["S3"][0],
          this.size["S3"][1],
          this.size["S3"][2]
        ),
        new THREE.MeshBasicMaterial({
          color: this.color["S3"],
          side: THREE.BackSide,
        })
      );
      cube2.position.z = -0.5;
      cube2.position.x = -0.94;
      cube2.position.y = 0.4 + 0.15;
      cube2.rotation.y = 1.571;
      this.object.push(cube2);
      this.scene.add(cube2);

      const cube3 = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["S3"][0],
          this.size["S3"][1],
          this.size["S3"][2]
        ),
        new THREE.MeshBasicMaterial({
          color: this.color["S3"],
          side: THREE.BackSide,
        })
      );
      cube3.position.z = 0.5;
      cube3.position.x = -0.94;
      cube3.position.y = 0.4 + 0.15;
      cube3.rotation.y = 1.571;
      this.object.push(cube3);
      this.scene.add(cube3);

      //       const cube = new THREE.Mesh(
      //         new THREE.BoxGeometry(
      //           this.size[this.box[indexI][indexY][indexN]][0],
      //           this.size[this.box[indexI][indexY][indexN]][1],
      //           this.size[this.box[indexI][indexY][indexN]][2]
      //         ),
      //         new THREE.MeshBasicMaterial({
      //           color: this.color[this.box[indexI][indexY][indexN]],
      //           side: THREE.BackSide,
      //         })
      //       );
      //       cube.position.y = y;
      //       cube.position.x = x;
      //       cube.position.z = z;
      //       this.object.push(cube);
      //       this.scene.add(cube);

      // let y = -1;
      // for (let indexI = 0; indexI < this.box.length; indexI++) {
      //   let z = +10;
      //   for (let indexY = 0; indexY < this.box[indexI].length; indexY++) {
      //     let x = +1;
      //     let maxZ = 0;
      //     let addZ = 0;
      //     let nextMaxz = 0;
      //     for (
      //       let indexN = 0;
      //       indexN < this.box[indexI][indexY].length;
      //       indexN++
      //     ) {
      //       const cube = new THREE.Mesh(
      //         new THREE.BoxGeometry(
      //           this.size[this.box[indexI][indexY][indexN]][0],
      //           this.size[this.box[indexI][indexY][indexN]][1],
      //           this.size[this.box[indexI][indexY][indexN]][2]
      //         ),
      //         new THREE.MeshBasicMaterial({
      //           color: this.color[this.box[indexI][indexY][indexN]],
      //           side: THREE.BackSide,
      //         })
      //       );
      //       cube.position.y = y;
      //       cube.position.x = x;
      //       cube.position.z = z;
      //       this.object.push(cube);
      //       this.scene.add(cube);
      //       x -= this.size[this.box[indexI][indexY][indexN]][0] + 0.5;
      //       if (this.size[this.box[indexI][indexY][indexN]][2] > maxZ) {
      //         maxZ = this.size[this.box[indexI][indexY][indexN]][2];
      //       }
      //     }
      //     if (this.box[indexI][indexY + 1] !== undefined) {
      //       //   console.log("not undefined");
      //       for (
      //         let indexX = 0;
      //         indexX < this.box[indexI][indexY + 1].length;
      //         indexX++
      //       ) {
      //         if (
      //           this.size[this.box[indexI][indexY + 1][indexX]][2] > nextMaxz
      //         ) {
      //           nextMaxz = this.size[this.box[indexI][indexY + 1][indexX]][2];
      //           addZ = this.size[this.box[indexI][indexY + 1][indexX]][3];
      //         }
      //       }
      //     }
      //     z -= maxZ + addZ;
      //     // z -= 2
      //   }
      //   y += 2;
      // }

      // console.log(OrbitControls)
      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.minDistance = 0;
      this.controls.maxDistance = Infinity;

      this.controls.enableZoom = true; // Set to false to disable zooming
      this.controls.zoomSpeed = 1.0;

      this.controls.enablePan = true; // Set to false to disable panning (ie vertical and horizontal translations)

      this.controls.enableDamping = true; // Set to false to disable damping (ie inertia)
      this.controls.dampingFactor = 0.25;
      this.controls.update();
      console.log("fin init");
      // console.log(this.object.length);
    },
    animate() {
      requestAnimationFrame(this.animate);
      this.render();
      this.update();
    },
    update() {
      // var delta = this.clock.getDelta(); // seconds.
      // var moveDistance = 10 * delta; // 200 pixels per second
      // if (this.object.length > 0) {
      //   for (let index = 0; index < this.object.length; index++) {
      //     this.object[index].position.x += moveDistance;
      //     this.collision(index);
      //   }
      // }

      this.controls.update();
    },
    render() {
      this.renderer.render(this.scene, this.camera);
    },
    changecolor() {
      console.log("change color");
      if (this.use == this.color) {
        this.use = this.color2;
      } else if (this.use == this.color2) {
        this.use = this.color3;
      } else {
        this.use = this.color;
      }
    },
    collision(index) {
      for (
        var vertexIndex = 0;
        vertexIndex <
        this.object[index].geometry.attributes.position.array.length;
        vertexIndex++
      ) {
        var localVertex = new THREE.Vector3()
          .fromBufferAttribute(
            this.object[index].geometry.attributes.position,
            vertexIndex
          )
          .clone();
        var globalVertex = localVertex.applyMatrix4(this.object[index].matrix);
        var directionVector = globalVertex.sub(this.object[index].position);

        var ray = new THREE.Raycaster(
          this.object[index].position,
          directionVector.clone().normalize()
        );
        var collisionResults = ray.intersectObjects(this.objectWall);
        if (
          collisionResults.length > 0.5 &&
          collisionResults[0].distance < directionVector.length()
        ) {
          // a collision occurred... do something...
          // console.log("Hit now");
          // //this.object
          // this.object[index].position.x -= 1;
          // this.object.splice(index, 1);
        }
      }
    },
    getXYZ(input) {
      if (input == "S1") {
        return 0.85, 0.95, 1.1;
      } else if (input == "S2") {
        return 0.92, 1.1, 1.3;
      } else if (input == "S3") {
        return 1.1, 1.3, 1.4;
      } else if (input == "M1") {
        return 1.7, 1.2, 1.9;
      } else if (input == "M2") {
        return 1.85, 1.3, 2.1;
      } else if (input == "M3") {
        return 1.9, 1.4, 2.2;
      } else if (input == "L1") {
        return 2.1, 2.1, 1.75;
      } else if (input == "L2") {
        return 2.3, 2.2, 1.85;
      } else if (input == "L3") {
        return 2.6, 2.2, 2.2;
      }
    },
    getColor(input) {
      if (input == "S1") {
        return 0xf82525;
      } else if (input == "S2") {
        return 0xf8be25;
      } else if (input == "S3") {
        return 0xcef825;
      } else if (input == "M1") {
        return 0x58f825;
      } else if (input == "M2") {
        return 0x25f8ab;
      } else if (input == "M3") {
        return 0x25cbf8;
      } else if (input == "L1") {
        return 0x2558f8;
      } else if (input == "L2") {
        return 0x6525f8;
      } else if (input == "L3") {
        return 0xf525f8;
      }
    },
  },
  mounted() {
    console.log("after");
    this.init();
    this.animate();
  },
};
</script>

<style scoped>
</style>