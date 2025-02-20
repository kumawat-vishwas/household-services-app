<template>
  <div>
    <NavbarUser class="shadow-sm p-3 mb-5 rounded"  v-if="showNavbarUser" />

    <NavbarAdmin class="shadow-sm p-3 mb-5 rounded"  v-if="showNavbarAdmin" />

    <NavbarServiceProfessional class="shadow-sm p-3 mb-5 rounded"  v-if="showNavbarServiceProfessional" />

    <NavbarDefault class="shadow-sm p-3 mb-5 rounded" v-if="showNavbarDefault" />

    <!-- Main content -->
    <router-view />
  </div>
</template>
<script>
import NavbarUser from './components/NavbarUser.vue';
import NavbarAdmin from './components/NavbarAdmin.vue';
import NavbarServiceProfessional from './components/NavbarServiceProfessional.vue';
import NavbarDefault from './components/NavbarDefault.vue';

export default {
  components: {
    NavbarUser,
    NavbarAdmin,
    NavbarDefault,
    NavbarServiceProfessional,
  },
  computed: {
    showNavbarUser() {
      return this.$route.meta.showNavbarUser;
    },
    showNavbarAdmin() {
      return this.$route.meta.showNavbarAdmin;
    },
    showNavbarServiceProfessional() {
      return this.$route.meta.showNavbarServiceProfessional;
    },
    showNavbarDefault() {
      return !this.showNavbarUser && !this.showNavbarAdmin && !this.showNavbarServiceProfessional;
    },
  },
};

</script>
