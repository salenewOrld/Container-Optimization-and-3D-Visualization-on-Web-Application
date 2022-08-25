<template>
  <v-card>
    <v-dialog
      v-model="isloading"
      hide-overlay
      persistent
      full-width
      height-width
      @click:outside="isloading = true"
    >
      <v-card height="80vh">
        <v-container fluid fill-height class="cyan lighten-1">
          <v-layout
            column
            no-gutters
            style="width: 100%"
            justify-center
            align-center
          >
            <v-flex xs2>
              <h1 class="font-weight-bold text-h2 basil--text">
                Process Genetic
              </h1>
            </v-flex>
            <v-flex xs2>
              <v-progress-circular
                indeterminate
                color="deep-orange darken-1"
                width="10"
                size="100"
              >
              </v-progress-circular>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-dialog>
    <v-progress-linear
      :active="scoketcolse"
      :indeterminate="scoketcolse"
      absolute
      bottom
      color="deep-purple accent-4"
      height="10"
    ></v-progress-linear>
    <div v-if="!isloading" class="text-center">
      <div v-for="(item, index) in historyList" :key="index">
        <StuffingContent
          v-bind:Element="'element' + page"
          :Container_Type="item.Container_Type"
          :Container="item.Container"
          :Weight="item.Weight"
          :Area="item.Area"
          :ContainerData="item.ContainerData"
          :BoxName="item.BoxName"
        ></StuffingContent>
      </div>
      <v-pagination
        class="pagination mb-2"
        v-model="page"
        :length="pages"
        @input="updatePage"
      ></v-pagination>
    </div>
  </v-card>
</template>
<script>
import store from "@/store";
// import store from "@/store";
// import axios from "axios";
import StuffingContent from "./StuffingContent.vue";
export default {
  name: "StuffingNew",
  data() {
    return {
      scoketcolse: true,
      isloading: true,
      window: {
        width: 0,
        height: 0,
      },
      weight: 0,
      area: 0,
      page: 1,
      pageSize: 1,
      list: [],
      listCount: 0,
      historyList: [],
      stack_info: {
        101: 0.76,
        102: 0.76,
        103: 0.76,
        104: 1.1,
        105: 1.1,
        106: 1.515,
        201: 0.76,
        202: 0.76,
        203: 0.76,
        204: 2.2,
        205: 2.28,
        206: 2.28,
        207: 1.515,
        208: 2.28,
        0: 0,
      },
    };
  },
  methods: {
    handleResize() {
      this.window.width = (window.innerWidth * 79) / 100;
      this.window.height = (window.innerHeight * 79) / 100;
      // store.commit("setWidth", (this.$el.clientWidth * 4) / 13);
      // store.commit("setHeight", (this.$el.clientWidth * 2.5) / 13);
      console.log(this.window.width);
      console.log(this.window.height);
    },
    initPage() {
      let _this = this;
      _this.listCount = _this.list.length;
      if (_this.listCount < _this.pageSize) {
        _this.historyList = _this.list;
      } else {
        _this.historyList = _this.list.slice(0, _this.pageSize);
      }
    },
    updatePage(pageIndex) {
      let _this = this;
      let _start = (pageIndex - 1) * _this.pageSize;
      let _end = pageIndex * _this.pageSize;
      _this.historyList = _this.list.slice(_start, _end);
      _this.page = pageIndex;
      console.log("Current Page = " + _this.page);
    },
    addlist(data) {
      // console.log('ก่อน re',data.ArrangementPattern)
      // console.log('หลัง re',this.rearrange(data.ArrangementPattern))
      const upper = data.TotalParcelsUsageName.map((element) => {
        return element.toUpperCase();
      });
      this.list.push({
        Container_Type: data.ContainerType,
        Container: this.rearrange(data.ArrangementPattern),
        Weight: data.ContainerTotalWeight.toFixed(2),
        Area: data.ContainerTotalArea.toFixed(2),
        ContainerData: data.TotalParcelsUsageAmount,
        BoxName: upper,
      });
      this.initPage();
      //console.log('asdasd = asd asd= ',this.list)
    },
    async socket() {
      const vue = this;
      let ContainerIndex = 0;
      console.log({
        Parcels: {
          ssp: store.getters.data.SSP.Amount,
          smp: store.getters.data.SMP.Amount,
          hssp: store.getters.data.HSSP.Amount,
          mlp: store.getters.data.MLP.Amount,
          mp: store.getters.data.MP.Amount,
          lp: store.getters.data.LP.Amount,
          lhp: store.getters.data.LHP.Amount,
          etc: store.getters.data.ETC.Amount,
        },
        ParcelsWeight: {
          ssp: [parseInt(store.getters.data.SSP.Weight[0])],
          smp: [parseInt(store.getters.data.SMP.Weight[0])],
          hssp: [parseInt(store.getters.data.HSSP.Weight[0])],
          mlp: [parseInt(store.getters.data.MLP.Weight[0])],
          mp: [parseInt(store.getters.data.MP.Weight[0])],
          lp: [parseInt(store.getters.data.LP.Weight[0])],
          lhp: [parseInt(store.getters.data.LHP.Weight[0])],
          etc: [parseInt(store.getters.data.ETC.Weight[0])],
        },
      });
      this.connection = await new WebSocket("ws://127.0.0.1:8000/ws");
      let containerType = this.containerType();
      console.log("sfnew ", containerType);
      this.connection.onopen = function () {
        console.log("websockets is connect.");
        this.send(
          JSON.stringify({
            Parcels: {
              ssp: store.getters.data.SSP.Amount,
              smp: store.getters.data.SMP.Amount,
              hssp: store.getters.data.HSSP.Amount,
              mlp: store.getters.data.MLP.Amount,
              mp: store.getters.data.MP.Amount,
              lp: store.getters.data.LP.Amount,
              lhp: store.getters.data.LHP.Amount,
              etc: store.getters.data.ETC.Amount,
            },
            ParcelsWeight: {
              ssp: [parseInt(store.getters.data.SSP.Weight[0])],
              smp: [parseInt(store.getters.data.SMP.Weight[0])],
              hssp: [parseInt(store.getters.data.HSSP.Weight[0])],
              mlp: [parseInt(store.getters.data.MLP.Weight[0])],
              mp: [parseInt(store.getters.data.MP.Weight[0])],
              lp: [parseInt(store.getters.data.LP.Weight[0])],
              lhp: [parseInt(store.getters.data.LHP.Weight[0])],
              etc: [parseInt(store.getters.data.ETC.Weight[0])],
            },
            ContainersType: containerType,
            Status: 0,
            ContainerIndex: ContainerIndex,
          })
        );
      };
      this.connection.onmessage = function (event) {
        vue.isloading = false;
        console.log("websockets is message.");
        const data = JSON.parse(event.data);
        console.log("data = ", data);
        if (data.Status == 1) {
          vue.addlist(data);
        }
        if (data.ContainerIndex + 1 == containerType.length) {
          data.ContainerIndex = 0;
        } else {
          data.ContainerIndex += 1;
        }
        this.send(
          JSON.stringify({ Status: 1, ContainerIndex: data.ContainerIndex })
        );
      };
      this.connection.onclose = function () {
        console.log("websockets is close.");
        vue.scoketcolse = false;
      };
      this.connection.onerror = function (event) {
        console.log("websockets is error.");
        console.log(event);
      };
    },
    containerType() {
      let use;
      //console.log("data form store con =", store.getters.containers);
      if (store.getters.containers.length > 0) {
        use = store.getters.containers;
      } else {
        use = store.getters.autoContainer;
      }
      //console.log("data from use use,", use);
      return use;
    },
    otimal(ArrangementPattern) {
      const maxRow = 2.37;
      const minRow = 2;
      let ConvertPattern = JSON.parse(JSON.stringify(ArrangementPattern));
      let OtimalPattern = JSON.parse(JSON.stringify(ArrangementPattern));

      for (let i = 0; i < ArrangementPattern.length; i++) {
        for (let y = 0; y < ArrangementPattern[i].length; y++) {
          ConvertPattern[i][y] = this.stack_info[ArrangementPattern[i][y]];
        }
      }

      for (let i = 0; i < ConvertPattern.length; i++) {
        let hasValue = 0;
        for (let x = 0; x < ConvertPattern[i].length; x++) {
          hasValue = hasValue + ConvertPattern[i][x];
        }
        if (hasValue > minRow && hasValue < maxRow) {
          console.log("แถว ", i, " เต็มเรียบร้อยแล้ว");
        } else {
          console.log("แถว ", i, " ยังว่างอยู่แล้ว");
          for (let z = i + 1; z < ConvertPattern.length; z++) {
            for (let y = 0; y < ConvertPattern[z].length; y++) {
              if (hasValue + ConvertPattern[z][y] < maxRow) {
                let temp1 = ConvertPattern[z][y];
                let temp2 = OtimalPattern[z][y];
                ConvertPattern[z][y] = 0;
                OtimalPattern[z][y] = 0;
                for (const value in ConvertPattern[i]) {
                  if (ConvertPattern[i][value] == 0) {
                    ConvertPattern[i][value] = temp1;
                    OtimalPattern[i][value] = temp2;
                    temp1 = 0;
                    temp2 = 0;
                  }
                }
              }
            }
          }
        }
      }

      for (let i = 0; i < OtimalPattern.length; i++) {
        for (let x = 0; x < OtimalPattern[i].length; x++) {
          if (OtimalPattern[i][x] == 0 && x !== 2) {
            let temp3 = OtimalPattern[i][x];
            OtimalPattern[i][x] = OtimalPattern[i][x + 1];
            OtimalPattern[i][x + 1] = temp3;
          }
        }
      }
      console.log("oti = ", OtimalPattern);
      return OtimalPattern;
    },
    rearrange(container) {
      for (let i = 0; i < container.length - 1; i++) {
        let sumWidth =
          this.stack_info[container[i][0]] +
          this.stack_info[container[i][1]] +
          this.stack_info[container[i][2]];
        if (sumWidth < 2) {
          for (let n = 0; n < 3; n++) {
            if (container[i][n] == 0) {
              for (let k = i + 1; k < container.length; k++) {
                for (let j = 0; j < 3; j++) {
                  if (
                    container[k][j] != 0 &&
                    this.stack_info[container[k][j]] + sumWidth < 2.37
                  ) {
                    sumWidth += this.stack_info[container[k][j]];
                    let temp = container[i][n];
                    container[i][n] = container[k][j];
                    container[k][j] = temp;
                    n += 1;
                  }
                }
              }
            }
          }
        }
      }
      for (let y = 0; y < 3; y++) {
        for (let i = 0; i < container.length; i++) {
          for (let x = 0; x < container[i].length; x++) {
            if (container[i][x] == 0 && x !== 2) {
              let temp3 = container[i][x];
              container[i][x] = container[i][x + 1];
              container[i][x + 1] = temp3;
            }
          }
        }
      }
      return container;
    },
  },
  created() {
    let _this = this;
    _this.initPage();
    _this.updatePage(_this.page);

    window.addEventListener("resize", this.handleResize);
    this.handleResize();
  },
  mounted() {
    this.socket();
  },
  computed: {
    pages() {
      let _this = this;
      if (_this.pageSize == null || _this.listCount == null) return 0;
      return Math.ceil(_this.listCount / _this.pageSize);
    },
  },
  components: { StuffingContent },
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

.container {
  width: 100%;
  position: relative;
  overflow: hidden;
}

a {
  text-decoration: none;
}

h1.main,
p.demos {
  -webkit-animation-delay: 18s;
  -moz-animation-delay: 18s;
  -ms-animation-delay: 18s;
  animation-delay: 18s;
}

.sp-container {
  position: fixed;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  z-index: 0;
  background: -webkit-radial-gradient(
    rgba(0, 0, 0, 0.1),
    rgba(0, 0, 0, 0.3) 35%,
    rgba(0, 0, 0, 0.7)
  );
  background: -moz-radial-gradient(
    rgba(0, 0, 0, 0.1),
    rgba(0, 0, 0, 0.3) 35%,
    rgba(0, 0, 0, 0.7)
  );
  background: -ms-radial-gradient(
    rgba(0, 0, 0, 0.1),
    rgba(0, 0, 0, 0.3) 35%,
    rgba(0, 0, 0, 0.7)
  );
  background: radial-gradient(
    rgba(0, 0, 0, 0.1),
    rgba(0, 0, 0, 0.3) 35%,
    rgba(0, 0, 0, 0.7)
  );
}

.sp-content {
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0px;
  top: 0px;
  z-index: 1000;
}

.sp-container h2 {
  position: absolute;
  top: 50%;
  line-height: 100px;
  height: 90px;
  margin-top: -50px;
  font-size: 90px;
  width: 100%;
  text-align: center;
  color: transparent;
  -webkit-animation: blurFadeInOut 3s ease-in backwards;
  -moz-animation: blurFadeInOut 3s ease-in backwards;
  -ms-animation: blurFadeInOut 3s ease-in backwards;
  animation: blurFadeInOut 3s ease-in backwards;
}

.sp-container h2.frame-1 {
  -webkit-animation-delay: 0s;
  -moz-animation-delay: 0s;
  -ms-animation-delay: 0s;
  animation-delay: 0s;
}

.sp-container h2.frame-2 {
  -webkit-animation-delay: 3s;
  -moz-animation-delay: 3s;
  -ms-animation-delay: 3s;
  animation-delay: 3s;
}

.sp-container h2.frame-3 {
  -webkit-animation-delay: 6s;
  -moz-animation-delay: 6s;
  -ms-animation-delay: 6s;
  animation-delay: 6s;
}

.sp-container h2.frame-4 {
  font-size: 200px;
  -webkit-animation-delay: 9s;
  -moz-animation-delay: 9s;
  -ms-animation-delay: 9s;
  animation-delay: 9s;
}

.sp-container h2.frame-5 {
  -webkit-animation: none;
  -moz-animation: none;
  -ms-animation: none;
  animation: none;
  color: transparent;
  text-shadow: 0px 0px 1px #fff;
}

.sp-container h2.frame-5 span {
  -webkit-animation: blurFadeIn 3s ease-in 12s backwards;
  -moz-animation: blurFadeIn 1s ease-in 12s backwards;
  -ms-animation: blurFadeIn 3s ease-in 12s backwards;
  animation: blurFadeIn 3s ease-in 12s backwards;
  color: transparent;
  text-shadow: 0px 0px 1px #fff;
}

.sp-container h2.frame-5 span:nth-child(2) {
  -webkit-animation-delay: 13s;
  -moz-animation-delay: 13s;
  -ms-animation-delay: 13s;
  animation-delay: 13s;
}

.sp-container h2.frame-5 span:nth-child(3) {
  -webkit-animation-delay: 14s;
  -moz-animation-delay: 14s;
  -ms-animation-delay: 14s;
  animation-delay: 14s;
}

.sp-globe {
  position: absolute;
  width: 282px;
  height: 273px;
  left: 50%;
  top: 50%;
  margin: -137px 0 0 -141px;
  background: transparent url(http://web-sonick.zz.mu/images/sl/globe.png)
    no-repeat top left;
  -webkit-animation: fadeInBack 3.6s linear 14s backwards;
  -moz-animation: fadeInBack 3.6s linear 14s backwards;
  -ms-animation: fadeInBack 3.6s linear 14s backwards;
  animation: fadeInBack 3.6s linear 14s backwards;
  -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=30)";
  filter: alpha(opacity=30);
  opacity: 0.3;
  -webkit-transform: scale(5);
  -moz-transform: scale(5);
  -o-transform: scale(5);
  -ms-transform: scale(5);
  transform: scale(5);
}

.sp-circle-link {
  position: absolute;
  left: 50%;
  bottom: 100px;
  margin-left: -50px;
  text-align: center;
  line-height: 100px;
  width: 100px;
  height: 100px;
  background: #fff;
  color: #3f1616;
  font-size: 25px;
  -webkit-border-radius: 50%;
  -moz-border-radius: 50%;
  border-radius: 50%;
  -webkit-animation: fadeInRotate 1s linear 16s backwards;
  -moz-animation: fadeInRotate 1s linear 16s backwards;
  -ms-animation: fadeInRotate 1s linear 16s backwards;
  animation: fadeInRotate 1s linear 16s backwards;
  -webkit-transform: scale(1) rotate(0deg);
  -moz-transform: scale(1) rotate(0deg);
  -o-transform: scale(1) rotate(0deg);
  -ms-transform: scale(1) rotate(0deg);
  transform: scale(1) rotate(0deg);
}

.sp-circle-link:hover {
  background: #85373b;
  color: #fff;
}

/**/

@-webkit-keyframes blurFadeInOut {
  0% {
    opacity: 0;
    text-shadow: 0px 0px 40px #fff;
    -webkit-transform: scale(1.3);
  }

  20%,
  75% {
    opacity: 1;
    text-shadow: 0px 0px 1px #fff;
    -webkit-transform: scale(1);
  }

  100% {
    opacity: 0;
    text-shadow: 0px 0px 50px #fff;
    -webkit-transform: scale(0);
  }
}

@-webkit-keyframes blurFadeIn {
  0% {
    opacity: 0;
    text-shadow: 0px 0px 40px #fff;
    -webkit-transform: scale(1.3);
  }

  50% {
    opacity: 0.5;
    text-shadow: 0px 0px 10px #fff;
    -webkit-transform: scale(1.1);
  }

  100% {
    opacity: 1;
    text-shadow: 0px 0px 1px #fff;
    -webkit-transform: scale(1);
  }
}

@-webkit-keyframes fadeInBack {
  0% {
    opacity: 0;
    -webkit-transform: scale(0);
  }

  50% {
    opacity: 0.4;
    -webkit-transform: scale(2);
  }

  100% {
    opacity: 0.2;
    -webkit-transform: scale(5);
  }
}

@-webkit-keyframes fadeInRotate {
  0% {
    opacity: 0;
    -webkit-transform: scale(0) rotate(360deg);
  }

  100% {
    opacity: 1;
    -webkit-transform: scale(1) rotate(0deg);
  }
}

/**/

@-moz-keyframes blurFadeInOut {
  0% {
    opacity: 0;
    text-shadow: 0px 0px 40px #fff;
    -moz-transform: scale(1.3);
  }

  20%,
  75% {
    opacity: 1;
    text-shadow: 0px 0px 1px #fff;
    -moz-transform: scale(1);
  }

  100% {
    opacity: 0;
    text-shadow: 0px 0px 50px #fff;
    -moz-transform: scale(0);
  }
}

@-moz-keyframes blurFadeIn {
  0% {
    opacity: 0;
    text-shadow: 0px 0px 40px #fff;
    -moz-transform: scale(1.3);
  }

  100% {
    opacity: 1;
    text-shadow: 0px 0px 1px #fff;
    -moz-transform: scale(1);
  }
}

@-moz-keyframes fadeInBack {
  0% {
    opacity: 0;
    -moz-transform: scale(0);
  }

  50% {
    opacity: 0.4;
    -moz-transform: scale(2);
  }

  100% {
    opacity: 0.2;
    -moz-transform: scale(5);
  }
}

@-moz-keyframes fadeInRotate {
  0% {
    opacity: 0;
    -moz-transform: scale(0) rotate(360deg);
  }

  100% {
    opacity: 1;
    -moz-transform: scale(1) rotate(0deg);
  }
}

/**/

@keyframes blurFadeInOut {
  0% {
    opacity: 0;
    text-shadow: 0px 0px 40px #fff;
    transform: scale(1.3);
  }

  20%,
  75% {
    opacity: 1;
    text-shadow: 0px 0px 1px #fff;
    transform: scale(1);
  }

  100% {
    opacity: 0;
    text-shadow: 0px 0px 50px #fff;
    transform: scale(0);
  }
}

@keyframes blurFadeIn {
  0% {
    opacity: 0;
    text-shadow: 0px 0px 40px #fff;
    transform: scale(1.3);
  }

  50% {
    opacity: 0.5;
    text-shadow: 0px 0px 10px #fff;
    transform: scale(1.1);
  }

  100% {
    opacity: 1;
    text-shadow: 0px 0px 1px #fff;
    transform: scale(1);
  }
}

@keyframes fadeInBack {
  0% {
    opacity: 0;
    transform: scale(0);
  }

  50% {
    opacity: 0.4;
    transform: scale(2);
  }

  100% {
    opacity: 0.2;
    transform: scale(5);
  }
}

@keyframes fadeInRotate {
  0% {
    opacity: 0;
    transform: scale(0) rotate(360deg);
  }

  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}
</style>