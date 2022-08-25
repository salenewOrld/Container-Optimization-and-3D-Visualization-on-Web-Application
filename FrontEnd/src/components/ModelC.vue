<template>
  <div :id="element"></div>
</template>>

<script>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import store from "@/store";
export default {
  name: "ModelC",
  props: {
    type: String,
    area: Array,
    element: String,
    width: Number,
    height: Number,
    index: Number,
  },
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      wall1: null,
      wall2: null,
      boxsRow1: [],
      boxsRow2: [],
      boxsRow3: [],
      first: true,
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
      size1: [0.76, 1.12, 1.09],
      input: [
        {
          Type: "Small",
          Area: [
            [106, 0, 0],
            [101, 101, 101],
            [101, 101, 101],
            [101, 101, 101],
            [101, 101, 101],
            [101, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
          ],
          outputs: [
            ["Color", "Name", "Package", "Volume", "Weight"],
            ["#ffff00", "BoxSmall_3", "10", 28.6, "20"],
            ["#80ff00", "BoxMedium_1", "4", 2.28 * 4, "20"],
            ["#00ffff", "BoxMedium_2", "1", 2.4 * 1, "30"],
            ["#0040ff", "BoxMedium_3", "2", 2.66 * 2, "40"],
          ],
        },
      ],
      stack_info: {
        101: [0.76, 1.12, 1.09],
        102: [0.76, 1.12, 0.73],
        103: [0.76, 1.12, 0.54],
        104: [1.1, 1.8, 1.09],
        105: [1.1, 1.8, 0.73],
        106: [1.515, 2.22, 0.73],
        201: [0.76, 1.12, 2.17],
        202: [0.76, 2.24, 2.24],
        203: [0.76, 2.24, 2.24],
        204: [2.2, 1.5, 2.4],
        205: [2.28, 1.12, 2.18],
        206: [2.28, 1.12, 2.19],
        207: [1.515, 2.22, 2.31],
        208: [2.28, 1.12, 2.17],
        0: [0, 0, 0],
      },
    };
  },
  methods: {
    init() {
      console.log("init");
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(
        75,
        this.width / this.height,
        0.1,
        1000
      );
      this.camera.position.set(6, 3, 5);
      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(this.width, this.height);
      document
        .getElementById(this.element)
        .appendChild(this.renderer.domElement);
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
      this.renderer.setSize(store.getters.width, store.getters.height);
      this.renderer.render(this.scene, this.camera);
      this.controls.update();
      if (store.getters.load) {
      console.log("api call data 100%");
      this.first = false;
      store.commit("setload", false);
      //console.log(store.getters.output.Data.Container[0][0].Container)
      // for (let index = 0; index < store.getters.output.Data.Container.length; index++) {
      //   console.log(index)

      // }
      this.createStack();
    }
      this.ajustStack();
      requestAnimationFrame(this.animate);
    },
    createWall() {
      // Materials

      const material1 = new THREE.MeshBasicMaterial();
      material1.color = new THREE.Color(0xff0000);

      const material2 = new THREE.MeshBasicMaterial();
      material2.color = new THREE.Color(0x0000ff);

      // wall
      const geometryWall = new THREE.BoxGeometry(0.001, 2, 100);
      const materialWall = new THREE.MeshBasicMaterial();
      materialWall.colorWrite = false;
      materialWall.transparent = true;

      this.wall1 = new THREE.Mesh(geometryWall, materialWall);
      this.wall2 = new THREE.Mesh(geometryWall, materialWall);

      this.scene.add(this.wall1);
      this.scene.add(this.wall2);

      this.wall1.position.set(1, 0, 0);

      this.wall2.rotateY(1.571);
      this.wall2.position.set(0, 0, -0.5);

      // Lights

      const pointLight = new THREE.PointLight(0xffffff, 0.1);
      pointLight.position.x = 2;
      pointLight.position.y = 3;
      pointLight.position.z = 4;
      this.scene.add(pointLight);
    },
    createStack() {
      this.OtimalOutpus();
      console.log("index = ", this.index);
      console.log(
        "exam data = ",
        store.getters.output[this.index - 1][0].Container
      );
      // console.log(store.getters.output[this.index-1][0].Container_Type)
      //store.getters.output.Data.Container_Type
      this.GeneratorContainer(
        store.getters.output[this.index - 1][0].Container_Type,
        0,
        0,
        0
      );

      // for (let i = 0; i < store.getters.output.Data.Container.length; i++) {
      for (
        let y = 0;
        y < store.getters.output[this.index - 1][0].Container.length;
        y++
      ) {
        for (
          let j = 0;
          j < store.getters.output[this.index - 1][0].Container[y].length;
          j++
        ) {
          if (j == 0) {
            this.boxsRow1.push(
              this.GeneratorStack(
                store.getters.output[this.index - 1][0].Container[y][j],
                0,
                0,
                0
              )
            );
          } else if (j == 1) {
            this.boxsRow2.push(
              this.GeneratorStack(
                store.getters.output[this.index - 1][0].Container[y][j],
                0,
                0,
                0
              )
            );
          } else {
            this.boxsRow3.push(
              this.GeneratorStack(
                store.getters.output[this.index - 1][0].Container[y][j],
                0,
                0,
                0
              )
            );
          }
        }
      }
      // }

      // add offset
      for (let i = 0; i < this.boxsRow1.length; i++) {
        this.boxsRow1[i].position.set(-i * 3, 0, 3);
      }

      for (let i = 0; i < this.boxsRow2.length; i++) {
        this.boxsRow2[i].position.set(-i * 3, 0, 5);
      }

      for (let i = 0; i < this.boxsRow3.length; i++) {
        this.boxsRow3[i].position.set(-i * 3, 0, 7);
      }
    },
    ajustStack() {
      // Set boundary for wall and box
      var wall1BB = new THREE.Box3().setFromObject(this.wall1);
      var wall2BB = new THREE.Box3().setFromObject(this.wall2);
      var boxsRow1BB = [];
      var boxsRow2BB = [];
      var boxsRow3BB = [];
      for (var box of this.boxsRow1) {
        boxsRow1BB.push(new THREE.Box3().setFromObject(box));
      }
      for (let i = 0; i < boxsRow1BB.length; i++) {
        boxsRow1BB[i].expandByVector(new THREE.Vector3(0.025, 0, 0.025));
      }
      for (box of this.boxsRow2) {
        boxsRow2BB.push(new THREE.Box3().setFromObject(box));
      }
      for (let i = 0; i < boxsRow2BB.length; i++) {
        boxsRow2BB[i].expandByVector(new THREE.Vector3(0.025, 0, 0.025));
      }

      for (box of this.boxsRow3) {
        boxsRow3BB.push(new THREE.Box3().setFromObject(box));
      }

      for (let i = 0; i < boxsRow3BB.length; i++) {
        boxsRow3BB[i].expandByVector(new THREE.Vector3(0.025, 0, 0.025));
      }

      var allCollide = true;
      var collideArr = [];
      for (let i = 0; i < boxsRow3BB.length; i++) {
        var collideWall = false;
        var collideRow1 = false;
        var collideRow2 = false;

        if (boxsRow3BB[i].intersectsBox(wall2BB)) {
          collideWall = true;
        }

        for (let j = 0; j < boxsRow1BB.length; j++) {
          if (boxsRow3BB[i].intersectsBox(boxsRow1BB[j])) {
            collideRow1 = true;
          }
        }

        for (let j = 0; j < boxsRow2BB.length; j++) {
          if (boxsRow3BB[i].intersectsBox(boxsRow2BB[j])) {
            collideRow2 = true;
          }
        }

        collideArr.push(collideWall || collideRow1 || collideRow2);
      }

      for (var collide of collideArr) {
        if (!collide) {
          allCollide = false;
        }
      }

      // Translate algorithm for row 1
      for (let i = 0; i < boxsRow1BB.length; i++) {
        collide = false;

        for (let j = 0; j < boxsRow1BB.length; j++) {
          if (
            boxsRow1BB[i] != boxsRow1BB[j] &&
            boxsRow1BB[i].intersectsBox(boxsRow1BB[j])
          ) {
            collide = true;
          }
        }

        if (!boxsRow1BB[i].intersectsBox(wall2BB)) {
          this.boxsRow1[i].translateZ(-0.05);
        } else if (
          !boxsRow1BB[i].intersectsBox(wall1BB) &&
          allCollide &&
          !collide
        ) {
          this.boxsRow1[i].translateX(0.05);
        }
      }

      // Translate algorithm for row 2
      for (let i = 0; i < boxsRow2BB.length; i++) {
        var collideX = false;
        collideRow1 = false;

        // Check collide along X axis
        for (let j = 0; j < boxsRow2BB.length; j++) {
          if (
            boxsRow2BB[i] != boxsRow2BB[j] &&
            boxsRow2BB[i].intersectsBox(boxsRow2BB[j])
          ) {
            collideX = true;
          }
        }

        // Check collide along Z axis
        for (let j = 0; j < boxsRow1BB.length; j++) {
          if (boxsRow2BB[i].intersectsBox(boxsRow1BB[j])) {
            collideRow1 = true;
          }
        }

        if (!boxsRow2BB[i].intersectsBox(wall2BB) && !collideRow1) {
          this.boxsRow2[i].translateZ(-0.05);
        } else if (!boxsRow2BB[i].intersectsBox(wall1BB) && allCollide) {
          if (boxsRow2BB[i].intersectsBox(wall2BB) && !collideRow1) {
            this.boxsRow2[i].translateX(0.05);
          } else if (collideRow1 && !collideX) {
            if (i != 0) {
              if (
                !boxsRow2BB[i].intersectsBox(boxsRow1BB[i - 1]) &&
                !boxsRow2BB[i].intersectsBox(boxsRow3BB[i - 1])
              ) {
                this.boxsRow2[i].translateX(0.05);
              } // else if () {
              //   this.boxsRow2[i].translateX(.025)
              // }
            } else {
              this.boxsRow2[i].translateX(0.05);
            }
          }
        }
      }

      // Translate algorithm for row 3
      for (let i = 0; i < boxsRow3BB.length; i++) {
        collideX = false;
        collideRow1 = false;
        collideRow2 = false;

        // Check collide along X axis
        for (let j = 0; j < boxsRow3BB.length; j++) {
          if (
            boxsRow3BB[i] != boxsRow3BB[j] &&
            boxsRow3BB[i].intersectsBox(boxsRow3BB[j])
          ) {
            collideX = true;
          }
        }

        // Check collide for row 1
        for (let j = 0; j < boxsRow2BB.length; j++) {
          if (boxsRow3BB[i].intersectsBox(boxsRow2BB[j])) {
            collideRow2 = true;
          }
        }

        // Check collide for row 2
        for (let j = 0; j < boxsRow1BB.length; j++) {
          if (boxsRow3BB[i].intersectsBox(boxsRow1BB[j])) {
            collideRow1 = true;
          }
        }

        if (
          !boxsRow3BB[i].intersectsBox(wall2BB) &&
          !collideRow1 &&
          !collideRow2
        ) {
          this.boxsRow3[i].translateZ(-0.05);
        } else if (!boxsRow3BB[i].intersectsBox(wall1BB) && allCollide) {
          if (boxsRow3BB[i].intersectsBox(wall2BB) && !collideRow1) {
            this.boxsRow3[i].translateX(0.05);
          } else if (collideRow1 && !collideRow2) {
            this.boxsRow3[i].translateX(0.05);
          } else if (collideRow2 && !collideX && !collideRow1) {
            this.boxsRow3[i].translateX(0.05);
          }
        }
      }
    },
    GeneratorStack(stack, x, y, z) {
      var crateTexture = new THREE.ImageUtils.loadTexture(
        require("@/assets/crate.png")
      );
      switch (stack) {
        case 101: {
          const cubeA = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["HSSP"][0],
              this.size["HSSP"][1],
              this.size["HSSP"][2]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture })
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
          );
          cubeB.position.x = 0;
          cubeB.position.y =
            0 + this.size["HSSP"][0] + this.size["HSSP"][0] / 2;
          cubeB.position.z = 0;
          const group = new THREE.Group();
          cubeA.rotateY(1.5721);
          cubeB.rotateY(1.5721);
          group.add(cubeA);
          group.add(cubeB);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - this.size["HSSP"][0] / 2;
          return group;
        }
        case 102: {
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
          cubeA.rotateY(1.5721);
          cubeB.rotateY(1.5721);
          cubeC.rotateY(1.5721);
          group.add(cubeA);
          group.add(cubeB);
          group.add(cubeC);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - this.size["SMP"][0] / 2;
          return group;
        }
        case 103: {
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
          cubeA.rotateY(1.5721);
          cubeB.rotateY(1.5721);
          cubeC.rotateY(1.5721);
          cubeD.rotateY(1.5721);
          group.add(cubeA);
          group.add(cubeB);
          group.add(cubeC);
          group.add(cubeD);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - this.size["SSP"][0] / 2;
          return group;
        }
        case 104: {
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
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - this.size["MP"][0] / 2;
          return group;
        }
        case 105: {
          const cubeA = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["MLP"][0],
              this.size["MLP"][2],
              this.size["MLP"][1]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture })
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
          );
          cubeC.position.y = 0 + this.size["MLP"][2] * 2;
          cubeC.position.x = 0;
          cubeC.position.z = 0;

          const group = new THREE.Group();
          group.add(cubeA);
          group.add(cubeB);
          group.add(cubeC);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - this.size["MLP"][0] / 2;
          return group;
        }
        case 106: {
          const cubeA = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["LP"][0],
              this.size["LP"][2],
              this.size["LP"][1]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture })
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
          );
          cubeC.position.y = 0 + this.size["LP"][2] * 2;
          cubeC.position.x = 0;
          cubeC.position.z = 0;

          const group = new THREE.Group();
          group.add(cubeA);
          group.add(cubeB);
          group.add(cubeC);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - this.size["LP"][0] / 2;
          return group;
        }
        case 201: {
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
          );
          cubeC.position.y = 0 + this.size["HSSP"][2] + this.size["SSP"][2] / 2;
          cubeC.position.x = 0;
          cubeC.position.z = 0;

          const group = new THREE.Group();
          cubeA.rotateY(1.5721);
          cubeB.rotateY(1.5721);
          cubeC.rotateY(1.5721);
          group.add(cubeA);
          group.add(cubeB);
          group.add(cubeC);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - this.size["SSP"][0] / 2;
          return group;
        }
        case 202: {
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
          return group;
        }
        case 203: {
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
          return group;
        }
        case 204: {
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
          cubeB.position.z = 0 + this.size["ETC"][0];

          const cubeC = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["LHP"][0],
              this.size["LHP"][2],
              this.size["LHP"][1]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture })
          );
          cubeC.position.y = this.size["ETC"][2] - 0.38;
          cubeC.position.x = 0;
          cubeC.position.z = +0.56;
          const group = new THREE.Group();
          group.add(cubeA);
          group.add(cubeB);
          group.add(cubeC);
          this.scene.add(group);
          return group;
        }
        case 205: {
          const cubeA = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["HSSP"][2],
              this.size["HSSP"][1],
              this.size["HSSP"][0]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture })
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
          );
          cubeD.position.y =
            0 + this.size["HSSP"][0] + this.size["HSSP"][0] / 2;
          cubeD.position.x = 0;
          cubeD.position.z = 0 - this.size["HSSP"][2] / 2;

          const group = new THREE.Group();
          group.add(cubeA);
          group.add(cubeB);
          group.add(cubeC);
          group.add(cubeD);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - (this.size["HSSP"][0] / 2) * 3;
          return group;
        }
        case 206: {
          const cubeA = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["SMP"][1],
              this.size["SMP"][2],
              this.size["SMP"][0]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture })
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
          // group.rotation.y = 1.571;
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - (this.size["SMP"][0] / 2) * 3;
          return group;
        }
        case 207: {
          const cubeA = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["LHP"][0],
              this.size["LHP"][2],
              this.size["LHP"][1]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture })
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
          );
          cubeC.position.y = 0.05 + this.size["LP"][2] * 2;
          cubeC.position.x = 0;
          cubeC.position.z = 0;

          const group = new THREE.Group();
          group.add(cubeA);
          group.add(cubeB);
          group.add(cubeC);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - this.size["LHP"][0] / 2;
          return group;
        }
        case 208: {
          const cubeA = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["SSP"][1],
              this.size["SSP"][2],
              this.size["SSP"][0]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture })
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
          group.position.x = x;
          group.position.y = y;
          group.position.z = z - (this.size["SSP"][0] / 2) * 3;
          return group;
        }
        default: {
          const cubeA = new THREE.Mesh(
            new THREE.BoxGeometry(0, 0, 0),
            new THREE.MeshBasicMaterial({ map: crateTexture })
          );
          cubeA.position.x = 0;
          cubeA.position.y = 0;
          cubeA.position.z = 0;
          const group = new THREE.Group();
          group.add(cubeA);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z;
          return group;
        }
      }
    },
    OtimalOutpus() {
      const maxRow = 2.37;
      const minRow = 2;
      console.log(
        "usecase = ",
        store.getters.output[this.index - 1][0].Container
      );

      let old = JSON.parse(
        JSON.stringify(store.getters.output[this.index - 1][0].Container)
      );
      let newAra = JSON.parse(
        JSON.stringify(store.getters.output[this.index - 1][0].Container)
      );
      console.log("copy = ", old);
      for (let z = 0; z < old.length; z++) {
        for (let x = 0; x < old[z].length; x++) {
          //console.log(newAra[z][x])
          // console.log(this.stack_info[101])
          // console.log(newAra[z][x])
          //console.log(this.stack_info[newAra[z][x]][0])
          old[z][x] = this.stack_info[newAra[z][x]][0];
        }
      }

      console.log("convert = ", old);
      console.log("original = ", newAra);

      for (let index = 0; index < old.length - 1; index++) {
        let hasValue = 0;
        for (const value in old[index]) {
          //console.log(old[index][value]);
          hasValue = hasValue + old[index][value];
        }
        if (hasValue > minRow) {
          console.log("แถวเต็ม");
        } else {
          console.log("แถวว่าง");
          for (const value in old[index + 1]) {
            if (old[index + 1][value] != 0) {
              if (hasValue + old[index + 1][value] < maxRow) {
                let temp = old[index + 1][value];
                let temp2 =
                  store.getters.output[this.index - 1][0].Container[index + 1][
                    value
                  ];
                old[index + 1][value] = 0;
                store.getters.output[this.index - 1][0].Container[index + 1][
                  value
                ] = 0;
                for (const value in old[index]) {
                  if (old[index][value] == 0) {
                    old[index][value] = temp;
                    store.getters.output[this.index - 1][0].Container[index][
                      value
                    ] = temp2;
                    temp = 0;
                    temp2 = 0;
                  }
                }
              }
            }
          }
        }
        //console.log('sum = '+hasValue)
      }
      console.log("After = " + old);
      console.log("after = ", newAra);
    },
    create20Standard() {},
    create40Standard() {},
    create40HighCube() {},
    GeneratorContainer(container, x, y, z) {
      var crateTexture2 = new THREE.ImageUtils.loadTexture(
        require("@/assets/containerBackground.jpg")
      );
      switch (container) {
        case "Small": {
          const planeBottom = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["Small"][0],
              this.size["Small"][1],
              this.size["Small"][2]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture2 })
          );
          planeBottom.position.x = x - 2;
          planeBottom.position.y = y - 0.7;
          planeBottom.position.z = z + 0.7;
          planeBottom.rotation.z = 1.571;
          planeBottom.rotation.y = 1.571;
          this.scene.add(planeBottom);
          break;
        }
        case "Large": {
          const planeBottom = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["Large"][0],
              this.size["Large"][1],
              this.size["Large"][2]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture2 })
          );
          planeBottom.position.x = x - 5;
          planeBottom.position.y = y - 0.7;
          planeBottom.position.z = z + 0.7;
          planeBottom.rotation.z = 1.571;
          planeBottom.rotation.y = 1.571;
          this.scene.add(planeBottom);
          break;
        }
        case "20Standard": {
          const planeBottom = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["Standard20"][0],
              this.size["Standard20"][1],
              this.size["Standard20"][2]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture2 })
          );
          planeBottom.position.x = x - 2;
          planeBottom.position.y = y - 0.7;
          planeBottom.position.z = z + 0.7;
          planeBottom.rotation.z = 1.571;
          planeBottom.rotation.y = 1.571;
          this.scene.add(planeBottom);
          break;
        }
        case "40Standard": {
          const planeBottom = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["Standard40"][0],
              this.size["Standard40"][1],
              this.size["Standard40"][2]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture2 })
          );
          planeBottom.position.x = x - 5;
          planeBottom.position.y = y - 0.7;
          planeBottom.position.z = z + 0.7;
          planeBottom.rotation.z = 1.571;
          planeBottom.rotation.y = 1.571;
          this.scene.add(planeBottom);
          break;
        }
        case "40HighCube": {
          const planeBottom = new THREE.Mesh(
            new THREE.BoxGeometry(
              this.size["HighCube40"][0],
              this.size["HighCube40"][1],
              this.size["HighCube40"][2]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture2 })
          );
          planeBottom.position.x = x - 5;
          planeBottom.position.y = y - 0.7;
          planeBottom.position.z = z + 0.7;
          planeBottom.rotation.z = 1.571;
          planeBottom.rotation.y = 1.571;
          this.scene.add(planeBottom);
          break;
        }
      }
    },
  },
  created() {},
  mounted() {
    // var lis = this.$refs.ul.getElementsByTagName("li");
    //console.log(store.getters.outputs)
    this.init();
    this.createWall();
    this.animate();

    //console.log("Height = " + store.getters.width);
  },
};
</script>

<style scoped>
</style>