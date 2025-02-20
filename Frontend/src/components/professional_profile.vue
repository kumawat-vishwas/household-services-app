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

        <div class="container card w-85 mt-1 p-4">
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Name: </span>{{ userData.name }}
            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Email: </span>{{ userData.email }}
            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Address: </span>{{ userData.address }}, {{ userData.pincode }}
            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Service Type: </span>{{ userData.service_type }}
            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Experience: </span>{{ userData.experience }} years
            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Document: </span>
                <button class="btn text-light bg-dark p-2" style="border-radius: 5px;"
                @click="downloadFile(userData.document)">Download</button>

            </div>
            <div class="mt-1" style="font-size: 1.2rem;">
                <span style="font-weight: 700;">Account Creation Date: </span>{{ userData.date_created }}
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

            about: '',
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
        downloadFile(filePath) {
            const downloadUrl = `http://localhost:8080/download/${filePath}`;
            
            // Trigger file download by opening the URL in a new tab
            window.open(downloadUrl, '_blank');
        },
        showBannerFor3Seconds() {
            this.showBanner = true;

            setTimeout(() => {
                this.showBanner = false;
                this.removeNotification()
            }, 3000);
        },
      
        async fetchProfile() {
            try {
                const response = await fetch('http://localhost:8080/api/professionalProfile', {
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