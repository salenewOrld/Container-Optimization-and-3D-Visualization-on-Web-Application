<template>
  <v-container class="grey lighten-5" >
    <v-row v-for="n in 2" :key="n">
      <v-col class="t1" cols="4" sm="4" md="4">
        <v-row justify="center" align="center">
          <model-components element="model" :width="500" :height="500"></model-components>
          <v-dialog
            transition="dialog-bottom-transition"
            hide-overlay
            v-model="dialog"
            width="80vw"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn class="btnSize" color="primary" v-bind="attrs" v-on="on">
                แสดงเต็มจอ
              </v-btn>
            </template>
            <v-card elevation="4" outlined height="80vh" width="80vw">
              <div id="fullmodel" justify="center" align="center">
                <model-components element="fullmodel" :width="getVW(79.5)" :height="getVH(79.5)"></model-components>
              </div>
            </v-card>
          </v-dialog>
        </v-row>
      </v-col>
      <v-col cols="8" sm="8" md="8">
        <v-row>
          <v-col class="t2" cols="6" sm="3" md="2">
            <p>Total</p>
          </v-col>
          <v-col class="t2" cols="6" sm="9" md="10">
            <p>{{ datas[0].totalAmount }} กล่อง</p>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="t3" cols="4" sm="4" md="4">
            <apexchart
              :options="datas[0].chartOptions"
              :series="datas[0].series[0].data"
              :color="datas[0].color"
            ></apexchart
          ></v-col>
          <v-col class="t4" cols="8" sm="8" md="8">
            <v-row
              v-for="(output, index) in outputs"
              :key="output"
              justify="center"
              align="center"
            >
              <v-col cols="4" sm="3" md="2">
                <span
                  v-if="index != 0"
                  class="dot"
                  :style="{ 'background-color': output[0] }"
                ></span>
                {{ output[1] }}
              </v-col>
              <v-col cols="4" sm="3" md="2">
                {{ output[2] }} <span v-if="index != 0">กล่อง</span>
              </v-col>
              <v-col cols="4" sm="3" md="2">
                {{ output[3] }} <span v-if="index != 0">ตารางเมตร</span></v-col
              >
              <v-col cols="4" sm="3" md="2">
                {{ output[4] }} <span v-if="index != 0">กิโลกรัม</span></v-col
              >
            </v-row>
          </v-col></v-row
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import apexchart from "vue-apexcharts";
import ModelComponents from "./ModelComponents.vue";
export default {
  name: "StuffingComponents",
  components: { apexchart, ModelComponents },
  data() {
    return {
      dialog: false,
      rotation: {
        x: -Math.PI / 2,
        y: 0,
        z: 0,
      },
      window: {
        width: 0,
        height: 0,
      },
      datas: [
        {
          maxArea: 32.43,
          useArea: 31.99,
          percentUse: 98.66,
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
          series: [
            {
              categories: [
                "BoxSmall_3",
                "BoxMedium_1",
                "BoxMedium_2",
                "BoxMedium_3",
                "FreeSpace",
              ],
              data: [10, 4, 1, 2],
            },
          ],
          totalAmount: 17,
          spacePerBox: [2.86, 2.28, 2.4, 2.66, 4.41],
        },
        {
          maxArea: 32.43,
          useArea: 30.95,
          percentUse: 95.45,
          chartOptions: {
            chart: {
              width: 300,
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
              "BoxSmall_1",
              "BoxSmall_2",
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
                "#ff0000",
                "#ff8000",
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
                    width: 200,
                  },
                },
              },
            ],
          },
          series: [
            {
              categories: [
                "BoxSmall_1",
                "BoxSmall_2",
                "BoxMedium_1",
                "BoxMedium_2",
                "BoxMedium_3",
                "BoxLarge_1",
                "BoxLarge_2",
                "BoxLarge_3",
                "FreeSpace",
              ],
              data: [1, 1, 1, 1, 1, 1, 1, 2],
            },
          ],
          totalAmount: 9,
          spacePerBox: [0.81, 1.01, 2.28, 2.24, 2.66, 4.41, 5.06, 12.32, 1.48],
        },
      ],
      dummy: {
        value: [],
        color: [],
        name: [],
        count: [],
        newCount: [],
      },
      outputs: [
        ["Color", "Name", "Package", "Volume", "Weight"],
        ["#ffff00", "BoxSmall_3", "10", 28.6, "20"],
        ["#80ff00", "BoxMedium_1", "4", 2.28*4, "20"],
        ["#00ffff", "BoxMedium_2", "1", 2.4*1, "30"],
        ["#0040ff", "BoxMedium_3", "2", 2.66*2, "40"],
      ],
    };
  },
  methods: {
    getVW(percent) {
      return (window.innerWidth * percent) / 100;
    },
    getVH(percent) {
      return (window.innerHeight * percent) / 100;
    },
    handleResize() {
      this.window.width = (window.innerWidth * 79) / 100;
      this.window.height = (window.innerHeight * 79) / 100;
      // console.log(this.window.width);
      // console.log(this.window.height);
    },
    setValue() {},
    adjustValue() {
      //console.log(this.dummy.value.length)
      this.series = [];
      this.chartOptions.fill.colors = [];
      this.chartOptions.labels = [];
      this.dummy.value = this.dummy.value.map(function (each_element) {
        return Number(each_element.toFixed(2));
      });
      for (let i = 0; i < this.dummy.value.length; i++) {
        if (this.dummy.value[i] != 0) {
          this.series.push(this.dummy.value[i]);
          this.chartOptions.fill.colors.push(this.dummy.color[i]);
          this.chartOptions.labels.push(this.dummy.name[i]);
          this.dummy.newCount.push(this.dummy.count[i]);
          //  console.log(this.dummy.value[i])
          //  console.log(this.dummy.color[i])
        }
      }
    },
  },
  created() {
    window.addEventListener("resize", this.handleResize);
    this.handleResize();
    //this.setValue();
    //this.adjustValue();
    //this.test = [this.container];
    console.log(this.datas[0].series[0].data);
  },
  destroyed() {
    window.removeEventListener("resize", this.handleResize);
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
</style>