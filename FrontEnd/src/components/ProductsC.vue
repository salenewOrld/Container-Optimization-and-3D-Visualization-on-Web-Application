<template>
  <div id="app">
    <v-data-table
      :headers="headers"
      :items="desserts"
      class="elevation-1"
      hide-default-footer
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="800px"
            max-height="800px"
            @click:outside="close"
          >
            <v-card>
              <v-card-title>
                <span class="text-h5"></span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="12" md="12">
                      <v-img
                        class="black--text align-center"
                        height="250"
                        :src="img.url[editedItem.name]"
                      >
                      </v-img></v-col
                  ></v-row>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.name"
                        readonly
                        label="Box Type"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.quantity"
                        label="Quantity (item)"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.weight"
                        label="Weight (k)"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">
                  Cancel
                </v-btn>
                <v-btn color="blue darken-1" text @click="save"> Save </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import store from "@/store";
export default {
  name: "ProductsC",
  data() {
    return {
      headers: [
        {
          text: "Box Type",
          align: "start",
          sortable: false,
          value: "name",
        },
        { text: "Width (m)", value: "width" },
        { text: "Length (m)", value: "length" },
        { text: "Height (m)", value: "height" },
        { text: "Quantity (item)", value: "quantity" },
        { text: "Weight (k)", value: "weight" },
        { text: "Actions", value: "actions", sortable: false },
      ],
      desserts: [],
      editedIndex: -1,
      editedItem: {
        name: "",
        calories: 0,
        fat: 0,
        carbs: 0,
        protein: 0,
      },
      defaultItem: {
        name: "",
        calories: 0,
        fat: 0,
        carbs: 0,
        protein: 0,
      },
      img: {
        url: {
          HSSP: require("@/assets/HSSP.png"),
          SMP: require("@/assets/SMP.png"),
          SSP: require("@/assets/SSP.png"),
          MP: require("@/assets/MP.png"),
          MLP: require("@/assets/MLP.png"),
          LHP: require("@/assets/LHP.png"),
          LP: require("@/assets/LP.png"),
          ETC: require("@/assets/ETC.png"),
        },
      },
            stack_info: {
        101: [0.76, 1.12, 1.09],
        102: [0.76, 1.12, 0.73],
        103: [0.76, 1.12, 0.54],
        104: [1.1, 1.8, 1.09],
        105: [1.1, 1.8, 0.73],
        106: [1.515, 2.22, 0.73],
        201: [0.76, 1.12, 2.17],
        202: [0.76, 2.24, 2.24],
        203: [0.76, 2.24, 2.24],
        204: [2.2, 1.5, 2.4],
        205: [2.28, 1.12, 2.18],
        206: [2.28, 1.12, 2.19],
        207: [1.515, 2.22, 2.31],
        208: [2.28, 1.12, 2.17],
      },
    };
  },
  methods: {
    initialize() {
      this.desserts = [
        {
          name: "HSSP",
          width: 0.76,
          length: 1.12,
          height: 1.09,
          quantity: 0,
          weight: 0,
        },
        {
          name: "SMP",
          width: 0.76,
          length: 1.12,
          height: 0.73,
          quantity: 0,
          weight: 0,
        },
        {
          name: "SSP",
          width: 0.76,
          length: 1.12,
          height: 0.54,
          quantity: 0,
          weight: 0,
        },
        {
          name: "MP",
          width: 1.1,
          length: 1.8,
          height: 1.09,
          quantity: 0,
          weight: 0,
        },
        {
          name: "MLP",
          width: 1.1,
          length: 1.8,
          height: 0.73,
          quantity: 0,
          weight: 0,
        },
        {
          name: "LHP",
          width: 1.1515,
          length: 2.22,
          height: 0.85,
          quantity: 0,
          weight: 0,
        },
        {
          name: "LP",
          width: 1.1515,
          length: 2.22,
          height: 0.73,
          quantity: 0,
          weight: 0,
        },
        {
          name: "ETC",
          width: 1.1,
          length: 1.15,
          height: 1.5,
          quantity: 0,
          weight: 0,
        },
      ];
    },
    editItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.desserts.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
        store.commit("setinputs", this.desserts);
        //console.log(store.getters.inputs);
      } else {
        this.desserts.push(this.editedItem);
      }
      this.close();
    },
  },
  created() {
    this.initialize();
  },
};
</script>

<style scoped>
</style>