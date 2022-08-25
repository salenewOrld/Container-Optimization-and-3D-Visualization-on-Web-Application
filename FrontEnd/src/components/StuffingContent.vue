<template>
  <v-container id="setheight" class="grey lighten-5">
    <v-row id="setheight">
      <v-col class="t1" cols="4" sm="4" md="4">
        <v-row justify="center" align="center">
          <div :id="Element" :ref="Element"></div>
          <!-- <ModelC :element="'id' + n" :width="380" :height="200" :index="n"></ModelC> -->
          <!-- <v-dialog transition="dialog-bottom-transition" hide-overlay v-model="dialog" width="80vw">
                            <template v-slot:activator="{ on, attrs }">
                                <v-btn class="btnSize" color="primary" v-bind="attrs" v-on="on">
                                    แสดงเต็มจอ
                                </v-btn>
                            </template>
                            <v-card elevation="4" outlined height="80vh" width="80vw">
                                <div :id="'id' + n" justify="center" align="center">
                                    <modelC :element="'idfull' + n" :width="getVW(79.5)" :height="getVH(79.5)"
                                        :index="n"></modelC>
                                </div>
                            </v-card>
                        </v-dialog> -->
        </v-row>
      </v-col>
      <v-col cols="8" sm="8" md="8">
        <v-row>
          <v-col class="font-weight-bold text-h6 basil--text amber lighten-1" cols="6" sm="3" md="2">
            <p>{{ Container_Type }}</p>
          </v-col>
          <v-col class="font-weight-bold text-h6 basil--text amber lighten-1" cols="6" sm="9" md="10">
            <p>พื้นที่ {{ Area }} ตารางเมตร</p>
            <p>น้ำหนัก {{ Weight }} กิโลกรัม</p>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="t3" cols="4" sm="4" md="4">
            <apexchart
              :options="chartOptions"
              :series="ContainerData"
            ></apexchart>
          </v-col>
          <v-col class="font-weight-bold text-subtitle-1 basil--text amber lighten-4" cols="8" sm="8" md="8">
            <v-row
              v-for="(n, index) in BoxName"
              :key="index"
              justify="center"
              align="center"
            >
              <v-col cols="6" sm="5" md="4"> 
                <p v-if="ContainerData[index] != 0" >ใช้งานกล่อง</p>
              </v-col>
              <v-col cols="4" sm="3" md="2">
                  <p v-if="ContainerData[index] != 0" >{{ n }} ทั้งหมด</p>
              </v-col>
              <v-col cols="3" sm="2" md="1">
                <p v-if="ContainerData[index] != 0" >{{ ContainerData[index] }}</p>
                </v-col
              >
              <v-col cols="3" sm="2" md="1">
<p v-if="ContainerData[index] != 0" > กล่อง</p>
            </v-col
              >
            </v-row>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import apexchart from "vue-apexcharts";
export default {
  name: "StuffingContent",
  components: { apexchart },
  model: {
    Element,
    Container_Type: null,
    Container: null,
    Weight: null,
    Area: null,
    ContainerData: null,
  },
  props: {
    Element: String,
    Container_Type: String,
    Container: Array,
    Weight: String,
    Area: String,
    ContainerData: Array,
    BoxName: Array,
  },
  data() {
    return {
      chartOptions: {
        chart: {
          width: 100,
          height: 100,
          type: "donut",
        },
        plotOptions: {
          pie: {
            startAngle: -90,
            endAngle: 270,
          },
        },
        dataLabels: {
          enabled: false,
        },
        labels: ["SSP", "SMP", "HSSP", "SMP", "MLP", "LHP", "LP", "ETC"],
        fill: {
          colors: [
            "#ffff00",
            "#80ff00",
            "#00ffff",
            "#0040ff",
            "#8000ff",
            "#ff00ff",
            "#ff0040",
            "#000000",
          ],
          type: "gradient",
        },
        legend: {
          show: false,
        },
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 100,
              },
            },
          },
        ],
      },
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      wall1: null,
      wall2: null,
      boxsRow1: [],
      boxsRow2: [],
      boxsRow3: [],
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
      use: [],
    };
  },
  methods: {
    init() {
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(75, 500 / 500, 0.1, 500);
      this.camera.position.set(6, 3, 5);
      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(300, 300);
      document
        .getElementById(this.Element)
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
      //this.createStack();
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
          this.use.push(group);
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
          this.use.push(group);
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
              this.size["SSP"][0],
              this.size["SSP"][2],
              this.size["SSP"][1]
            ),
            new THREE.MeshBasicMaterial({ map: crateTexture })
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
          this.use.push(group);
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
          );
          cubeB.position.y = 0 + this.size["MP"][0];
          cubeB.position.x = 0;
          cubeB.position.z = 0;
          cubeA.rotateY(1.5721);
          cubeB.rotateY(1.5721);
          const group = new THREE.Group();
          group.add(cubeA);
          group.add(cubeB);
          this.use.push(group);
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
          cubeA.rotateY(1.5721);
          cubeB.rotateY(1.5721);
          cubeC.rotateY(1.5721);
          const group = new THREE.Group();
          group.add(cubeA);
          group.add(cubeB);
          group.add(cubeC);
          this.use.push(group);
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
          this.use.push(group);
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
          this.use.push(group);
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
          this.use.push(group);
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
          this.use.push(group);
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
          this.use.push(group);
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
          this.use.push(group);
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
          this.use.push(group);
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
          this.use.push(group);
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
          this.use.push(group);
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
          this.use.push(group);
          this.scene.add(group);
          group.position.x = x;
          group.position.y = y;
          group.position.z = z;
          return group;
        }
      }
    },
    animate() {
      //this.renderer.setSize(store.getters.width, store.getters.height);
      this.renderer.render(this.scene, this.camera);
      this.controls.update();
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

      this.use.push(this.wall1);
      this.use.push(this.wall2);
      this.use.push(pointLight);
    },
    createStack() {
      //this.OtimalOutpus();
      console.log("create stack now");
      this.createWall();
      this.GeneratorContainer(this.Container_Type, 0, 0, 0);
      console.log(this.Container);
      for (let y = 0; y < this.Container.length; y++) {
        for (let j = 0; j < this.Container[y].length; j++) {
          if (j == 0) {
            this.boxsRow1.push(
              this.GeneratorStack(this.Container[y][j], 0, 0, 0)
            );
          } else if (j == 1) {
            this.boxsRow2.push(
              this.GeneratorStack(this.Container[y][j], 0, 0, 0)
            );
          } else {
            this.boxsRow3.push(
              this.GeneratorStack(this.Container[y][j], 0, 0, 0)
            );
          }
        }
      }
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
              }
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
          this.use.push(planeBottom);
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
          this.use.push(planeBottom);
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
          this.use.push(planeBottom);
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
          this.use.push(planeBottom);
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
          this.use.push(planeBottom);
          this.scene.add(planeBottom);
          break;
        }
      }
    },
  },
  created() {},
  mounted() {
    this.init();
    this.createWall();
    this.createStack();
    this.animate();
  },
  updated() {
    console.log("computed", this.update);
    // this.camera = null,
    // this.renderer = null,
    // this.controls = null,
    // this.wall1 = null,
    // this.wall2 = null,
    // this.boxsRow1 = [],
    // this.boxsRow2 = [],
    // this.boxsRow3 = []
    // this.init();

    console.log(this.scene.children);
    (this.boxsRow1 = []), (this.boxsRow2 = []), (this.boxsRow3 = []);
    for (const key in this.scene.children) {
      //this.scene.remove(this.scene.children[key])
      for (const value in this.use) {
        if (this.use[value] == this.scene.children[key]) {
          this.scene.remove(this.scene.children[key]);
        }
      }
    }
    this.createStack();
  },
  computed: {
    update() {
      console.log(this.Container);
      return this.Container;
    },
  },
};
</script>

<style scoped>
.full {
  width: 100%;
  height: 100%;
}

.item-a {
  display: inline-block;
  width: 70%;
}

.t1 {
  background-color: rgb(122, 158, 158);
}

.t2 {
  background-color: rgb(224, 173, 173);
}

.t3 {
  background-color: rgb(82, 73, 73);
}

.t4 {
  background-color: rgb(158, 153, 142);
}

.dot {
  height: 10px;
  width: 10px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
}

#setheight {
  height: 30%;
}
</style>