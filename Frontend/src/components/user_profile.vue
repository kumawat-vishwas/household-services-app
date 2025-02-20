<template>
    <div class="container">
        <div class="jumbotron">

            <h2>My Profile</h2>
            <p style="font-size: 1rem;">Account related informations.</p>
        </div>

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

        <div v-if="editMode" class="container card w-85 mt-1 p-4">
            <form @submit.prevent="updateUserData()">
                <div class="form-group">
                    <label for="name">Name</label>
                    <input v-model="userData.name" type="text" class="form-control" id="name"
                        placeholder="Enter name" required>
                </div>
                <div class="form-group">
                    <label for="address">Address</label>
                    <input v-model="userData.address" type="text" class="form-control" id="address"
                        placeholder="Enter address" required>
                </div>
                <div class="form-group">
                    <label for="pincode">Pincode</label>
                    <input v-model="userData.pincode" type="number" class="form-control" id="pincode"
                        placeholder="Enter pincode" required>
                </div>
                <button type="submit" class="mt-2 btn btn-dark btn-block">Submit</button>
                <button @click="toggleEditMode()"
                    class="mt-2 mx-2 btn btn-danger btn-block">Back</button>
            </form>
        </div>
        <div v-else class="container card w-85 mt-1 p-4">
            <div style="right: 10px; position: absolute;">
                <button @click="toggleEditMode()" class="mt-2 mx-2 btn btn-danger btn-block" >Edit</button>
            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Name: </span>{{ userData.name }}
            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Email: </span>{{ userData.email }}
            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Address: </span>{{ userData.address }}
            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Pincode: </span>{{ userData.pincode }}
            </div>

        </div>
    </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';

export default {
    name: 'get_profile',
    data() {
        return {
            userData: '',
            editMode: false,
            editedAbout: '',
            showBanner: false,
            authToken : '',
        };
    },
    computed: {
        ...mapGetters(['alertMessage']),
    },
    async mounted() {
        await this.authTokenAssign();
        await this.fetchProfile();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        showBannerFor3Seconds() {
            this.showBanner = true;

            setTimeout(() => {
                this.showBanner = false;
                this.removeNotification()
            }, 3000);
        },
        toggleEditMode() {
            this.editMode = !this.editMode;
        },

        async updateUserData() {
            try {

                const response = await fetch('http://localhost:8080/api/updateUserData', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                    body: JSON.stringify(this.userData),
                });
                const data = await response.json();
                if (response.ok) {
                    var alertMessage = {
                        "Notification": data,
                    };
                    await this.fetchProfile();
                    await this.toggleEditMode(); 

                } else {
                    var alertMessage = {
                        "Notification": data,
                    };
                }
                this.$store.dispatch('updateAlertMessage', alertMessage);
            } catch (error) {
                console.error('Error:', error);
                var alertMessage = {
                    "Alert": 'An Error Occurred, Account updation Failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
            }
            this.showBannerFor3Seconds();
        },
        async fetchProfile() {
            try {
                const response = await fetch('http://localhost:8080/api/userProfile', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                });

                const data = await response.json();
                if (response.ok) {
                    this.userData = data;
                }
            } catch (error) {
                var alertMessage = {
                    "Alert": 'An error occurred, Profile fetching failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
            }
        },
        removeNotification() {
            var alertMessage = null;
            this.$store.dispatch('updateAlertMessage', alertMessage);
        }
    },
};
</script>