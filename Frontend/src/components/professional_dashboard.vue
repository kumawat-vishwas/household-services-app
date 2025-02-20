<template>
    <div class="container">
        <div>
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
        </div>

        <div class="row mb-4">

            <!-- Today's Services Block -->
            <div class="jumbotron">
                <div class="d-flex my-2 flex-row">
                    <h2>Today's Services</h2>
                    <div v-if="isSearchtodayService" class="d-flex">
                        <input type="text" v-model="todayServiceSearch" placeholder="Search todayService..."
                            @input="todayServiceSearchFilter" class="search-input form-control w-75 mr-sm-2 mx-2" />
                        <button class="btn btn-dark" @click="disableSearchtodayService">Back</button>
                    </div>
                    <div v-else class="mx-2">
                        <button class="btn btn-dark" @click="activateSearchtodayService">Search</button>
                    </div>
                </div>

            </div>
            <div v-if="isSearchtodayService">
                <div v-if='Object.keys(filteredtodayService).length > 0'>
                    <div class="container mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Location (with pincode)</th>
                                    <th scope="col">Date of Request</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in filteredtodayService" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.customer_name }}</td>
                                    <td>{{ item.customer_address }}, {{ item.customer_pincode }}</td>
                                    <td>{{ item.date_of_request }}</td>
                                    <td>
                                        <button class="btn text-light bg-dark p-2" style="border-radius: 5px;"
                                            @click="acceptServiceRequest(item.service_request_id)">Accept</button>
                                        <button class="btn mx-2 text-light bg-danger p-2" style="border-radius: 5px;"
                                            @click="rejectServiceRequest(item.service_request_id)">Reject</button>
                                    </td>

                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No results found.</div>
            </div>
            <div v-else>
                <div v-if='Object.keys(today_services).length > 0'>
                    <div class="container mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Location (with pincode)</th>
                                    <th scope="col">Date of Request</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in today_services" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.customer_name }}</td>
                                    <td>{{ item.customer_address }}, {{ item.customer_pincode }}</td>
                                    <td>{{ item.date_of_request }}</td>
                                    <td>
                                        <button class="btn text-light bg-dark p-2" style="border-radius: 5px;"
                                            @click="acceptServiceRequest(item.service_request_id)">Accept</button>
                                        <button class="btn mx-2 text-light bg-danger p-2" style="border-radius: 5px;"
                                            @click="rejectServiceRequest(item.service_request_id)">Reject</button>
                                    </td>

                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No services available.</div>

            </div>

            <!-- Closed Services Block -->

            <div class="d-flex flex-row my-2">
                <h2 class="mx-2">Closed Services</h2>
                <div v-if="isSearchclosedservice" class="d-flex">
                    <input type="text" v-model="closedserviceSearch" placeholder="Search closedservice..."
                        @input="closedserviceSearchFilter" class="search-input form-control w-75 mr-sm-2 mx-2" />
                    <button class="btn btn-dark" @click="disableSearchclosedservice">Back</button>
                </div>
                <div v-else class="mx-2">
                    <button class="btn btn-dark" @click="activateSearchclosedservice">Search</button>
                </div>
            </div>
            <div v-if="isSearchclosedservice">
                <div v-if='Object.keys(filteredclosedservice).length > 0'>
                    <div class="container mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Location (with pincode)</th>
                                    <th scope="col">Date of Request</th>
                                    <th scope="col">Date of Completion</th>
                                    <th scope="col">Rating</th>
                                    <th scope="col">Remarks (If any)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in filteredclosedservice" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.customer_name }}</td>
                                    <td>{{ item.customer_address }}, {{ item.customer_pincode }}</td>
                                    <td>{{ item.date_of_request }}</td>
                                    <td>
                                        {{ item.date_of_completion }}
                                    </td>
                                    <td>
                                        {{ item.rating }}
                                    </td>
                                    <td>
                                        {{ item.remarks }}
                                    </td>

                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No results found.</div>
            </div>
            <div v-else>
                <div v-if='Object.keys(closed_services).length > 0'>
                    <div class="container mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Location (with pincode)</th>
                                    <th scope="col">Date of Request</th>
                                    <th scope="col">Date of Completion</th>
                                    <th scope="col">Rating</th>
                                    <th scope="col">Remarks (If any)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in closed_services" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.customer_name }}</td>
                                    <td>{{ item.customer_address }}, {{ item.customer_pincode }}</td>
                                    <td>{{ item.date_of_request }}</td>
                                    <td>
                                        {{ item.date_of_completion }}
                                    </td>
                                    <td>
                                        {{ item.rating }}
                                    </td>
                                    <td>
                                        {{ item.remarks }}
                                    </td>

                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No services available.</div>
            </div>

            <!-- Accepted/Rejected Services Block -->

            <div class="d-flex flex-row my-2">
                <h2 class="mx-2">Accepted/Rejected Services</h2>
                <div v-if="isSearchacceptedRejectedService" class="d-flex">
                    <input type="text" v-model="acceptedRejectedServiceSearch"
                        placeholder="Search acceptedRejectedService..." @input="acceptedRejectedServiceSearchFilter"
                        class="search-input form-control w-75 mr-sm-2 mx-2" />
                    <button class="btn btn-dark" @click="disableSearchacceptedRejectedService">Back</button>
                </div>
                <div v-else class="mx-2">
                    <button class="btn btn-dark" @click="activateSearchacceptedRejectedService">Search</button>
                </div>
            </div>
            <div v-if="isSearchacceptedRejectedService">
                <div v-if='Object.keys(filteredacceptedRejectedService).length > 0'>
                    <div class="container mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Location (with pincode)</th>
                                    <th scope="col">Date of Request</th>
                                    <th scope="col">Service Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in filteredacceptedRejectedService" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.customer_name }}</td>
                                    <td>{{ item.customer_address }}, {{ item.customer_pincode }}</td>
                                    <td>{{ item.date_of_request }}</td>
                                    <td>
                                        {{ item.service_status }}
                                    </td>


                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No results found.</div>
            </div>
            <div v-else>
                <div v-if='Object.keys(acceptedRejected).length > 0'>
                    <div class="container mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Location (with pincode)</th>
                                    <th scope="col">Date of Request</th>
                                    <th scope="col">Service Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in acceptedRejected" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.customer_name }}</td>
                                    <td>{{ item.customer_address }}, {{ item.customer_pincode }}</td>
                                    <td>{{ item.date_of_request }}</td>
                                    <td>
                                        {{ item.service_status }}
                                    </td>


                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No services available.</div>
            </div>

        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';


export default {
    name: 'ProfessionalDashboard',
    data() {
        return {
            today_services: '',
            closed_services: '',
            acceptedRejected: '',
            isSearchtodayService: false,
            todayServiceSearch: '',
            filteredtodayService: '',
            isSearchclosedservice: false,
            closedserviceSearch: '',
            filteredclosedservice: '',
            isSearchacceptedRejectedService: false,
            acceptedRejectedServiceSearch: '',
            filteredacceptedRejectedService: '',
            showBanner: false,
            authToken : '',

        };
    },

    computed: {
        ...mapGetters(['alertMessage']),

    },
    async mounted() {
        await this.authTokenAssign();
        await this.getAllTodayServices();
        await this.getAllClosedServices();
        await this.getAccpetedRejected();
        await this.userVisited();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        acceptedRejectedServiceSearchFilter() {
            const query = this.acceptedRejectedServiceSearch.toLowerCase();
            this.filteredacceptedRejectedService = this.acceptedRejected.filter(item => {
                const nameMatches = item.customer_name && item.customer_name.toLowerCase().includes(query);
                const customer_addressMatches = item.customer_address && item.customer_address.toLowerCase().includes(query);
                const pincodeMatches = item.customer_pincode !== undefined && item.customer_pincode.toString().includes(query);
                const date_of_request = item.date_of_request && item.date_of_request.toString().includes(query);

                const service_status = item.service_status && item.service_status.toString().includes(query);

                return nameMatches || customer_addressMatches || pincodeMatches || date_of_request || service_status; // Use OR to match any field
            });

            
        },


        activateSearchacceptedRejectedService() {
            this.isSearchacceptedRejectedService = true;
            this.filteredacceptedRejectedService = this.acceptedRejected
        },
        disableSearchacceptedRejectedService() {
            this.isSearchacceptedRejectedService = false;
        },
        closedserviceSearchFilter() {
            const query = this.closedserviceSearch.toLowerCase();
            this.filteredclosedservice = this.closed_services.filter(item => {
                const nameMatches = item.customer_name && item.customer_name.toLowerCase().includes(query);
                const customer_addressMatches = item.customer_address && item.customer_address.toLowerCase().includes(query);
                const pincodeMatches = item.customer_pincode !== undefined && item.customer_pincode.toString().includes(query);
                const date_of_request = item.date_of_request && item.date_of_request.toString().includes(query);
                const date_of_completion = item.date_of_completion && item.date_of_completion.toString().includes(query);
                const remarks = item.remarks && item.remarks.toString().includes(query);
                const rating = item.rating !== undefined && item.rating.toString().includes(query);

                return nameMatches || customer_addressMatches || pincodeMatches || date_of_request || date_of_completion || remarks || rating; // Use OR to match any field
            });

            
        },


        activateSearchclosedservice() {
            this.isSearchclosedservice = true;
            this.filteredclosedservice = this.closed_services
        },
        disableSearchclosedservice() {
            this.isSearchclosedservice = false;
        },
        todayServiceSearchFilter() {
            const query = this.todayServiceSearch.toLowerCase();
            this.filteredtodayService = this.today_services.filter(item => {
                const nameMatches = item.customer_name && item.customer_name.toLowerCase().includes(query);
                const customer_addressMatches = item.customer_address && item.customer_address.toLowerCase().includes(query);
                const pincodeMatches = item.customer_pincode !== undefined && item.customer_pincode.toString().includes(query);
                const date_of_request = item.date_of_request && item.date_of_request.toString().includes(query);

                return nameMatches || customer_addressMatches || pincodeMatches || date_of_request; // Use OR to match any field
            });

            
        },
        activateSearchtodayService() {
            this.isSearchtodayService = true;
            this.filteredtodayService = this.today_services;
        },
        disableSearchtodayService() {
            this.isSearchtodayService = false;
        },
        showBannerFor3Seconds() {
            this.showBanner = true;
            setTimeout(() => {
                this.showBanner = false;
                this.removeNotification()
            }, 3000);
        },
        async getAllTodayServices() {
            try {
                if (this.authToken) {
                    const response = await fetch('http://localhost:8080/api/getAllTodayServices', {
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
                    
                    this.today_services = data;
                    await this.getAccpetedRejected();
                }
            } catch (error) {
                var alertMessage = {
                    "Alert": 'An error occurred, Today\'s services fetching failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
            }
        },
        async getAccpetedRejected() {
            try {
                if (this.authToken) {
                    const response = await fetch('http://localhost:8080/api/getAccpetedRejected', {
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
                    
                    this.acceptedRejected = data;
                }
            } catch (error) {
                var alertMessage = {
                    "Alert": 'An error occurred, Accepted/Rejected fetching failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
            }
        },
        async getAllClosedServices() {
            try {
                if (this.authToken) {
                    const response = await fetch('http://localhost:8080/api/getAllClosedServices', {
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
                    
                    this.closed_services = data;
                }
            } catch (error) {
                var alertMessage = {
                    "Alert": 'An error occurred, Closed Services fetching failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
            }
        },
        async acceptServiceRequest(item_id) {
            try {
                const serviceRequestData = {
                    service_request_id: item_id,
                };

                const response = await fetch('http://localhost:8080/api/acceptServiceRequest', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                    body: JSON.stringify(serviceRequestData),
                });

                const data = await response.json();
                if (response.ok) {
                    var alertMessage = {
                        "Notification": data,
                    };
                    await this.getAllTodayServices();
                } else {
                    var alertMessage = {
                        "Alert": data,
                    };
                }
                this.$store.dispatch('updateAlertMessage', alertMessage);
            } catch (error) {
                var alertMessage = {
                    "Alert": `An Error Occurred,accepting failed`,
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
            }
            this.showBannerFor3Seconds();
        },
        async rejectServiceRequest(item_id) {
            try {
                const serviceRequestData = {
                    service_request_id: item_id,
                };

                const response = await fetch('http://localhost:8080/api/rejectServiceRequest', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                    body: JSON.stringify(serviceRequestData),
                });

                const data = await response.json();
                if (response.ok) {
                    var alertMessage = {
                        "Notification": data,
                    };
                    await this.getAllTodayServices();
                } else {
                    var alertMessage = {
                        "Alert": data,
                    };
                }
                this.$store.dispatch('updateAlertMessage', alertMessage);
            } catch (error) {
                var alertMessage = {
                    "Alert": `An Error Occurred,rejecting failed`,
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
            }
            this.showBannerFor3Seconds();
        },

        async userVisited() {
            try {

                const response = await fetch('http://localhost:8080/api/userVisited', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                });

                if (response.ok) {

                } else {
                    console.error('User visit saving failed', response.statusText, response);

                }
            } catch (error) {
                console.error('Error:', error);

            }
        },

        removeNotification() {
            const alertMessage = null;
            this.$store.dispatch('updateAlertMessage', alertMessage);
        }

    },
};
</script>

<style scoped>
@media (max-width: 768px) {
    .song {
        flex-wrap: wrap;
        width: auto;
    }

    .service {
        flex-direction: column !important;
    }

    .mobile {
        flex-direction: column !important;
        margin: auto;
    }

    .song_title {
        margin: auto;
    }

    .song .card {
        width: 100% !important;
    }
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5) !important;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}

.modal-content {
    max-height: 75%;
    overflow-y: auto;
}

.container {
    width: 100%;
    overflow-x: auto;
}

.song_title {
    margin: auto 0px;
    margin-left: 12px;
    width: fit-content;
}

.col-md-6 {
    width: fit-content !important;
}
</style>