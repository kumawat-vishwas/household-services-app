
<template>
  <div v-if="user_type === 'customer' & authToken != 'null'">
    <div class="container d-flex m-auto">
      <div class="card w-100 py-3 loginOption" @click="customerDashboard()">
        <div class="card-body m-auto">
          <h5 class="card-title>">You are already logged in as Customer. Click here to go to dashboard</h5>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="user_type === 'professional' & authToken != 'null'">
    <div class="container d-flex m-auto">
      <div class="card w-100 py-3 loginOption" @click="professionalDashboard()">
        <div class="card-body m-auto">
          <h5 class="card-title>">You are already logged in as Professional. Click here to go to dashboard</h5>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="user_type === 'admin' & authToken != 'null'">
    <div class="container d-flex m-auto">
      <div class="card w-100 py-3 loginOption" @click="adminDashboard()">
        <div class="card-body m-auto">
          <h5 class="card-title>">You are already logged in as Admin. Click here to go to dashboard</h5>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="container d-flex m-auto">
      <div class="card w-100 py-3 loginOption" @click="showCustomerLoginPopup()">
        <div class="card-body m-auto">
          <h5 class="card-title>">Continue as User</h5>
        </div>
      </div>
      <div class="card w-100 py-3 loginOption" @click="showServiceProfessionalLoginPopup()">
        <div class="card-body m-auto">
          <h5 class="card-title>">Continue as Service Professional</h5>
        </div>
      </div>
      <div class="card w-100 py-3 loginOption" @click="showAdminLoginPopup()">
        <div class="card-body m-auto">
          <h5 class="card-title>">Continue as Admin</h5>
        </div>
      </div>
    </div>
  </div>


  <!-- Customer Login -->
  <div v-if="showCustomerLogin" class="modal-overlay" @click.self="hidePopup">
    <div class="modal-content scrollbar-primary w-75">
      <span class="close-btn" @click="hidePopup">&times;</span>
      <customerLoginModal />
    </div>
  </div>
  
  <!-- Professional Login-->
  <div v-if="showServiceProfessionalLogin" class="modal-overlay" @click.self="hidePopup">
    <div class="modal-content scrollbar-primary w-75">
      <span class="close-btn" @click="hidePopup">&times;</span>
      <professionalLoginModal />
    </div>
  </div>
  
  <!-- Admin Login-->
  <div v-if="showAdminLogin" class="modal-overlay" @click.self="hidePopup">
    <div class="modal-content scrollbar-primary w-75">
      <span class="close-btn" @click="hidePopup">&times;</span>
      <adminLoginModal />
    </div>
  </div>



</template>

<script>
import { mapGetters } from 'vuex';
import customerLoginModal from './customerLoginModal.vue';
import professionalLoginModal from './professionalLoginModal.vue';
import adminLoginModal from './adminLoginModal.vue';


export default {

  name: 'indexPage',
  data() {
    return {
      showCustomerLogin: false,
      showServiceProfessionalLogin: false,
      showAdminLogin: false,
      user_type: null,
      authToken : '',
    };
  },
  components: {
    customerLoginModal,
    professionalLoginModal,
    adminLoginModal,
  },
  computed: {
    ...mapGetters(['profileData']),
  },
  async mounted() {
    await this.authTokenAssign();
    await this.checkUserType();
  },
  methods: {
    async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
    async checkUserType() {
      this.user_type = localStorage.getItem('user_type');
    }
    ,
    customerDashboard(){
      this.$router.push('/user/dashboard');
    },
    professionalDashboard(){
      this.$router.push('/service-professional/dashboard');
    },
    adminDashboard(){
      this.$router.push('/admin/dashboard');
    },
    showCustomerLoginPopup() {
      this.showCustomerLogin = true;
      this.showServiceProfessionalLogin = false;
      this.showAdminLogin = false;
    },
    hidePopup() {
      this.showCustomerLogin = false;
      this.showServiceProfessionalLogin = false;
      this.showAdminLogin = false;
    },
    showServiceProfessionalLoginPopup() {
      this.showCustomerLogin = false;
      this.showServiceProfessionalLogin = true;
      this.showAdminLogin = false;
    },
    showAdminLoginPopup() {
      this.showCustomerLogin = false;
      this.showServiceProfessionalLogin = false;
      this.showAdminLogin = true;
    },

  },
}
</script>

<style scoped>
.loginOption:hover {
  background-color: #ffffd1;
  /* border: none; */
  /* margin-right: 10px;
  margin-left: 10px; */
  width: 150% !important;
  cursor: pointer;
}
.container{
  align-items: normal !important;
}
</style>
