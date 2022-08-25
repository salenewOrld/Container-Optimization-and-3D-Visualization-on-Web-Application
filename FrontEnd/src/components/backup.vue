<template>
  <v-row justify="center" align="center" v-for="i in container.length" :key="i">
    <v-col cols="12" sm="8" md="6" justify="center" align="center">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="12" md="12" justify="center" align="center">
          <v-btn color="accent" elevation="3" rounded disabled block>
            {{ container[i - 1] }}
          </v-btn></v-col
        >
      </v-row>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="12" md="12" justify="center" align="center">
          <v-img
            class="black--text align-center"
            height="125px"
            width="125px"
            src="@/assets/container.png"
          >
          </v-img
        ></v-col>
      </v-row>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="12" md="12" justify="center" align="center">
          <v-btn color="accent" elevation="3" rounded block>
            Infomation Container
          </v-btn></v-col
        >
      </v-row>
    </v-col>
  </v-row>
  <v-col cols="10" sm="10" md="10" justify="center" align="center">
    <v-row no-gutters>
      <v-col cols="4" sm="4" md="4" justify="center" align="center">
        <p>จำนวนตู้</p>
      </v-col>
      <v-col cols="2" sm="2" md="2" justify="center" align="center">
        <p>กว้าง</p>
      </v-col>
      <v-col cols="2" sm="2" md="2" justify="center" align="center">
        <p>ยาว</p>
      </v-col>
      <v-col cols="2" sm="2" md="2" justify="center" align="center">
        <p>สูง</p>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="1" sm="1" md="1" justify="right" align="right">
        <v-btn color="primary" elevation="2" icon @click="decrement">
          <v-icon dark> mdi-minus </v-icon></v-btn
        >
      </v-col>
      <v-col cols="2" sm="2" md="2" justify="center" align="center">
        <v-btn color="accent" elevation="3" rounded disabled block>
          {{ count }}
        </v-btn>
        <!-- <v-text-field label="จำนวน" solo v-model="count"></v-text-field> -->
      </v-col>
      <v-col cols="1" sm="1" md="1" justify="left" align="left">
        <v-btn color="primary" elevation="2" icon @click="increment">
          <v-icon dark> mdi-plus </v-icon></v-btn
        >
      </v-col>
      <v-col cols="2" sm="2" md="2" justify="center" align="center">
        <v-btn color="accent" elevation="3" rounded disabled block>
          {{ length }}
        </v-btn>
      </v-col>
      <v-col cols="2" sm="2" md="2" justify="center" align="center">
        <v-btn color="accent" elevation="3" rounded disabled block>
          {{ width }}
        </v-btn>
      </v-col>
      <v-col cols="2" sm="2" md="2" justify="center" align="center">
        <v-btn color="accent" elevation="3" rounded disabled block>
          {{ height }}
        </v-btn>
      </v-col>
    </v-row>
  </v-col>

</template>
UI คำนวนเก่า
    <v-row justify="center" align="center">
      <v-col cols="12" sm="6" md="4" justify="center" align="center">
        <v-btn color="accent" elevation="3" rounded disabled block>
          20 STANDARD
        </v-btn>
        <v-img
          class="black--text align-center"
          height="125px"
          width="125px"
          src="@/assets/container.png"
        >
        </v-img>
        <v-btn color="accent" elevation="3" rounded disabled block>
          จำนวน {{ datas.length }} ตู้
        </v-btn>
      </v-col>
    </v-row>
    <v-row justify="center" align="center" v-for="i in datas.length" :key="i">
      <v-col cols="4" sm="4" md="4" justify="center" align="center">
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
          <v-card elevation="4" outlined height="80vh" width="80vw"> </v-card>
        </v-dialog>
      </v-col>
      <v-col cols="8" sm="8" md="8" justify="center" align="center">
        <v-row no-gutters>
          <v-col cols="4" sm="4" md="4" justify="center" align="center">
            <v-card class="mx-auto item-a" max-width="900">
              <apexchart
                :options="datas[i - 1].chartOptions"
                :series="datas[i - 1].series[0].data"
                :color="datas[i - 1].color"
              ></apexchart>
            </v-card>
          </v-col>
          <v-col cols="8" sm="8" md="8" justify="center" align="center">
            <v-card class="mx-auto" max-width="900">
              <v-row align="center">
                <v-col>
                  <p>
                    ใช้พื้นที่ทั้งหมด
                    {{ datas[i - 1].percentUse }}
                    %
                  </p>
                  <p>
                    ใช้กล่องทั้งหมดทั้งหมด
                    {{ datas[i - 1].totalAmount }} กล่อง
                  </p>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="12"
                      md="12"
                      v-for="n in datas[i - 1].series[0].categories.length - 1"
                      :key="n"
                    >
                      {{ datas[i - 1].series[0].categories[n - 1] }} จำนวน
                      {{ datas[i - 1].series[0].data[n - 1] }} กล่อง
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
