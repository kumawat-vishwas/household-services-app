import { createStore } from 'vuex';

const store = createStore({
  state: {
    isAuthenticated: false,
    alertMessage: null,
    userProfile: null,
    authToken: localStorage.getItem('authToken') || null, // Initialize with localStorage value if available
  },
  mutations: {
    setAuthentication(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
    setAlertMessage(state, alertMessage) {
      state.alertMessage = alertMessage;
    },
    setUserProfile(state, userProfile) {
      state.userProfile = userProfile;
    },
    clearAlertMessage(state) {
      state.alertMessage = null;
    },
    setSearchQuery(state, query) {
      state.searchQuery = query;
    },
    setUserRole(state, role) {
      state.userRole = role;
    },
    setAuthToken(state, token) {
      state.authToken = token;
      state.isAuthenticated = !!token; 
    },
    // clearAuthToken(state) {
    //   state.authToken = null;
    // },
  },
  actions: {
    async logout() {
      try {
        const response = await fetch('http://localhost:8080/api/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.$store.getters.authToken}`, 
          },
        });

        if (response.ok) {
          localStorage.removeItem('authToken');
          this.$store.dispatch('setAuthentication', false);

          this.$router.push('/');
        } else {
          console.error('Logout failed:', response.statusText);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    updateSearchDetails({ commit }, payload) {
      commit('setSearchQuery', payload.searchQuery);
    },
    updateUserRole({ commit }, payload) {
      commit('setUserRole', payload.userRole);
    },
    updateAlertMessage({ commit }, alertMessage) {
      commit('setAlertMessage', alertMessage);
    },
    clearAuthToken({ commit }, authToken) {
      commit('setAuthToken', authToken);
    },
    updateUserProfile({ commit }, userProfile) {
      commit('setUserProfile', userProfile);
    },
    setAuthFromLocalStorage({ commit }) {
      const token = localStorage.getItem('authToken');
      if (token) {
        commit('setAuthToken', token); 
      }
    },
    setAuthentication({ commit }, isAuthenticated) {
      commit('setAuthentication', isAuthenticated);
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    authToken: () => localStorage.getItem('authToken'),
    selectedShow: (state) => state.selectedShow,
    alertMessage: (state) => state.alertMessage,
    profileData: (state) => state.userProfile,
    additionalData: (state) => state.additionalData,
  },
});



export default store;
