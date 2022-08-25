import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    AR: 0,
    WT: 0,
    api_get: 'http://127.0.0.1:8000/test/getInformation',
    inputs: null,
    //[20Standard,40Standard,40HighCube,Small,Large]
    container: [false, false, false, false, false],
    autoContainer: ['20Standard'],
    useContainer: [],
    containers: [],
    width: 0,
    height: 0,
    output: [[{ Area: 0, Weight: 0 ,Container_Type:'Unknow'}]],
    load: false,
    // MP: [1.1, 1.8, 1.09],
    // LHP: [1.515, 2.22, 0.85],
    // LP: [1.515, 2.22, 0.73],
    // HSSP: [0.76, 1.12, 1.09],
    // ETC: [1.1, 1.5, 1.55],
    // MLP: [1.1, 1.8, 0.73],
    // SSP: [0.76, 1.12, 0.54],
    // SMP: [0.76, 1.12, 0.73],
    data: {
      Boxes: {
        MP: {
          Amount: 0,
          Weight: []
        },
        LHP: {
          Amount: 0,
          Weight: []
        },
        LP: {
          Amount: 0,
          Weight: []
        },
        HSSP: {
          Amount: 100,
          Weight: [50]
        },
        ETC: {
          Amount: 0,
          Weight: []
        },
        MLP: {
          Amount: 0,
          Weight: []
        },
        SSP: {
          Amount: 0,
          Weight: []
        },
        SMP: {
          Amount: 0,
          Weight: []
        }
      }
    }
  },
  getters: {
    inputs: state => state.inputs,
    width: state => state.width,
    height: state => state.height,
    container: state => state.container,
    containers: state => state.containers,
    api_get: state => state.api_get,
    data: state => state.data.Boxes,
    output: state => state.output,
    AR: state => state.AR,
    WT: state => state.WT,
    load: state => state.load,
    autoContainer: state => state.autoContainer
  },
  mutations: {
    setload: (state, load) => {
      state.load = load
    },
    setinputs: (state, inputs) => {
      console.log('asdsadasdasd as',parseInt(inputs[0].weight))
      state.inputs = inputs
      state.data.Boxes.HSSP.Amount = parseInt(inputs[0].quantity)
      state.data.Boxes.HSSP.Weight = [parseInt(inputs[0].weight)]
      state.data.Boxes.SMP.Amount = parseInt(inputs[1].quantity)
      state.data.Boxes.SMP.Weight = [parseInt(inputs[1].weight)]
      state.data.Boxes.SSP.Amount = parseInt(inputs[2].quantity)
      state.data.Boxes.SSP.Weight = [parseInt(inputs[2].weight)]
      state.data.Boxes.MP.Amount = parseInt(inputs[3].quantity)
      state.data.Boxes.MP.Weight = [parseInt(inputs[3].weight)]
      state.data.Boxes.MLP.Amount = parseInt(inputs[4].quantity)
      state.data.Boxes.MLP.Weight = [parseInt(inputs[4].weight)]
      state.data.Boxes.LHP.Amount = parseInt(inputs[5].quantity)
      state.data.Boxes.LHP.Weight = [parseInt(inputs[5].weight)]
      state.data.Boxes.LP.Amount = parseInt(inputs[6].quantity)
      state.data.Boxes.LP.Weight = [parseInt(inputs[6].weight)]
      state.data.Boxes.ETC.Amount = parseInt(inputs[7].quantity)
      state.data.Boxes.ETC.Weight = [parseInt(inputs[7].weight)]
      //console.log(state.data.Boxes.MP.Weight)
    },
    setOutput: (state, output) => {
      state.output = output
    },
    setWidth: (state, width) => {
      state.width = width
    },
    setHeight: (state, height) => {
      state.height = height
    },
    setContainer: (state, container) => {
      state.container[container] = state.container[container] ? false : true
    },
    saveContainer: (state, containers) => {
      state.containers = (containers)
    },
    ajustData: (state) => {
      for (const key in state.inputs) {
        //console.log(state.inputs[key].quantity)
        switch (state.inputs[key].name) {
          case 'MP':
            state.data.Boxes.MP.Amount = (state.inputs[key].quantity)
            state.data.Boxes.MP.Weight[0] = (state.inputs[key].weight)
            break;
          case 'LHP':
            state.data.Boxes.LHP.Amount = (state.inputs[key].quantity)
            state.data.Boxes.LHP.Weight[0] = (state.inputs[key].weight)
            break
          case 'LP':
            state.data.Boxes.LP.Amount = (state.inputs[key].quantity)
            state.data.Boxes.LP.Weight[0] = (state.inputs[key].weight)
            break;
          case 'HSSP':
            state.data.Boxes.HSSP.Amount = (state.inputs[key].quantity)
            state.data.Boxes.HSSP.Weight[0] = (state.inputs[key].weight)
            break
          case 'ETC':
            state.data.Boxes.ETC.Amount = (state.inputs[key].quantity)
            state.data.Boxes.ETC.Weight[0] = (state.inputs[key].weight)
            break;
          case 'MLP':
            state.data.Boxes.MLP.Amount = (state.inputs[key].quantity)
            state.data.Boxes.MLP.Weight[0] = (state.inputs[key].weight)
            break
          case 'SSP':
            state.data.Boxes.SSP.Amount = (state.inputs[key].quantity)
            state.data.Boxes.SSP.Weight[0] = (state.inputs[key].weight)
            break;
          case 'SMP':
            state.data.Boxes.SMP.Amount = (state.inputs[key].quantity)
            state.data.Boxes.SMP.Weight[0] = (state.inputs[key].weight)
            break
        }
      }
      // state.data.Boxes.MP.Amount = state.data.Boxes.MP.Weight.length
      // state.data.Boxes.LHP.Amount = state.data.Boxes.LHP.Weight.length
      // state.data.Boxes.LP.Amount = state.data.Boxes.LP.Weight.length
      // state.data.Boxes.HSSP.Amount = state.data.Boxes.HSSP.Weight.length
      // state.data.Boxes.ETC.Amount = state.data.Boxes.ETC.Weight.length
      // state.data.Boxes.MLP.Amount = state.data.Boxes.MLP.Weight.length
      // state.data.Boxes.SSP.Amount = state.data.Boxes.ETC.Weight.length
      // state.data.Boxes.SMP.Amount = state.data.Boxes.MLP.Weight.length

    }
  },
  actions: {
  },
  modules: {
  }
})
