<template>
  <div id="app">
    <v-app id="inspire">
      <v-card color="amber lighten-3">
        <v-card-title class="text-center justify-center py-6">
          <h1 class="font-weight-bold text-h2 basil--text">
            Container Loading
          </h1>
        </v-card-title>
        <v-tabs
          v-model="tab"
          background-color="amber lighten-3"
          color="basil"
          grow
        >
          <v-tab v-for="item in items" :key="item">
            {{ item }}
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item v-for="item in items" :key="item">
            <v-card color="basil" flat>
              <v-card-text v-if="item == 'PRODUCTS'">
                <products-c></products-c>
                <v-card
                  elevation="2"
                  outlined
                  shaped
                  class="red lighten-5"
                  id="pad"
                >
                  <v-container shaped outlined type="success">
                    <v-row justify="center" align="center">
                      <v-col
                        cols="4"
                        md="4"
                        sm="4"
                        justify="center"
                        align="center"
                      >
                        <v-btn color="primary" @click="tab = 1"> Next </v-btn>
                      </v-col></v-row
                    >
                  </v-container></v-card
                >
              </v-card-text>
              <v-card-text v-if="item == 'CONTAINERS'">
                <containers-components></containers-components>
                <v-card
                  elevation="2"
                  outlined
                  shaped
                  class="red lighten-5"
                  id="pad"
                >
                  <v-container shaped outlined type="success">
                    <v-row justify="center" align="center">
                      <v-col
                        cols="4"
                        md="4"
                        sm="4"
                        justify="center"
                        align="center"
                      >
                        <v-btn color="primary" id="pad" @click="tab = 0">
                          Back
                        </v-btn>
                        <v-btn color="primary" id="pad" @click="tab = 2">
                          Next
                        </v-btn>
                      </v-col></v-row
                    >
                  </v-container>
                </v-card>
              </v-card-text>
              <v-card-text v-if="item == 'STUFFING RESULT'" max-height="300">
                <stuffing-new></stuffing-new>
                <v-card
                  elevation="2"
                  outlined
                  shaped
                  class="red lighten-5"
                  id="pad"
                >
                  <v-container shaped outlined type="success">
                    <v-row justify="center" align="center">
                      <v-col
                        cols="4"
                        md="4"
                        sm="4"
                        justify="center"
                        align="center"
                      >
                        <v-btn color="primary" @click="tab = 1"> Back </v-btn>
                      </v-col></v-row
                    >
                  </v-container></v-card
                >
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-app>
  </div>
</template>

<script>
import ContainersComponents from "./components/ContainersComponents.vue";

import ProductsC from "./components/ProductsC.vue";
import StuffingNew from "./components/StuffingNew.vue";
export default {
  name: "App",

  components: {
    ContainersComponents,
    ProductsC,
    StuffingNew
},
  methods: {
    goProducts() {
      this.tab = "PRODUCTS";
    },
    goContainer() {
      this.tab = "CONTAINERS";
    },
    goStuffing() {
      this.tab = "STUFFING RESULT";
    },
  },
  data: () => ({
    tab: null,
    items: ["PRODUCTS", "CONTAINERS", "STUFFING RESULT"],
  }),
};
</script>

<style>
#pad {
  margin: 20px;
  padding: 20px;
}
</style>
