<template>
  <div id="container">asdasd</div>
</template>

<script>
// import { ref } from "vue";
import * as THREE from "three";
import  OrbitControls from "three-orbit-controls";
// import { OrbitControls } from "https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/controls/OrbitControls.js";
var object = [];
var scene = null;
var camera = null;
var renderer = null;
var controls = null;
let color =[0xff00ff , 0xffff00 , 0x00ffff, 0xf0f0f0 ,0xB5EE70];
let color2 =[0xB5EE70, 0xff00ff, 0xffff00 , 0x00ffff, 0xf0f0f0];
let color3 =[0x000000 ,  0xf0f0f0 , 0xff00ff, 0xB5EE70, 0x00ffff,];
let use = color;
function changecolor() {
  console.log('change color')
  if (use == color) {
    use = color2
  } else if (use == color2) {
    use = color3
  } else {
    use = color
  }
}
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

  // const geometry = new THREE.BoxGeometry(0.8075, 0.8075, 0.8075);
  // const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
  // const cube = new THREE.Mesh(geometry, material);
  // cube.position.x = -2;
  // object.push(cube);
  // scene.add(cube);
  // let y = -1.45;
  // let z = 2.45;
  let x = 0.68;
  for (let index = 0; index < 2; index++) {
    // แนวกว้าง
     let z = 2.45;
      let y = -1.45;
   for (let index = 0; index < 2; index++) {
    // แนวสูง
    for (let index = 0; index < 5; index++) {
      // แนวยาว
      const cube = new THREE.Mesh(
        new THREE.BoxGeometry(1.012, 1.012, 1.012),
        new THREE.MeshBasicMaterial({ color: use[index] })
      )
      cube.position.y = y;
      cube.position.x = x;
      cube.position.z = z;  
      object.push(cube);
      scene.add(cube);
      // z = z - 1.012
      z -= 1.012
    }
    y += 1.012
    z = 2.45
    changecolor()
    }
    x -= 1.012   
  }


  // const cube2 = new THREE.Mesh(
  //   new THREE.BoxGeometry(1.012, 1.012, 1.012),
  //   new THREE.MeshBasicMaterial({ color: 0xff00ff })
  // )
  // cube2.position.y = -1.45+1.012;
  // cube2.position.x = 0.68;
  // cube2.position.z = 2.45;
  // object.push(cube2);
  // scene.add(cube2);

  // const cube1 = new THREE.Mesh(
  //   new THREE.BoxGeometry(1.012, 1.012, 1.012),
  //   new THREE.MeshBasicMaterial({ color: 0x00ff00 })
  // )
  // cube1.position.y = -1.45;
  // cube1.position.x = 0.68;
  // cube1.position.z = 2.45-1.012;
  // object.push(cube1);
  // scene.add(cube1);

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
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
