<script>
// import { ref } from "vue";
import * as THREE from "three";
import { OrbitControls } from "https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/controls/OrbitControls.js";
var object = [];
var scene = null;
var camera = null;
var renderer = null;
var controls = null;

function init() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );

  camera.position.set(5, 0, 0);
  // camera.position.set(6, 3, 5);

  renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  //   document.getElementById('app').appendChild(renderer.domElement);

  //   console.log(document.getElementById("app"));

  const geometry = new THREE.BoxGeometry(0.8075, 0.8075, 0.8075);
  const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
  const cube = new THREE.Mesh(geometry, material);
  cube.position.x = -2;
  object.push(cube);
  scene.add(cube);

  const cube2 = new THREE.Mesh(
    new THREE.BoxGeometry(1.012, 1.012, 1.012),
    new THREE.MeshBasicMaterial({ color: 0xff00ff })
  );
  cube2.position.y = -1.45 + 1.012;
  cube2.position.x = 0.68;
  cube2.position.z = 2.45;
  object.push(cube2);
  scene.add(cube2);

  const cube1 = new THREE.Mesh(
    new THREE.BoxGeometry(1.012, 1.012, 1.012),
    new THREE.MeshBasicMaterial({ color: 0x00ff00 })
  );
  cube1.position.y = -1.45;
  cube1.position.x = 0.68;
  cube1.position.z = 2.45;
  object.push(cube1);
  scene.add(cube1);

  const plane = new THREE.Mesh(
    new THREE.BoxGeometry(0.1, 2.35, 5.895),
    new THREE.MeshBasicMaterial({
      color: 0xffff00,
      side: THREE.DoubleSide,
    })
  );
  plane.position.y = -2;
  plane.rotation.z = 1.571;
  object.push(plane);
  scene.add(plane);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.minDistance = 0;
  controls.maxDistance = Infinity;

  controls.enableZoom = true; // Set to false to disable zooming
  controls.zoomSpeed = 1.0;

  controls.enablePan = true; // Set to false to disable panning (ie vertical and horizontal translations)

  controls.enableDamping = true; // Set to false to disable damping (ie inertia)
  controls.dampingFactor = 0.25;
  controls.update();
  Tutor();
}
function animate() {
  requestAnimationFrame(animate);
  for (let index = 0; index < object.length; index++) {
    // object[index].rotation.z += 0.01;
    // object[index].rotation.y += 0.01;
  }
  controls.update();
  renderer.render(scene, camera);
}
async function Tutor() {
  for (let i = 0; i < 5; i++) {
    console.log(camera.position);
    await sleep(3000);
  }
}
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
init();
animate();

function OtimalOutpus() {
  const maxRow = 2.37;
  const minRow = 2;
  console.log("usecase = ", store.getters.output[this.index - 1][0].Container);

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
}
</script>

<template>
  <div id="container">asdasd</div>
</template>

<style scoped>
a {
  color: #42b983;
}
</style>
