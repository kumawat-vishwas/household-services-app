<template>
    <div class="container">
        <div v-if="showBanner" class="d-flex banner" style="justify-content: center;">
            <div v-if="alertMessage" class="d-flex flex-row flex-wrap alert container bg-warning text-dark w-50"
                role="alert"
                style="position: fixed;bottom: 0px; z-index: 99999; justify-content: center; align-items: end;">
                <span v-for="value, key in alertMessage" class="mx-1" style="width: auto;gap: 16px">
                    <strong>{{ key }}:</strong> {{ value }};
                </span>
                <span type="button" class="position-absolute btn btn-link btn-sm text-dark"
                    @click="removeNotification()" style="right: 0; font-size: 1.2rem;"><i
                        class="bi bi-x-circle"></i></span>
            </div>
        </div>



        <form @submit.prevent="verify_admin">
            <!-- Login Form -->
            <h2 class="mb-4 mt-3 text-center">Login as Admin</h2>
            <div class="form-group">
                <label for="email">Email</label>
                <input v-model="loginForm.email" type="text" class="form-control" id="email" placeholder="Enter email">
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input v-model="loginForm.password" type="password" class="form-control" id="password"
                    placeholder="Enter password">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Login</button>
        </form>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'customerLoginModal',
    data() {
        return {
            showBanner: false,
            selectedService: null,
            loginForm: {
                email: '',
                password: '',
            },
            message: '',
            authToken : '',
        };
    },
    computed: {
        ...mapGetters(['alertMessage']),
    },
    async mounted() {
        await this.authTokenAssign();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        async verify_admin() {
            try {
                const response = await fetch(`http://localhost:8080/api/get_account_type/${this.loginForm.email}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    // body: JSON.stringify(this.loginForm.email),
                });
                if (!response.ok) {
                    // console.error('Login failed:', response.status, response.statusText);
                    const data = await response.json();
                    var alertMessage = {
                        "Notification": `${data}`,
                    };
                    this.$store.dispatch('updateAlertMessage', alertMessage);
                    this.showBannerFor3Seconds();
                    return;
                }
                const data = await response.json();
                // 
                if (data.type == 'admin') {
                    await this.login();
                } else {
                    var alertMessage = {
                        "Notification": "You are not an Admin",
                    };
                    this.$store.dispatch('updateAlertMessage', alertMessage);
                    this.showBannerFor3Seconds();
                }

            } catch (error) {
                console.error(error);
            }
        },
        async login() {
            try {
                const response = await fetch('http://localhost:8080/login?include_auth_token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.loginForm),
                });
                if (!response.ok) {
                    console.error('Login failed:', response.status, response.statusText);
                    return;
                }
                const data = await response.json();
                if (data && data.response && data.response.user && data.response.user.authentication_token) {
                    const token = data.response.user.authentication_token;
                    localStorage.setItem('authToken', token);
                    localStorage.setItem('user_type', "admin");
                    this.$store.dispatch('setAuthentication', true);
                    // await this.clearCache();
                    this.$router.push('/admin/dashboard');
                } else {
                    var alertMessage = {
                        "Notification": "Authentication token not found in the response.",
                    };
                    this.$store.dispatch('updateAlertMessage', alertMessage);
                    this.showBannerFor3Seconds();
                }

            } catch (error) {
                console.error(error);
            }
        },
        removeNotification() {
            const alertMessage = null;
            this.$store.dispatch('updateAlertMessage', alertMessage);
        },
        showBannerFor3Seconds() {
            this.showBanner = true;

            setTimeout(() => {
                this.showBanner = false;
                this.removeNotification()
            }, 3000);
        },


    },
};
</script>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: auto;
}
</style>