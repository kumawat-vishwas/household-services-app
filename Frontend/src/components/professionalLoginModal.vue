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



        <form v-if="loginMode" @submit.prevent="verify_professional">
            <!-- Login Form -->
            <h2 class="mb-4 mt-3 text-center">Login as Professional</h2>
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
            <h2 class="mb-4 mt-3 text-center">Register as Professional</h2>
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
                <label for="name">Service Name</label>
                <select v-model="userDetails.selectedService" class="form-select" aria-label="Default select example" required>
                    <option v-for="op in servicesAvailable">{{ op }}</option>
                </select>
            </div>
            <div class="form-group">
                <label for="name">Experience (in yrs)</label>
                <input v-model="userDetails.experience" type="text" class="form-control" id="experience"
                    placeholder="Enter your experience" required>
            </div>
            <div class="form-group">
                <label for="name">Attach Documents (Single PDF)</label>
                    <div class="form-group">
                        <label for="exampleFormControlFile1">Attach file</label>
                        <input type="file" id="fileInput" @change="handleFileUpload" required />
                    </div>
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
            selectedService: null,
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
                address: '',
                pincode: '',
                selectedService: '',
                experience: '',
                type: 'professional',
            },
            attachedFile: null,
            servicesAvailable: '',
            authToken : '',
        };
    },
    computed: {
        ...mapGetters(['alertMessage']),
    },
    async mounted() {
        await this.authTokenAssign();
        await this.getServicesAvailable();
        await this.clearCache();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        handleFileUpload(event) {
            this.attachedFile = event.target.files[0];
        },
        async verify_professional() {
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
                if (data.type == 'professional') {
                    await this.login();
                } else {
                    var alertMessage = {
                        "Notification": "You are not Service Professional",
                    };
                    this.$store.dispatch('updateAlertMessage', alertMessage);
                    this.showBannerFor3Seconds();
                }

            } catch (error) {
                console.error(error);
            }
        },
        async getServicesAvailable() {
            try {
                const response = await fetch(`http://localhost:8080/api/getServicesAvailable`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                if (!response.ok) {
                    const data = await response.json();
                    var alertMessage = {
                        "Notification": `${data}`,
                    };
                    this.$store.dispatch('updateAlertMessage', alertMessage);
                    this.showBannerFor3Seconds();
                    return;
                }
                const data = await response.json();
                this.servicesAvailable=data;

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
                    localStorage.setItem('user_type', "professional");
                    this.$store.dispatch('setAuthentication', true);
                    // await this.clearCache();
                    this.$router.push('/service-professional/dashboard');
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
                    await this.addUserRole();
                    
                    this.$router.push('/service-professional/dashboard');
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
        async addUserRole() {
            try {
                const role = 'professional';
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
            const formData = new FormData();
            formData.append('file', this.attachedFile);
            formData.append('email', this.registerForm.email);
            formData.append('name', this.userDetails.name);
            formData.append('address', this.userDetails.address);
            formData.append('pincode', this.userDetails.pincode);
            formData.append('selectedService', this.userDetails.selectedService);
            formData.append('experience', this.userDetails.experience);
            formData.append('type', this.userDetails.type);

            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];

            if (!file) {
                var alertMessage = {
                    "Notification": "No file selected",
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
                return;
            }
            const allowedExtension = 'pdf';
            const fileExtension = file.name.split('.').pop().toLowerCase();
            if (fileExtension !== allowedExtension) {
                var alertMessage = {
                    "Notification": "File should be pdf",
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
                return;
            }

            try {
                const response = await fetch('http://localhost:8080/api/registerProfessionalDetails', {
                    method: 'POST',
                    headers: {
                        'Authentication-Token': localStorage.getItem('authToken'),
                    },
                    body: formData,
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