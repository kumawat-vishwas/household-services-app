<template>
    <nav class="navbar border-bottom mb-3 navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <router-link to="/" class="navbar-brand">
                <p class="bold" style="margin: 0px;">Household Services App</p>
            </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <router-link to="/" class="nav-link active" aria-current="page">
                        <p class="bi bi-house"><span class="mx-1">Home</span></p>
                    </router-link>
                    <router-link v-if="authToken" to="#" @click="logout()" class="nav-link">
                        <p class="bi bi-box-arrow-right"><span class="mx-1">Logout</span></p>
                    </router-link>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
import { mapGetters } from 'vuex';

export default {

    name: 'Navbar',
    data() {
        return {
            authToken : '',
        };
    },

    async mounted() {
        await this.authTokenAssign();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        async logout() {
            try {
                const response = await fetch('http://localhost:8080/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('user_type');
                    this.$store.dispatch('setAuthentication', false);
                    this.$store.dispatch('clearAuthToken', null);
                    await this.clearCache();
                    this.$router.push('/');
                } else {
                    console.error('Logout failed:', response.statusText);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },
        async clearCache() {
            try {
                const response = await fetch('http://localhost:8080/api/clearCache', {
                    method: 'POST',
                    headers: {
                        'content-type': 'application/json'
                    }
                })
                const data = await response.json()
                
                if (response.ok) {
                    
                } else {
                    console.error("error")
                }
            } catch (error) {
                
            }
        },
     
    },
}
</script>

<style scoped>
.navbar-nav {
    margin-left: auto;
}

.bold {
    font-weight: 700;
}

.navbar {
    --bs-navbar-color: #f2fff9 !important;
}

/* .navbar-brand,
.navbar-nav .show>.nav-link,
.navbar-nav .nav-link.active {
    color: #f2fff9 !important;
} */

.border-bottom {
    border-bottom: var(--bs-border-width) var(--bs-border-style) #dee2e64f !important;
}

.nav-link{
    color: #000;
}
.nav-link:hover, .nav-link:focus {
    color: #494949;
}
</style>