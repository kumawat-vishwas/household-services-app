<template>
    <nav class="navbar border-bottom mb-3 navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <router-link to="/admin/dashboard" class="navbar-brand bold" style="margin: 0px;">
                Welcome to Admin Dashboard
            </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <router-link to="/admin/dashboard" class="nav-link"><p class="bi bi-house"><span class="mx-1">Home</span></p></router-link>
                    <router-link to="/admin/summary" class="nav-link"><p class="bi bi-graph-up"><span class="mx-1">Summary</span></p></router-link>
                    <router-link @click="logout()" to="#" class="nav-link"><p class="bi bi-box-arrow-right"><span class="mx-1">Logout</span></p></router-link>
                </div>
            </div>
        </div>
    </nav>
</template>
<script>
import { mapGetters, mapState } from 'vuex';

export default {
    name: 'navbarCreator',
    data() {
        return {
            authToken : '',
        };
    },
    computed: {
        ...mapGetters(['profileData']),
    },
    async mounted() {
        await this.authTokenAssign();
        await this.checkUserPermission();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        async checkUserPermission() {
            try {
                if (this.authToken) {
                    const response = await fetch('http://localhost:8080/api/checkUserPermission', {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authentication-Token': this.authToken,
                        },
                    });

                    if (!response.ok) {
                        return;
                    }

                    const data = await response.json();
                    if (data !== 'Admin') {
                        if (data === 'Professional') {
                            this.$router.push('/service-professional/dashboard');
                        } else if (data === 'Customer') {
                            this.$router.push('/user/dashboard');
                        }
                    }
                }
            } catch (error) {
                var alertMessage = {
                    "Alert": 'An error occurred, Professionals fetching failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
            }
        },
        async logout() {
            try {
                const response = await fetch('http://localhost:8080/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                });

                if (response.ok) {
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('user_type');
                    this.$store.dispatch('setAuthentication', false);
                    await this.clearCache();
                    this.$router.push('/');
                } else {
                    console.error('Logout failed:', response.statusText);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },
        async clearCache(){
            try{
                const response= await fetch('http://localhost:8080/api/clearCache',{
                    method:'POST',
                    headers:{
                      'content-type':'application/json'
                    }
                })
                const data = await response.json()
                
                if (response.ok){
                    
                }else{
                    console.error("error")
                }
            }catch(error){
                
            }
        },
    },
};
</script>
<style scoped>
.navbar-nav{
    margin-left: auto;
}
.bold{
    font-weight: 700;
}
.border-bottom{
    border-bottom: var(--bs-border-width) var(--bs-border-style) #dee2e64f !important;
}
.nav-link{
    color: #000;
}
.nav-link:hover, .nav-link:focus {
    color: #494949;
}
</style>