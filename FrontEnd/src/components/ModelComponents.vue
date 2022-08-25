<template>
  <div id="model" ref="model" justify="center" align="center"></div>
</template>

<script>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
export default {
  name: "ModelComponents",
  props: {
    element: String,
    width: Number,
    height: Number,
  },
  data() {
    return {
      object: [],
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      color2: [0xb5ee70, 0xff00ff, 0xffff00, 0x00ffff, 0xf0f0f0],
      color3: [0xffff00, 0xf0f0f0, 0xff00ff, 0xb5ee70, 0x00ffff],
      use: [0xff00ff, 0xffff00, 0x00ffff, 0xf0f0f0, 0xb5ee70],
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
        // กว้าง * ยาว * สูง
        // Width * Length * Height
        MP: [1.1, 1.8, 1.09],
        LHP: [1.515, 2.22, 0.85],
        LP: [1.515, 2.22, 0.73],
        HSSP: [0.76, 1.12, 1.09],
        ETC: [1.1, 1.5, 1.55],
        MLP: [1.1, 1.8, 0.73],
        SSP: [0.76, 1.12, 0.54],
        SMP: [0.76, 1.12, 0.73],

        Small: [0.1, 2.37, 5.9],
        Large: [0.1, 2.37, 12],
        Standard20: [0.1, 2.35, 5.895],
        Standard40: [0.1, 2.35, 12.029],
        HighCube40: [0.1, 2.35, 12.024],
      },
      input: {
        type: "Large",
        Area: [
          [204, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
          [0, 0, 0],
        ],
      },
    };
  },
  methods: {
    init() {
      console.log("init");
      console.log(this.$refs.model);
      this.scene = new THREE.Scene();
      // console.log('width = ',window.innerWidth)
      // console.log('height = ',window.innerHeight)
      this.camera = new THREE.PerspectiveCamera(
        75,
        this.width / this.height,
        0.1,
        1000
      );

      this.camera.position.set(6, 3, 5);
      // camera.position.set(6, 3, 5);

      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(this.width, this.height);
      //   console.log(this.renderer.domElement);
      // document.body.appendChild(this.renderer.domElement);
      // console.log(document.body)
      // // console.log(document.getElementById("model"));
      // // console.log(document.domElement)
      document
        .getElementById(this.element)
        .appendChild(this.renderer.domElement);
      // console.log(this.renderer.domElement)
      // //   console.log(document.getElementById("app"));
      // // this.$refs.model.appendChild(this.renderer.domElement)
      // var crateTexture = new THREE.ImageUtils.loadTexture(
      //   require("@/assets/crate.png")
      // );

      // let x = 0.68;
      // for (let index = 0; index < 2; index++) {
      //   // แนวกว้าง
      //   let z = 2.45;
      //   let y = -1.45;
      //   for (let index = 0; index < 2; index++) {
      //     // แนวสูง
      //     for (let index = 0; index < 5; index++) {
      //       // แนวยาว
      //       const cube = new THREE.Mesh(
      //         new THREE.BoxGeometry(1.012, 1.012, 1.012),
      //         new THREE.MeshBasicMaterial({ map: crateTexture })
      //       );
      //       cube.position.y = y;
      //       cube.position.x = x;
      //       cube.position.z = z;
      //       this.object.push(cube);
      //       this.scene.add(cube);
      //       // z = z - 1.012
      //       z -= 1.012;
      //     }
      //     y += 1.012;
      //     z = 2.45;
      //     this.changecolor();
      //   }
      //   x -= 1.012;
      // }
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
      //         new THREE.MeshBasicMaterial({ map: crateTexture })
      //         // new THREE.MeshBasicMaterial({
      //         //   color: this.color[this.box[indexI][indexY][indexN]],
      //         //   side: THREE.BackSide,
      //         // })
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

      //create....(x,y,z)
      // this.create101(-1.18500 + 0.38,-1.4,5.7/2-0.38);
      // this.create101(0,-1.4,5.7/2-0.38);
      // this.create101(+1.18500 - 0.38,-1.4,5.7/2-0.38);
      let AreaLenght;
      let AreaWidth;
      let rangbox;
      if (this.input.type == "Small") {
        [AreaWidth, AreaLenght] = this.createSmall();
      } else if (this.input.type == "Large") {
        [AreaWidth, AreaLenght] = this.createLarge();
      }
      console.log(AreaWidth);
      for (let indexI = 0; indexI < this.input.Area.length; indexI++) {
        for (
          let indexX = 0;
          indexX < this.input.Area[indexI].length;
          indexX++
        ) {
          if (indexX == 0) {
            if (this.input.Area[indexI][indexX] == 101) {
              rangbox = this.create101(
                AreaWidth - this.size["HSSP"][0] / 2,
                -1.4,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 102) {
              rangbox = this.create102(
                AreaWidth - this.size["SMP"][0] / 2,
                -1.6,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 103) {
              rangbox = this.create103(
                AreaWidth - this.size["SSP"][0] / 2,
                -1.7,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 104) {
              rangbox = this.create104();
            } else if (this.input.Area[indexI][indexX] == 105) {
              rangbox = this.create105();
            } else if (this.input.Area[indexI][indexX] == 106) {
              rangbox = this.create106(
                AreaWidth - this.size["LP"][0] / 2,
                -1.6,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 201) {
              rangbox = this.create201(
                AreaWidth - this.size["SSP"][0] / 2,
                -1.7,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 202) {
              rangbox = this.create202();
            } else if (this.input.Area[indexI][indexX] == 203) {
              rangbox = this.create203();
            } else if (this.input.Area[indexI][indexX] == 204) {
              rangbox = this.create204();
            } else if (this.input.Area[indexI][indexX] == 205) {
              rangbox = this.create205();
            } else if (this.input.Area[indexI][indexX] == 206) {
              rangbox = this.create206(
                AreaWidth - this.size["SMP"][0] / 2,
                -1.6,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 207) {
              rangbox = this.create207();
            } else if (this.input.Area[indexI][indexX] == 208) {
              rangbox = this.create208();
            }
          } else if (indexX == 1) {
            if (this.input.Area[indexI][indexX] == 101) {
              rangbox = this.create101(0, -1.4, AreaLenght);
            } else if (this.input.Area[indexI][indexX] == 102) {
              rangbox = this.create102(0, -1.6, AreaLenght);
            } else if (this.input.Area[indexI][indexX] == 103) {
              rangbox = this.create103(0, -1.7, AreaLenght);
            } else if (this.input.Area[indexI][indexX] == 104) {
              rangbox = this.create104();
            } else if (this.input.Area[indexI][indexX] == 105) {
              rangbox = this.create105();
            } else if (this.input.Area[indexI][indexX] == 106) {
              rangbox = this.create106(0, -1.6, AreaLenght);
            } else if (this.input.Area[indexI][indexX] == 201) {
              rangbox = this.create201(0, -1.7, AreaLenght);
            } else if (this.input.Area[indexI][indexX] == 202) {
              rangbox = this.create202();
            } else if (this.input.Area[indexI][indexX] == 203) {
              rangbox = this.create203();
            } else if (this.input.Area[indexI][indexX] == 204) {
              rangbox = this.create204();
            } else if (this.input.Area[indexI][indexX] == 205) {
              rangbox = this.create205();
            } else if (this.input.Area[indexI][indexX] == 206) {
              rangbox = this.create206(0, -1.7, AreaLenght);
            } else if (this.input.Area[indexI][indexX] == 207) {
              rangbox = this.create207();
            } else if (this.input.Area[indexI][indexX] == 208) {
              rangbox = this.create208();
            }
          } else if (indexX == 2) {
            if (this.input.Area[indexI][indexX] == 101) {
              rangbox = this.create101(
                -AreaWidth + this.size["HSSP"][0] / 2,
                -1.4,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 102) {
              rangbox = this.create102(
                -AreaWidth + this.size["SMP"][0] / 2,
                -1.6,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 103) {
              rangbox = this.create103(
                -AreaWidth + this.size["SSP"][0] / 2,
                -1.7,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 104) {
              rangbox = this.create104();
            } else if (this.input.Area[indexI][indexX] == 105) {
              rangbox = this.create105();
            } else if (this.input.Area[indexI][indexX] == 106) {
              rangbox = this.create106(
                AreaWidth + this.size["LP"][0] / 2,
                -1.6,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 201) {
              rangbox = this.create201(
                -AreaWidth + this.size["SSP"][0] / 2,
                -1.7,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 202) {
              rangbox = this.create202();
            } else if (this.input.Area[indexI][indexX] == 203) {
              rangbox = this.create203();
            } else if (this.input.Area[indexI][indexX] == 204) {
              rangbox = this.create204();
            } else if (this.input.Area[indexI][indexX] == 205) {
              rangbox = this.create205();
            } else if (this.input.Area[indexI][indexX] == 206) {
              rangbox = this.create206(
                -AreaWidth + this.size["SMP"][0] / 2,
                -1.6,
                AreaLenght
              );
            } else if (this.input.Area[indexI][indexX] == 207) {
              rangbox = this.create207();
            } else if (this.input.Area[indexI][indexX] == 208) {
              rangbox = this.create208();
            }
          }
        }
        AreaLenght -= rangbox * 1.5;
      }

      // var light1 = new THREE.DirectionalLight(0xffffff);
      // light1.position.set(0, 1, 1).normalize();
      // this.scene.add(light1);
      // var light2 = new THREE.DirectionalLight(0xffffff);
      // light2.position.set(2, 1, -1).normalize();
      // this.scene.add(light2);
      // var light3 = new THREE.DirectionalLight(0xffffff);
      // light3.position.set(-2, 1, -1).normalize();
      // this.scene.add(light3);
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
    },
    animate() {
      requestAnimationFrame(this.animate);
      // for (let index = 0; index < this.object.length; index++) {
      //   // object[index].rotation.z += 0.01;
      //   // object[index].rotation.y += 0.01;
      // }
      this.controls.update();
      this.renderer.setSize(this.width, this.height);
      this.renderer.render(this.scene, this.camera);
    },
    getVW(percent) {
      return (window.innerWidth * percent) / 100;
    },
    getVH(percent) {
      return (window.innerHeight * percent) / 100;
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
    create101(x, y, z) {
      // console.log(this.size["HSSP"]);

      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["HSSP"][0],
          this.size["HSSP"][1],
          this.size["HSSP"][2]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.x = 0;
      cubeA.position.y = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["HSSP"][0],
          this.size["HSSP"][1],
          this.size["HSSP"][2]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.x = 0;
      cubeB.position.y = 0 + this.size["HSSP"][0] + this.size["HSSP"][0] / 2;
      cubeB.position.z = 0;
      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      this.scene.add(group);
      group.position.x = x;
      group.position.y = y;
      group.position.z = z - this.size["HSSP"][0] / 2;
      return this.size["HSSP"][0];
    },
    create102(x, y, z) {
      console.log(this.size["SMP"]);
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][0],
          this.size["SMP"][2],
          this.size["SMP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][0],
          this.size["SMP"][2],
          this.size["SMP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0 + this.size["SMP"][2];
      cubeB.position.x = 0;
      cubeB.position.z = 0;

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][0],
          this.size["SMP"][2],
          this.size["SMP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeC.position.y = 0 + this.size["SMP"][2] * 2;
      cubeC.position.x = 0;
      cubeC.position.z = 0;

      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      this.scene.add(group);
      group.position.x = x;
      group.position.y = y;
      group.position.z = z - this.size["SMP"][0] / 2;
      return this.size["SMP"][0];
    },
    create103(x, y, z) {
      console.log(this.size["SSP"]);
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][0],
          this.size["SSP"][2],
          this.size["SSP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][0],
          this.size["SSP"][2],
          this.size["SSP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0 + this.size["SSP"][2];
      cubeB.position.x = 0;
      cubeB.position.z = 0;

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][0],
          this.size["SSP"][2],
          this.size["SSP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeC.position.y = 0 + this.size["SSP"][2] * 2;
      cubeC.position.x = 0;
      cubeC.position.z = 0;

      cubeB.position.y = 0 + this.size["SSP"][2];
      cubeB.position.x = 0;
      cubeB.position.z = 0;

      const cubeD = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][0],
          this.size["SSP"][2],
          this.size["SSP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeD.position.y = 0 + this.size["SSP"][2] * 3;
      cubeD.position.x = 0;
      cubeD.position.z = 0;

      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      group.add(cubeD);
      this.scene.add(group);
      group.position.x = x;
      group.position.y = y;
      group.position.z = z - this.size["SSP"][0] / 2;
      return this.size["SSP"][0];
    },
    create104() {
      console.log(this.size["MP"]);

      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["MP"][0],
          this.size["MP"][2],
          this.size["MP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["MP"][0],
          this.size["MP"][2],
          this.size["MP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0 + this.size["MP"][0];
      cubeB.position.x = 0;
      cubeB.position.z = 0;
      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      this.scene.add(group);
    },
    create105() {
      console.log(this.size["MLP"]);
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["MLP"][0],
          this.size["MLP"][2],
          this.size["MLP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["MLP"][0],
          this.size["MLP"][2],
          this.size["MLP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0 + this.size["MLP"][2];
      cubeB.position.x = 0;
      cubeB.position.z = 0;

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["MLP"][0],
          this.size["MLP"][2],
          this.size["MLP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeC.position.y = 0 + this.size["MLP"][2] * 2;
      cubeC.position.x = 0;
      cubeC.position.z = 0;

      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      this.scene.add(group);
    },
    create106(x, y, z) {
      console.log(this.size["LP"]);
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["LP"][0],
          this.size["LP"][2],
          this.size["LP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["LP"][0],
          this.size["LP"][2],
          this.size["LP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0 + this.size["LP"][2];
      cubeB.position.x = 0;
      cubeB.position.z = 0;

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["LP"][0],
          this.size["LP"][2],
          this.size["LP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeC.position.y = 0 + this.size["LP"][2] * 2;
      cubeC.position.x = 0;
      cubeC.position.z = 0;

      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      this.scene.add(group);
      group.rotation.y = 1.571;
      group.position.x = x - 0.3;
      group.position.y = y;
      group.position.z = z - this.size["LP"][2] / 2 - 0.2;
      return this.size["LP"][2] + 0.3;
    },
    create201(x, y, z) {
      console.log(this.size["SSP"]);
      console.log(this.size["HSSP"]);
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][0],
          this.size["SSP"][2],
          this.size["SSP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][0],
          this.size["SSP"][2],
          this.size["SSP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0 + this.size["SSP"][2];
      cubeB.position.x = 0;
      cubeB.position.z = 0;

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["HSSP"][0],
          this.size["HSSP"][2],
          this.size["HSSP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeC.position.y = 0 + this.size["HSSP"][2] + this.size["SSP"][2] / 2;
      cubeC.position.x = 0;
      cubeC.position.z = 0;

      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      this.scene.add(group);
      group.position.x = x;
      group.position.y = y;
      group.position.z = z - this.size["SSP"][0] / 2;
      return this.size["SSP"][0];
    },
    create202() {
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][0],
          this.size["SMP"][2],
          this.size["SMP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][0],
          this.size["SMP"][2],
          this.size["SMP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
      );
      cubeB.position.y = 0;
      cubeB.position.x = 0 - this.size["SMP"][0];
      cubeB.position.z = 0;

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["ETC"][2],
          this.size["ETC"][1],
          this.size["ETC"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
      );
      cubeC.position.y = 0 + this.size["SMP"][2] + this.size["SMP"][2] / 2;
      cubeC.position.x = -0.38;
      cubeC.position.z = 0;
      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      this.scene.add(group);
      // group.rotation.y = 1.571;
      // group.position.x = x;
      // group.position.y = y;
      // group.position.z = z - this.size["SMP"][0] + 0.4;
      return this.size["SMP"][0];
    },
    create203() {
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][0],
          this.size["SSP"][2],
          this.size["SSP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][0],
          this.size["SSP"][2],
          this.size["SSP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
      );
      cubeB.position.y = 0;
      cubeB.position.x =
        0 + this.size["SSP"][2] + this.size["SSP"][2] / 2 - 0.05;
      cubeB.position.z = 0;
      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["ETC"][2],
          this.size["ETC"][1],
          this.size["ETC"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
      );
      cubeC.position.y =
        0 + this.size["SSP"][0] / 2 + this.size["SSP"][0] - 0.15;
      cubeC.position.x = 0 + 0.37;
      cubeC.position.z = 0;
      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      this.scene.add(group);
    },
    create204() {
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["ETC"][2],
          this.size["ETC"][1],
          this.size["ETC"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;
      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["ETC"][2],
          this.size["ETC"][1],
          this.size["ETC"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
      );
      cubeB.position.y = 0;
      cubeB.position.x = 0;
      cubeB.position.z = 0+this.size["ETC"][0];

            const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["LHP"][0],
          this.size["LHP"][2],
          this.size["LHP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })

      );
      cubeC.position.y = this.size["ETC"][2]-0.38;
      cubeC.position.x = 0;
      cubeC.position.z = +0.56;
      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      this.scene.add(group);
    },
    create205() {
      console.log(this.size["HSSP"]);
      console.log(this.size["MP"]);

      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["HSSP"][2],
          this.size["HSSP"][1],
          this.size["HSSP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["HSSP"][2],
          this.size["HSSP"][1],
          this.size["HSSP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0;
      cubeB.position.x = 0;
      cubeB.position.z = 0 - this.size["HSSP"][0];

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["HSSP"][2],
          this.size["HSSP"][1],
          this.size["HSSP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeC.position.y = 0;
      cubeC.position.x = 0;
      cubeC.position.z = (0 - this.size["HSSP"][0]) * 2;

      const cubeD = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["MP"][0],
          this.size["MP"][2],
          this.size["MP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeD.position.y = 0 + this.size["HSSP"][0] + this.size["HSSP"][0] / 2;
      cubeD.position.x = 0;
      cubeD.position.z = 0 - this.size["HSSP"][2] / 2;

      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      group.add(cubeD);
      this.scene.add(group);
    },
    create206(x, y, z) {
      console.log(this.size["SMP"]);
      console.log(this.size["MLP"]);

      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][1],
          this.size["SMP"][2],
          this.size["SMP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][1],
          this.size["SMP"][2],
          this.size["SMP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0;
      cubeB.position.x = 0;
      cubeB.position.z = 0 - this.size["SMP"][0];

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][1],
          this.size["SMP"][2],
          this.size["SMP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeC.position.y = 0;
      cubeC.position.x = 0;
      cubeC.position.z = (0 - this.size["SMP"][0]) * 2;

      const cubeD = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][1],
          this.size["SMP"][2],
          this.size["SMP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeD.position.y = 0 + this.size["SMP"][0];
      cubeD.position.x = 0;
      cubeD.position.z = 0;

      const cubeE = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][1],
          this.size["SMP"][2],
          this.size["SMP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeE.position.y = 0 + this.size["SMP"][0];
      cubeE.position.x = 0;
      cubeE.position.z = 0 - this.size["SMP"][0];

      const cubeF = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SMP"][1],
          this.size["SMP"][2],
          this.size["SMP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeF.position.y = 0 + this.size["SMP"][0];
      cubeF.position.x = 0;
      cubeF.position.z = (0 - this.size["SMP"][0]) * 2;

      const cubeG = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["MLP"][0],
          this.size["MLP"][2],
          this.size["MLP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeG.position.y = 0 + this.size["SMP"][1] + this.size["SMP"][0] / 2;
      cubeG.position.x = 0;
      cubeG.position.z = 0 - this.size["SMP"][1] / 2;

      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      group.add(cubeD);
      group.add(cubeE);
      group.add(cubeF);
      group.add(cubeG);
      this.scene.add(group);
      group.rotation.y = 1.571;
      group.position.x = x;
      group.position.y = y;
      group.position.z = z - this.size["SMP"][0] + 0.4;
      return this.size["SMP"][0];
    },
    create207() {
      console.log(this.size["LHP"]);
      console.log(this.size["LP"]);
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["LHP"][0],
          this.size["LHP"][2],
          this.size["LHP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["LP"][0],
          this.size["LP"][2],
          this.size["LP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0.05 + this.size["LP"][2];
      cubeB.position.x = 0;
      cubeB.position.z = 0;

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["LP"][0],
          this.size["LP"][2],
          this.size["LP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeC.position.y = 0.05 + this.size["LP"][2] * 2;
      cubeC.position.x = 0;
      cubeC.position.z = 0;

      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      this.scene.add(group);
    },
    create208() {
      console.log(this.size["SSP"]);
      console.log(this.size["MP"]);

      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      const cubeA = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][1],
          this.size["SSP"][2],
          this.size["SSP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeA.position.y = 0;
      cubeA.position.x = 0;
      cubeA.position.z = 0;

      const cubeB = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][1],
          this.size["SSP"][2],
          this.size["SSP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeB.position.y = 0;
      cubeB.position.x = 0;
      cubeB.position.z = 0 - this.size["SSP"][0];

      const cubeC = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][1],
          this.size["SSP"][2],
          this.size["SSP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeC.position.y = 0;
      cubeC.position.x = 0;
      cubeC.position.z = (0 - this.size["SSP"][0]) * 2;

      const cubeD = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][1],
          this.size["SSP"][2],
          this.size["SSP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeD.position.y = 0 + this.size["SSP"][2];
      cubeD.position.x = 0;
      cubeD.position.z = 0;

      const cubeE = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][1],
          this.size["SSP"][2],
          this.size["SSP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeE.position.y = 0 + this.size["SSP"][2];
      cubeE.position.x = 0;
      cubeE.position.z = 0 - this.size["SSP"][0];

      const cubeF = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["SSP"][1],
          this.size["SSP"][2],
          this.size["SSP"][0]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeF.position.y = 0 + this.size["SSP"][2];
      cubeF.position.x = 0;
      cubeF.position.z = (0 - this.size["SSP"][0]) * 2;

      const cubeG = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["MP"][0],
          this.size["MP"][2],
          this.size["MP"][1]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture })
        // new THREE.MeshBasicMaterial({
        //   color: this.color[S1],
        //   side: THREE.BackSide,
        // })
      );
      cubeG.position.y = 0 + this.size["SSP"][2] + this.size["SSP"][0] / 2;
      cubeG.position.x = 0;
      cubeG.position.z = 0 - this.size["SSP"][1] / 2;

      const group = new THREE.Group();
      group.add(cubeA);
      group.add(cubeB);
      group.add(cubeC);
      group.add(cubeD);
      group.add(cubeE);
      group.add(cubeF);
      group.add(cubeG);
      this.scene.add(group);
    },
    createSmall() {
      var crateTexture2 = new THREE.ImageUtils.loadTexture(
        require("@/assets/containerBackground.jpg")
      );
      const planeBottom = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["Small"][0],
          this.size["Small"][1],
          this.size["Small"][2]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture2 })
        // new THREE.MeshBasicMaterial({
        //   color: 0xb4b4b4,
        //   side: THREE.BackSide,
        // })
      );
      planeBottom.position.y = -2;
      planeBottom.rotation.z = 1.571;
      this.scene.add(planeBottom);
      return [this.size["Small"][1] / 2, this.size["Small"][2] / 2];
    },
    createLarge() {
      var crateTexture2 = new THREE.ImageUtils.loadTexture(
        require("@/assets/containerBackground.jpg")
      );
      const planeBottom = new THREE.Mesh(
        new THREE.BoxGeometry(
          this.size["Large"][0],
          this.size["Large"][1],
          this.size["Large"][2]
        ),
        new THREE.MeshBasicMaterial({ map: crateTexture2 })
        // new THREE.MeshBasicMaterial({
        //   color: 0xb4b4b4,
        //   side: THREE.BackSide,
        // })
      );
      planeBottom.position.z = 0.2;
      planeBottom.position.y = -2;
      planeBottom.rotation.z = 1.571;
      this.scene.add(planeBottom);
      return [this.size["Large"][1] / 2, this.size["Large"][2] / 2];
    },
    create20Standard() {},
    create40Standard() {},
    create40HighCube() {},
  },
  mounted() {
    console.log("after");
    this.init();
    this.animate();
    // console.log(this.object);
    // console.log(this.scene);
    // console.log(this.camera);
    // console.log(this.renderer);
    // console.log(this.controls);
    // console.log(this.$refs.model.parentElement.appendChild('p'))
  },
};
</script>

<style scoped>
#model {
  width: 100%;
  height: 100%;
}
</style>