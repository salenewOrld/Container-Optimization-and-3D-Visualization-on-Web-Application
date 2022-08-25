<template>
  <div>
    <div>
      <v-container
        id="setheight"
        class="grey lighten-5"
        v-for="n in max"
        :key="n"
      >
        <v-row id="setheight">
          <v-col class="t1" cols="4" sm="4" md="4">
            <v-row justify="center" align="center">
              <ModelC :element="'id' + n" :width="380" :height="200" :index="n"></ModelC>
              <v-dialog
                transition="dialog-bottom-transition"
                hide-overlay
                v-model="dialog"
                width="80vw"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="btnSize"
                    color="primary"
                    v-bind="attrs"
                    v-on="on"
                  >
                    แสดงเต็มจอ
                  </v-btn>
                </template>
                <v-card elevation="4" outlined height="80vh" width="80vw">
                  <div :id="'id' + n" justify="center" align="center">
                    <modelC
                      :element="'idfull' + n"
                      :width="getVW(79.5)"
                      :height="getVH(79.5)"
                      :index="n"
                    ></modelC>
                  </div>
                </v-card>
              </v-dialog>
            </v-row>
          </v-col>
          <v-col cols="8" sm="8" md="8">
            <v-row>
              <v-col class="t2" cols="6" sm="3" md="2">
                <p>{{ $store.state.output[n-1][0].Container_Type }}</p>
              </v-col>
              <v-col class="t2" cols="6" sm="9" md="10">
                <p>ใช้พื้นที่ {{ $store.state.output[n-1][0].Area }} ตารางเมตร</p>
                <p>น้ำหนัก {{ $store.state.output[n-1][0].Weight }} กิโลกรัม</p>
              </v-col>
            </v-row>
            <v-row
              ><v-col class="t3" cols="4" sm="4" md="4">
                <apexchart
                  :options="chartOptions"
                  :series="data"
                ></apexchart> </v-col
              ><v-col class="t4" cols="8" sm="8" md="8">
                <v-row v-for="i in 14" :key="i"> {{ i }} กล่อง </v-row>
              </v-col></v-row
            >
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import apexchart from "vue-apexcharts";
import ModelC from "./ModelC.vue";
import store from "@/store";
import axios from "axios";
export default {
  name: "StuffingC",
  components: { ModelC, apexchart },
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
        labels: [
          "BoxSmall_3",
          "BoxMedium_1",
          "BoxMedium_2",
          "BoxMedium_3",
          "BoxLarge_1",
          "BoxLarge_2",
          "BoxLarge_3",
          "FreeSpace",
        ],
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
      data: [10, 4, 1, 2],
      window: {
        width: 0,
        height: 0,
      },
      max: 1,
      weight:0,
      area:0
    };
  },
  methods: {
    getVW(percent) {
      //console.log("width = " + (window.innerWidth * percent) / 100);
      return (window.innerWidth * percent) / 100;
    },
    getVH(percent) {
      //console.log("height = " + (window.innerHeight * percent) / 100);
      return (window.innerHeight * percent) / 100;
    },
    handleResize() {
      this.window.width = (window.innerWidth * 79) / 100;
      this.window.height = (window.innerHeight * 79) / 100;
      store.commit("setWidth", (this.$el.clientWidth * 4) / 13);
      store.commit("setHeight", (this.$el.clientWidth * 2.5) / 13);
      console.log(this.window.width);
      console.log(this.window.height);
    },
  },
  async created() {
    //Call API
    store.commit('ajustData')

    // console.log('amount = ',store.getters.data.HSSP.Amount)
    // console.log('weight = ',store.getters.data.HSSP.Weight[0])
    
    const response = await axios.post(
      "http://127.0.0.1:8000/test/getInformation",
      {
        HSSP: { Amount: store.getters.data.HSSP.Amount, Weights: [parseInt(store.getters.data.HSSP.Weight[0])] },
        SMP: { Amount: store.getters.data.SMP.Amount, Weights: [parseInt(store.getters.data.SMP.Weight[0])]  },
        SSP: { Amount: store.getters.data.SSP.Amount, Weights: [parseInt(store.getters.data.SSP.Weight[0])]  },
        MP: { Amount: store.getters.data.MP.Amount, Weights: [parseInt(store.getters.data.MP.Weight[0])] },
        MLP: { Amount: store.getters.data.MLP.Amount, Weights: [parseInt(store.getters.data.MLP.Weight[0])]  },
        LP: { Amount: store.getters.data.LP.Amount, Weights: [parseInt(store.getters.data.LP.Weight[0])]  },
        LHP: { Amount: store.getters.data.LHP.Amount, Weights: [parseInt(store.getters.data.LHP.Weight[0])]  },
        ETC: { Amount: store.getters.data.ETC.Amount, Weights: [parseInt(store.getters.data.ETC.Weight[0])]  },
        ContainerType: { Type: ['Small'] },
      }
    );
    store.commit("setOutput", response.data.Data.Container);
    store.commit('setload',true)
    console.log(response.data.Data.Container)
    //this.max = response.data.Data.Container.length-1

    //console.log(response.data.Container[0][0].Weight)
    //this.weight = response.data.Container[0][0].Weight
    //Set Size
    window.addEventListener("resize", this.handleResize);
    this.handleResize();
  },
  destroyed() {
    //Clear Size
    window.removeEventListener("resize", this.handleResize);
  },
  mounted() {
    store.commit("setWidth", (this.$el.clientWidth * 4) / 13);
    store.commit("setHeight", (this.$el.clientWidth * 2.5) / 13);
    //console.log(store.getters.width);
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