<template>
  <div>
    <v-card elevation="2" outlined shaped class="grey lighten-5" id="pad">
      <v-container class="grey lighten-5">
        <v-item-group multiple>
          <v-container>
            <v-row justify="center" align="center">
              <v-col
                v-for="n in 5"
                :key="n"
                cols="12"
                md="4"
                sm="4"
                justify="center"
                align="center"
                @click="print(n)"
              >
                <v-btn color="accent" elevation="3" disabled block>{{
                  container[n - 1]
                }}</v-btn>
                <v-item v-slot="{ active, toggle }">
                  <v-card
                    :color="active ? 'primary' : ''"
                    class="d-flex align-center"
                    dark
                    height="200"
                    @click="toggle"
                  >
                    <v-scroll-y-transition hide-on-leave leave-absolute>
                      <div
                        v-if="active"
                        class="text-h1 flex-grow-1 text-center"
                      >
                        Selection
                      </div>
                      <v-img
                        class="black--text align-center"
                        aspect-ratio="3"
                        contain
                        src="@/assets/container.png"
                      >
                      </v-img>
                    </v-scroll-y-transition>
                  </v-card>
                </v-item>
              </v-col>
            </v-row>
          </v-container>
        </v-item-group> </v-container
    ></v-card>
  </div>
</template>

<script>
import store from "@/store";
export default {
  name: "ContainerComponents",
  data() {
    return {
      count: 1,
      length: 5895,
      width: 2350,
      height: 2392,
      container: [
        "20’STANDARD",
        "40’STANDARD",
        "40’HIGH-CUBE",
        "Small",
        "Large",
      ],
      containers: ["20Standard", "40Standard", "40HighCube", "Small", "Large"],
      useContainers: []
    };
  },
  methods: {
    increment() {
      this.count++;
    },
    decrement() {
      if (this.count > 0) {
        this.count--;
      }
    },
    print(n) {

      this.useContainers.push(this.containers[n-1])
      store.commit("setContainer", n - 1);
      if(store.getters.container[n-1]){
        console.log('')
      } else {
        this.useContainers = this.useContainers.filter(item => item !== this.containers[n-1])
      }
      this.useContainers = [...new Set(this.useContainers)]
      //console.log(this.useContainers = [...new Set(this.useContainers)])
      store.commit("saveContainer", this.useContainers)
    },
  },
};
</script>

<style scoped>
</style>