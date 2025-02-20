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



        <form v-if="loginMode" @submit.prevent="verify_customer">
            <!-- Login Form -->
            <h2 class="mb-4 mt-3 text-center">Login as Customer</h2>
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
            <p class="mt-3 text-center">Don't have an account? <a @click="toggleMode" class="text-primary">Register</a>
            </p>
        </form>
        <form v-else @submit.prevent="register">
            <!-- Registration Form -->
            <h2 class="mb-4 mt-3 text-center">User: Register</h2>
            <div class="form-group">
                <label for="name">Name</label>
                <input v-model="userDetails.name" type="text" class="form-control" id="name"
                    placeholder="Enter your name" required>
            </div>
            <div class="form-group">
                <label for="newEmail">Email</label>
                <input v-model="registerForm.email" type="text" class="form-control" id="newEmail"
                    placeholder="Enter new email" required>
            </div>
            <div class="form-group">
                <label for="newPassword">Password</label>
                <input v-model="registerForm.password" type="password" class="form-control" id="newPassword"
                    placeholder="Enter new password " required>
            </div>
            <div class="form-group">
                <label for="address">Address</label>
                <input v-model="userDetails.address" type="text" class="form-control" id="address"
                    placeholder="Enter new address" required>
            </div>
            <div class="form-group">
                <label for="pincode">Pincode</label>
                <input v-model="userDetails.pincode" type="text" class="form-control" id="pincode"
                    placeholder="Enter new pincode" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Register</button>
            <p class="mt-3 text-center">Already have an account? <a @click="toggleMode" class="text-primary">Login</a>
            </p>
        </form>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'customerLoginModal',
    data() {
        return {
            loginMode: true,
            showBanner: false,
            loginForm: {
                email: '',
                password: '',
            },
            message: '',
            registerForm: {
                email: '',
                password: '',
            },
            userDetails: {
                email: '',
                name: '',
                address:'',
                pincode:'',
                type: 'customer',
                authToken : '',
            },
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
        async verify_customer() {
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
                if (data.type == 'customer'){
                    await this.login();
                } else {
                    var alertMessage = {
                        "Notification": "You are not customer",
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
                    localStorage.setItem('user_type', "customer");
                    this.$store.dispatch('setAuthentication', true);
                    // await this.clearCache();
                    this.$router.push('/user/dashboard');
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
        async register() {
            try {
                const response = await fetch('http://localhost:8080/register?include_auth_token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.registerForm),
                });
                if (!response.ok) {
                    console.error('Login failed:', response.status, response.statusText);
                    return;
                }
                const data = await response.json();
                if (data && data.response && data.response.user && data.response.user.authentication_token) {
                    const token = data.response.user.authentication_token;
                    localStorage.setItem('authToken', token);
                    localStorage.setItem('user_type', "customer");
                    this.$store.dispatch('setAuthentication', true);
                    // await this.clearCache();
                    await this.userRole();
                    
                    this.$router.push('/user/dashboard');
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
        async userRole() {
            try {
                const role = 'customer';
                const response = await fetch('http://localhost:8080/api/addUserRole', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('authToken'),
                    },
                    body: JSON.stringify(role),
                });
                if (!response.ok) {
                    console.error('Login failed:', response.status, response.statusText);
                    return;
                }
                const data = await response.json();
                
                await this.addUserDetails();
            } catch (error) {
                console.error(error);
            }
        },
        async addUserDetails() {
            try {
                this.userDetails.email = this.registerForm.email;
                const response = await fetch('http://localhost:8080/api/registerCustomerDetails', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('authToken'),
                    },
                    body: JSON.stringify(this.userDetails),
                });
                if (!response.ok) {
                    console.error('Login failed:', response.status, response.statusText);
                    return;
                }
                const data = await response.json();
                
            } catch (error) {
                console.error(error);
            }
        },
        toggleMode() {
            this.loginMode = !this.loginMode;
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