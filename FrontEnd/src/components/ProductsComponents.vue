<template>
  <div>
    <v-card elevation="2" outlined shaped class="grey lighten-5" id='pad'>
      <v-container>
        <v-row
          no-gutters
          justify="center"
          align="center"
          v-for="(input, index) in inputs"
          :key="input"
        >
          <v-col>
            <v-btn color="accent" elevation="3" rounded disabled block>
              {{ input.name }}
            </v-btn>
          </v-col>
          <v-col>
            <v-btn color="accent" elevation="3" rounded disabled block>
              {{ input.length }}
            </v-btn>
          </v-col>
          <v-col>
            <v-btn color="accent" elevation="3" rounded disabled block>
              {{ input.width }}
            </v-btn>
          </v-col>
          <v-col>
            <v-btn color="accent" elevation="3" rounded disabled block>
              {{ input.height }}
            </v-btn>
          </v-col>
          <v-col>
            <v-btn color="accent" elevation="3" rounded disabled block>
              {{ input.weight }}
            </v-btn>
          </v-col>
          <v-col>
            <v-btn color="accent" elevation="3" rounded disabled block>
              {{ input.quantity }}
            </v-btn>
          </v-col>
          <v-col>
            <v-btn
              rounded
              block
              v-bind:style="{ backgroundColor: input.color, important }"
            >
              สี{{ input.color }}
            </v-btn>
          </v-col>

          <v-col>
            <v-btn
              color="accent"
              elevation="3"
              rounded
              block
              @click="deleteRow(index)"
            >
              Delete
            </v-btn>
          </v-col>
        </v-row>
        <v-row> </v-row>
        <v-row justify="center" align="center">
          <v-col cols="4" md="4" sm="4" justify="center" align="center">
            <!-- <v-btn color="accent" elevation="3" rounded @click="addRow">
          Add row
        </v-btn> -->
            <v-dialog transition="dialog-bottom-transition" max-width="1200">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" v-bind="attrs" v-on="on">
                  เพิ่มกล่องสินค้า
                </v-btn>
              </template>
              <template v-slot:default="dialog">
                <v-card>
                  <v-toolbar color="primary" dark>เพิ่มกล่องสินค้า </v-toolbar>
                  <v-item-group>
                    <v-container>
                      <v-row>
                        <v-col
                          v-for="n in 8"
                          :key="n"
                          cols="4"
                          md="4"
                          sm="4"
                          @click="test(n)"
                        >
                          <v-item v-slot="{ active, toggle }">
                            <v-card
                              :color="active ? 'primary' : ''"
                              class="d-flex align-center"
                              dark
                              height="150"
                              @click="toggle"
                            >
                              <v-scroll-y-transition
                                hide-on-leave
                                leave-absolute
                              >
                                <div
                                  v-if="active"
                                  class="text-h1 flex-grow-1 text-center"
                                >
                                  Select
                                </div>
                                <v-img
                                  class="black--text align-center"
                                  height="150"
                                  :src="img.url[n - 1]"
                                >
                                </v-img>
                              </v-scroll-y-transition>
                            </v-card>
                          </v-item>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-item-group>
                  <v-form>
                    <v-container>
                      <v-row>
                        <v-col
                          cols="4"
                          sm="4"
                          md="4"
                          justify="center"
                          align="center"
                        >
                          <v-text-field
                            label="Width"
                            solo
                            v-model="width[select]"
                            disabled
                          ></v-text-field>
                        </v-col>

                        <v-col
                          cols="4"
                          sm="4"
                          md="4"
                          justify="center"
                          align="center"
                        >
                          <v-text-field
                            label="Length"
                            solo
                            v-model="length[select]"
                            disabled
                          ></v-text-field>
                        </v-col>

                        <v-col
                          cols="4"
                          sm="4"
                          md="4"
                          justify="center"
                          align="center"
                        >
                          <v-text-field
                            label="Height"
                            solo
                            v-model="height[select]"
                            disabled
                          ></v-text-field>
                        </v-col>
                        <v-col
                          cols="4"
                          sm="4"
                          md="4"
                          justify="center"
                          align="center"
                        >
                          <v-text-field
                            label="ชื่อสินค้า"
                            solo
                            v-model="names[select]"
                            disabled
                          ></v-text-field>
                        </v-col>

                        <v-col
                          cols="4"
                          sm="4"
                          md="4"
                          justify="center"
                          align="center"
                        >
                          <v-text-field
                            label="จำนวน"
                            solo
                            v-model="quantity"
                            v-on:keypress="NumbersOnly"
                          ></v-text-field>
                        </v-col>

                        <v-col
                          cols="4"
                          sm="4"
                          md="4"
                          justify="center"
                          align="center"
                        >
                          <v-text-field
                            label="น้ำหนัก"
                            solo
                            v-model="weight"
                            v-on:keypress="NumbersOnly"
                          ></v-text-field>
                        </v-col>

                        <v-col
                          cols="12"
                          sm="12"
                          md="12"
                          justify="center"
                          align="center"
                        >
                          <v-dialog
                            transition="dialog-bottom-transition"
                            max-width="400"
                            max-height="650"
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-btn
                                class="btnSize"
                                color="primary"
                                v-bind="attrs"
                                v-on="on"
                              >
                                เลือกสีกล่องสินค้า
                              </v-btn>
                            </template>
                            <template v-slot:default="dialog">
                              <v-card>
                                <v-toolbar color="primary" dark
                                  >เลือกสี
                                </v-toolbar>
                                <v-container>
                                  <v-row justify="space-around" align="center">
                                    <v-color-picker
                                      class="ma-2"
                                      hide-sliders
                                      hide-inputs
                                      hide-canvas
                                      show-swatches
                                      v-model="color"
                                    ></v-color-picker>
                                  </v-row>
                                  <v-row justify="space-around" align="center">
                                    <v-sheet dark class="pa-4">
                                      <pre>{{ color }}</pre>
                                    </v-sheet>
                                  </v-row>
                                  <v-row>
                                    <v-card-actions class="justify-end">
                                      <v-btn text @click="setColor(dialog)"
                                        >เลือกสี</v-btn
                                      >
                                    </v-card-actions>
                                  </v-row>
                                </v-container>
                              </v-card>
                            </template>
                          </v-dialog>
                          <div v-bind:style="{ backgroundColor: color }">
                            สีปัจจุบัน
                          </div>
                          <!-- <v-text-field label="สี" solo></v-text-field> -->
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-form>
                  <v-card-actions class="justify-end">
                    <v-btn text @click="addRow(dialog)">เพิ่มสินค้า</v-btn>
                  </v-card-actions>
                </v-card>
              </template>
            </v-dialog>
          </v-col>
        </v-row>
      </v-container></v-card
    ><v-spacer></v-spacer>

  </div>
</template>

<script>
import store from '../store'
export default {
  name: "ProductsComponents",
  data() {
    return {
      width: [0, 0.76, 0.76, 0.76, 1.1, 1.1, 1.1515, 1.1515, 1.1515],
      length: [0, 1.12, 1.12, 1.12, 1.8, 1.8, 2.22, 2.22, 1.5],
      height: [0, 1.09, 0.73, 0.54, 1.09, 0.73, 0.85, 0.73, 2.24],
      names:['HSSP','SMP','SSP','MP','MLP','LHP','LP','ETC'],
      select: 0,
      inputs: [],
      name: "",
      quantity: "",
      weight: "",
      color: "#673AB7",
      img: {
        url: [
          require("@/assets/HSSP.png"),
          require("@/assets/SMP.png"),
          require("@/assets/SSP.png"),
          require("@/assets/MP.png"),
          require("@/assets/MLP.png"),
          require("@/assets/LHP.png"),
          require("@/assets/LP.png"),
          require("@/assets/ETC.png"),
        ],
      },
    };
  },
  methods: {
    NumbersOnly(evt) {
      evt = evt ? evt : window.event;
      var charCode = evt.which ? evt.which : evt.keyCode;
      if (
        charCode > 31 &&
        (charCode < 48 || charCode > 57) &&
        charCode !== 46
      ) {
        evt.preventDefault();
      } else {
        return true;
      }
    },
    test(i) {
      // console.log(i)
      this.select = i;
    },
    addRow(dialog) {
      dialog.value = false;
      const vue = this;
      this.inputs.push({
        name: vue.name,
        quantity: vue.quantity,
        weight: vue.weight,
        color: vue.color,
        length: vue.length[vue.select],
        width: vue.width[vue.select],
        height: vue.height[vue.select],
      });
      store.commit('setinputs',this.inputs)
    },
    deleteRow(index) {
      this.inputs.splice(index, 1);
      console.log(this.img.url[0]);
    },
    setColor(dialog) {
      dialog.value = false;
    },
  },
};
</script>

<style scoped>
.col {
  margin-top: 15px;
  margin-left: 10px;
  margin-right: 10px;
}
.btnSize {
  display: flex;
  flex-direction: column;
  height: auto;
  flex-grow: 1;
  flex-wrap: wrap;
  min-width: 0;
  width: 100%;
}
</style>