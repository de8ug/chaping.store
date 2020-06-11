import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentStep: 1,
    de8ugtoken: ''
  },
  mutations: {
    changeStep(state, value) {
      state.currentStep = value
    },
    addDe8ugToken(state, v){
      console.log('now token is:', v)
      state.de8ugtoken = v
    }
  },
  actions: {
    changeStep: ({commit}, value) => {
      commit('changeStep', value)
    }
  }
})
