import { createStore } from 'vuex'

export default createStore({
  state: {
    token: null,
    username: null,
  },
  mutations: {
    setToken(state, token) {
      state.token = token
    },
    setUsername(state, username) {
      state.username = username
    }
  },
  actions: {
    login({ commit }, { token, username }) {
      commit('setToken', token)
      commit('setUsername', username)
    }
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
})
