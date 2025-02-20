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

            <!-- Services Block -->
            <div class="jumbotron">
                <div class="d-flex flex-row my-2">
                    <h2>Services</h2>
                    <button class="btn btn-warning mx-2" @click="addNewServicePopup()" role="button">Add New</button>
                    <div v-if="isSearchServices" class="d-flex">
                        <input type="text" v-model="serviceSearch" placeholder="Search Services..."
                            @input="serviceSearchFilter" class="search-input form-control w-75 mr-sm-2 mx-2" />
                        <button class="btn btn-dark" @click="disableSearchServices">Back</button>
                    </div>
                    <div v-else>
                        <button class="btn btn-dark" @click="activateSearchServices">Search</button>
                    </div>
                </div>
            </div>
            <div v-if="isSearchServices">
                <div v-if='Object.keys(filteredServices).length > 0'>
                    <div class="container border rounded mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Service Name</th>
                                    <th scope="col">Price</th>
                                    <th scope="col">Time Required</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in filteredServices" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.name }}</td>
                                    <td>{{ item.price }}</td>
                                    <td>{{ item.time_required }}</td>
                                    <td>
                                        <button class="btn text-dark bg-warning p-2" style="border-radius: 5px;"
                                            @click="showServiceDetailsPopup(item)">View</button>
                                        <button class="btn text-light bg-dark mx-2 p-2" style="border-radius: 5px;"
                                            @click="editServicePopup(item)">Edit</button>
                                        <button class="btn text-light bg-danger p-2" style="border-radius: 5px;"
                                            @click="deleteService(item.id)">Delete</button>
                                    </td>

                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No results found.
                </div>
            </div>
            <div v-else>
                <div v-if='Object.keys(services).length > 0'>
                    <div class="container border rounded mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Service Name</th>
                                    <th scope="col">Price</th>
                                    <th scope="col">Time Required</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in services" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.name }}</td>
                                    <td>{{ item.price }}</td>
                                    <td>{{ item.time_required }}</td>
                                    <td>
                                        <button class="btn text-dark bg-warning p-2" style="border-radius: 5px;"
                                            @click="showServiceDetailsPopup(item)">View</button>
                                        <button class="btn text-light bg-dark mx-2 p-2" style="border-radius: 5px;"
                                            @click="editServicePopup(item)">Edit</button>
                                        <button class="btn text-light bg-danger p-2" style="border-radius: 5px;"
                                            @click="deleteService(item.id)">Delete</button>
                                    </td>

                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No services available. Add now by clicking on
                    <b>Add New</b> button above
                </div>

            </div>

            <!-- Professionals Block -->
            <div class="d-flex flex-row my-2">
                <h2>Professionals</h2>
                <div v-if="isSearchProfessional" class="d-flex">
                    <input type="text" v-model="professionalSearch" placeholder="Search Professional..."
                        @input="professionalSearchFilter" class="search-input form-control w-75 mr-sm-2 mx-2" />
                    <button class="btn btn-dark" @click="disableProfessionalServices">Back</button>
                </div>
                <div v-else class="mx-2">
                    <button class="btn btn-dark" @click="activateProfessionalServices">Search</button>
                </div>
            </div>
            <div v-if="isSearchProfessional">
                <div v-if='Object.keys(filteredProfessional).length > 0'>
                    <div class="container border rounded mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Experience (Yrs)</th>
                                    <th scope="col">Service Name</th>
                                    <th scope="col">Status</th>
                                    <th scope="col">Action</th>
                                    <th scope="col">Export</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in filteredProfessional" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.name }}</td>
                                    <td>{{ item.experience }} years</td>
                                    <td>{{ item.service_type }}</td>
                                    <td>{{ item.status }}</td>
                                    <td>
                                        <button class="mx-2 btn text-dark bg-warning p-2" style="border-radius: 5px;"
                                            @click="showProfessionalDetailsPopup(item)">View</button>
                                        <span v-if="item.status == 'pending'">
                                            <button class="btn text-light bg-success p-2" style="border-radius: 5px;"
                                                @click="modifyProfessional(item.id, 'approve')">Approve</button>
                                            <button class="btn text-light mx-2 bg-danger p-2"
                                                style="border-radius: 5px;"
                                                @click="modifyProfessional(item.id, 'reject')">Reject</button>
                                        </span>
                                        <span v-else-if="item.status == 'rejected'">
                                            Rejected
                                        </span>
                                        <span v-else-if="item.status == 'approved'">
                                            <button class="btn text-light bg-danger p-2" style="border-radius: 5px;"
                                                @click="modifyProfessional(item.id, 'block')">Block</button>
                                        </span>
                                        <span v-else>
                                            <button class="btn text-light bg-success p-2" style="border-radius: 5px;"
                                                @click="modifyProfessional(item.id, 'approve')">Unblock and
                                                Approve</button>
                                        </span>
                                    </td>
                                    <td><button class="btn text-light bg-success p-2" style="border-radius: 5px;"
                                        @click="exportCSV(item.id)">Export as CSV</button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No professionals available.</div>
            </div>
            <div v-else>
                <div v-if='Object.keys(all_professionals).length > 0'>
                    <div class="container border rounded mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Experience (Yrs)</th>
                                    <th scope="col">Service Name</th>
                                    <th scope="col">Status</th>
                                    <th scope="col">Action</th>
                                    <th scope="col">Export</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in all_professionals" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.name }}</td>
                                    <td>{{ item.experience }} years</td>
                                    <td>{{ item.service_type }}</td>
                                    <td>{{ item.status }}</td>
                                    <td>
                                        <button class="mx-2 btn text-dark bg-warning p-2" style="border-radius: 5px;"
                                            @click="showProfessionalDetailsPopup(item)">View</button>
                                        <span v-if="item.status == 'pending'">
                                            <button class="btn text-light bg-success p-2" style="border-radius: 5px;"
                                                @click="modifyProfessional(item.id, 'approve')">Approve</button>
                                            <button class="btn text-light mx-2 bg-danger p-2"
                                                style="border-radius: 5px;"
                                                @click="modifyProfessional(item.id, 'reject')">Reject</button>
                                        </span>
                                        <span v-else-if="item.status == 'rejected'">
                                            Rejected
                                        </span>
                                        <span v-else-if="item.status == 'approved'">
                                            <button class="btn text-light bg-danger p-2" style="border-radius: 5px;"
                                                @click="modifyProfessional(item.id, 'block')">Block</button>
                                        </span>
                                        <span v-else>
                                            <button class="btn text-light bg-success p-2" style="border-radius: 5px;"
                                                @click="modifyProfessional(item.id, 'approve')">Unblock and
                                                Approve</button>
                                        </span>
                                    </td>
                                    <td>
                                        <button class="btn text-light bg-dark p-2" style="border-radius: 5px;"
                                                @click="exportCSV(item.id)">Export as CSV</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No professionals available.</div>

            </div>
            <!-- Services Requests Block -->
            <div class="d-flex flex-row my-2">
                <h2>Service Requests</h2>
                <div v-if="isSearchServiceRequest" class="d-flex">
                    <input type="text" v-model="serviceRequestSearch" placeholder="Search Service Request..."
                        @input="serviceRequestSearchFilter" class="search-input form-control w-75 mr-sm-2 mx-2" />
                    <button class="btn btn-dark" @click="disableSearchServiceRequest">Back</button>
                </div>
                <div v-else class="mx-2">
                    <button class="btn btn-dark" @click="activateSearchServiceRequest">Search</button>
                </div>
            </div>
            <div v-if="isSearchServiceRequest">
                <div v-if='Object.keys(filteredServiceRequest).length > 0'>
                    <div class="container border rounded mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Professional Name</th>
                                    <th scope="col">Service Name</th>
                                    <th scope="col">Date of Request</th>
                                    <th scope="col">Date of Completion</th>
                                    <th scope="col">Service Status</th>
                                    <th scope="col">Rating</th>
                                    <th scope="col">Remarks</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in filteredServiceRequest" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.customer_name }}</td>
                                    <td>{{ item.professional_name }}</td>
                                    <td>{{ item.service_name }}</td>
                                    <td>{{ item.date_of_request }}</td>
                                    <td>
                                        <span v-if="service_status = 'closed'">{{ item.date_of_completion }}</span>
                                        <span v-else>Service is not closed</span>
                                    </td>
                                    <td>{{ item.service_status }}</td>
                                    <td>
                                        <span v-if="service_status = 'closed'">{{ item.rating }}</span>
                                        <span v-else>Service is not closed</span>
                                    </td>
                                    <td>
                                        <span v-if="service_status = 'closed'">
                                            <span v-if="item.remarks">{{ item.remarks }}</span>
                                            <span v-else>No remarks</span>
                                        </span>
                                        <span v-if="service_status = 'closed'">{{ item.remarks }}</span>
                                        <span v-else>Service is not closed</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No service requests available.</div>
            </div>
            <div v-else>
                <div v-if='Object.keys(all_service_requests).length > 0'>
                    <div class="container border rounded mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Customer Name</th>
                                    <th scope="col">Professional Name</th>
                                    <th scope="col">Service Name</th>
                                    <th scope="col">Date of Request</th>
                                    <th scope="col">Date of Completion</th>
                                    <th scope="col">Service Status</th>
                                    <th scope="col">Rating</th>
                                    <th scope="col">Remarks</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in all_service_requests" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.customer_name }}</td>
                                    <td>{{ item.professional_name }}</td>
                                    <td>{{ item.service_name }}</td>
                                    <td>{{ item.date_of_request }}</td>
                                    <td>
                                        <span v-if="service_status = 'closed'">{{ item.date_of_completion }}</span>
                                        <span v-else>Service is not closed</span>
                                    </td>
                                    <td>{{ item.service_status }}</td>
                                    <td>
                                        <span v-if="service_status = 'closed'">{{ item.rating }}</span>
                                        <span v-else>Service is not closed</span>
                                    </td>
                                    <td>
                                        <span v-if="service_status = 'closed'">
                                            <span v-if="item.remarks">{{ item.remarks }}</span>
                                            <span v-else>No remarks</span>
                                        </span>
                                        <span v-if="service_status = 'closed'">{{ item.remarks }}</span>
                                        <span v-else>Service is not closed</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No service requests available.</div>

            </div>

            <!-- Customer Block -->
            <div class="d-flex flex-row my-2">
                <h2>Customers</h2>
                <div v-if="isSearchCustomer" class="d-flex">
                        <input type="text" v-model="customerSearch" placeholder="Search Customers..."
                            @input="customerSearchFilter" class="search-input form-control w-75 mr-sm-2 mx-2" />
                        <button class="btn btn-dark" @click="disableSearchCustomer">Back</button>
                    </div>
                    <div v-else class="mx-2">
                        <button class="btn btn-dark" @click="activateSearchCustomer">Search</button>
                    </div>
            </div>
            <div v-if="isSearchCustomer">
                <div v-if='Object.keys(filteredCustomer).length > 0'>
                    <div class="container border rounded mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Address</th>
                                    <th scope="col">Status</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {{ item }}
                                <tr v-for="(item, index) in filteredCustomer" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.name }}</td>
                                    <td>{{ item.address }}, {{ item.pincode }}</td>
                                    <td>{{ item.status }}</td>
                                    <td>
                                        <span v-if="item.status == 'blocked'">
                                            <button class="btn text-light bg-success p-2" style="border-radius: 5px;"
                                                @click="modifyCustomer(item.id, 'unblock')">Unblock it</button>
                                        </span>
                                        <span v-else-if="item.status == 'unblocked'">
                                            <button class="btn text-light bg-danger p-2" style="border-radius: 5px;"
                                                @click="modifyCustomer(item.id, 'block')">Block it</button>
                                        </span>
                                    
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No customers available.</div>
            </div>
            <div v-else>
                <div v-if='Object.keys(all_customers).length > 0'>
                    <div class="container border rounded mb-3 scrollbar-primary mobile" style="gap: 5px;">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Address</th>
                                    <th scope="col">Status</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in all_customers" :key="index">
                                    <th scope="row">{{ index + 1 }}</th>
                                    <td>{{ item.name }}</td>
                                    <td>{{ item.address }}, {{ item.pincode }}</td>
                                    <td>{{ item.status }}</td>
                                    <td>
                                        <span v-if="item.status == 'blocked'">
                                            <button class="btn text-light bg-success p-2" style="border-radius: 5px;"
                                                @click="modifyCustomer(item.id, 'unblock')">Unblock it</button>
                                        </span>
                                        <span v-else-if="item.status == 'unblocked'">
                                            <button class="btn text-light bg-danger p-2" style="border-radius: 5px;"
                                                @click="modifyCustomer(item.id, 'block')">Block it</button>
                                        </span>
                                  
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div v-else class="card p-4" style="font-size: 1.2rem;">No customers available.</div>

            </div>

        </div>
    </div>



    <!-- Show Edit Service Popup -->
    <div v-if="showEditService" class="modal-overlay" @click.self="hideServicePopup">
        <div class="modal-content scrollbar-primary w-75">
            <span class="close-btn" @click="hideServicePopup">&times;</span>
            <div>
                <h2>Fill details in below form to update {{ selectedService.name }}</h2>
                <!-- {{ selectedServiceForClose }} -->
                <div class="d-flex flex-wrap container">
                    <div class="m-2 p-2 col-md-2 card"><b>Service Name:</b> {{ selectedService.name }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Price:</b> {{ selectedService.price }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Time Required:</b> {{ selectedService.time_required
                        }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Description:</b> {{ selectedService.description }}</div>
                </div>
                <div class="container">
                    <form @submit.prevent="updateService()">
                        <!-- Login Form -->
                        <div class="form-group">
                            <label for="name">Name</label>
                            <input v-model="selectedService.name" type="text" class="form-control" id="name"
                                placeholder="Enter name" required>
                        </div>
                        <div class="form-group">
                            <label for="price">Price</label>
                            <input v-model="selectedService.price" type="text" class="form-control" id="price"
                                placeholder="Enter price">
                        </div>
                        <div class="form-group">
                            <label for="time_required">Time Required</label>
                            <input v-model="selectedService.time_required" type="text" class="form-control"
                                id="time_required" placeholder="Enter time required">
                        </div>
                        <div class="form-group">
                            <label for="description">Description</label>
                            <input v-model="selectedService.description" type="text" class="form-control"
                                id="description" placeholder="Enter description">
                        </div>
                        <button type="submit" class="mt-2 btn btn-dark btn-block">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- View Service Details Popup -->
    <div v-if="showServiceDetails" class="modal-overlay" @click.self="hideServicePopup">
        <div class="modal-content scrollbar-primary w-75">
            <span class="close-btn" @click="hideServicePopup">&times;</span>
            <div>
                <h2>{{ selectedService.name }}</h2>
                <!-- {{ selectedServiceForClose }} -->
                <div class="d-flex flex-wrap container">
                    <div class="m-2 p-2 col-md-2 card"><b>Service Name:</b> {{ selectedService.name }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Price:</b> {{ selectedService.price }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Time Required:</b> {{ selectedService.time_required
                        }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Description:</b> {{ selectedService.description }}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- View Professional Details Popup -->
    <div v-if="showProfessionalDetails" class="modal-overlay" @click.self="hideProfessionalPopup">
        <div class="modal-content scrollbar-primary w-75">
            <span class="close-btn" @click="hideProfessionalPopup">&times;</span>
            <div>
                <h2>{{ selectedProfessional.name }}</h2>
                <div class="d-flex flex-wrap container">
                    <div class="m-2 p-2 col-md-2 card"><b>Service Name:</b> {{ selectedProfessional.name }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Address:</b> {{ selectedProfessional.address }}, {{
                        selectedProfessional.pincode }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Service Type:</b> {{ selectedProfessional.service_type
                        }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Experience:</b> {{ selectedProfessional.experience }} years
                    </div>
                    <div class="m-2 p-2 col-md-2 card"><b>Date Created:</b> {{ selectedProfessional.date_created }}
                    </div>
                    <div class="m-2 p-2 col-md-2 card"><b>Document:</b> <button class="btn text-light bg-dark p-2"
                            style="border-radius: 5px;"
                            @click="downloadFile(selectedProfessional.document)">Download</button></div>
                    <div class="m-2 p-2 col-md-2 card"><b>Account Status:</b> {{ selectedProfessional.status }}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Show Add New Service Popup -->
    <div v-if="addNewService" class="modal-overlay" @click.self="hideServicePopup">
        <div class="modal-content scrollbar-primary w-75">
            <span class="close-btn" @click="hideServicePopup">&times;</span>
            <div>
                <h2>Add New Service</h2>
                <div class="d-flex flex-wrap container">
                    <div class="m-2 p-2 col-md-2 card"><b>Service Name:</b> {{ newService.name }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Price:</b> {{ newService.price }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Time Required:</b> {{ newService.time_required
                        }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Description:</b> {{ newService.description }}</div>
                </div>
                <div class="container">
                    <form @submit.prevent="addService()">
                        <!-- Login Form -->
                        <div class="form-group">
                            <label for="name">Name</label>
                            <input v-model="newService.name" type="text" class="form-control" id="name"
                                placeholder="Enter name" required>
                        </div>
                        <div class="form-group">
                            <label for="price">Price</label>
                            <input v-model="newService.price" type="number" class="form-control" id="price"
                                placeholder="Enter price">
                        </div>
                        <div class="form-group">
                            <label for="time_required">Time Required</label>
                            <input v-model="newService.time_required" type="text" class="form-control"
                                id="time_required" placeholder="Enter time required">
                        </div>
                        <div class="form-group">
                            <label for="description">Description</label>
                            <input v-model="newService.description" type="text" class="form-control" id="description"
                                placeholder="Enter description">
                        </div>
                        <button type="submit" class="mt-2 btn btn-dark btn-block">Submit</button>
                    </form>
                </div>
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
            all_customers: '',
            all_professionals: '',
            services: '',
            all_requests: '',
            showEditService: false,
            addNewService: false,
            selectedService: null,
            newService: {
                name: '',
                price: '',
                time_required: '',
                description: '',
            },
            showServiceDetails: false,
            showProfessionalDetails: false,
            selectedProfessional: null,
            all_service_requests: '',
            isSearchServices: false,
            serviceSearch: '',
            filteredServices: '',
            isSearchProfessional: false,
            professionalSearch: '',
            filteredProfessional: '',
            isSearchServiceRequest: false,
            serviceRequestSearch: '',
            filteredServiceRequest: '',
            isSearchCustomer: false,
            customerSearch: '',
            filteredCustomer: '',
            showBanner: false,
            authToken : '',
        };
    },
    computed: {
        ...mapGetters(['alertMessage']),
    },
    async mounted() {
        await this.authTokenAssign();
        await this.getAllServices();
        await this.getAllProfessionals();
        await this.getAllCustomers();
        await this.getAllServiceRequests();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        serviceSearchFilter() {
            const query = this.serviceSearch.toLowerCase();
            this.filteredServices = this.services.filter(item => {
                const nameMatches = item.name && item.name.toLowerCase().includes(query);
                const priceMatches = item.price !== undefined && item.price.toString().includes(query);
                const timeRequiredMatches = item.time_required && item.time_required.toString().includes(query);

                return nameMatches || priceMatches || timeRequiredMatches; // Use OR to match any field
            });

            
        },
        professionalSearchFilter() {
            const query = this.professionalSearch.toLowerCase();
            this.filteredProfessional = this.all_professionals.filter(item => {
                const nameMatches = item.name && item.name.toLowerCase().includes(query);
                const experienceMatches = item.experience !== undefined && item.experience.toString().includes(query);
                const serviceNameMatches = item.service_type && item.service_type.toLowerCase().includes(query);
                const statusMatches = item.status && item.status.toLowerCase().includes(query);


                return nameMatches || experienceMatches || serviceNameMatches || statusMatches; // Use OR to match any field
            });

            
        },
        serviceRequestSearchFilter() {
            const query = this.serviceRequestSearch.toLowerCase();
            this.filteredServiceRequest = this.all_service_requests.filter(item => {
                const customernameMatches = item.customer_name && item.customer_name.toLowerCase().includes(query);
                const professionalnameMatches = item.professional_name && item.professional_name.toLowerCase().includes(query);
                const service_nameMatches = item.service_name && item.service_name.toLowerCase().includes(query);
                const statusMatches = item.service_status && item.service_status.toLowerCase().includes(query);
                const remarksMatches = item.remarks && item.remarks.toLowerCase().includes(query);
                const ratingMatches = item.rating !== undefined && item.rating.toString().includes(query);


                return customernameMatches || professionalnameMatches || service_nameMatches || statusMatches || remarksMatches || ratingMatches;
            });

            
        },
        customerSearchFilter() {
            const query = this.customerSearch.toLowerCase();
            this.filteredCustomer = this.all_customers.filter(item => {
                const nameMatches = item.name && item.name.toLowerCase().includes(query);
                const addressMatches = item.address && item.address.toLowerCase().includes(query);
                const statusMatches = item.status && item.status.toLowerCase().includes(query);
                const pincodeMatches = item.pincode !== undefined && item.pincode.toString().includes(query);

                return nameMatches || addressMatches || statusMatches || pincodeMatches; // Use OR to match any field
            });

            
        },

        downloadFile(filePath) {
            // Replace 'your-backend-url' with your actual backend address
            const downloadUrl = `http://localhost:8080/download/${filePath}`;
            
            // Trigger file download by opening the URL in a new tab
            window.open(downloadUrl, '_blank');
        },
        activateSearchServiceRequest() {
            this.isSearchServiceRequest = true;
            this.filteredServiceRequest = this.all_service_requests;
        },
        disableSearchServiceRequest() {
            this.isSearchServiceRequest = false;
        },
        activateSearchCustomer() {
            this.isSearchCustomer = true;
            this.filteredCustomer=this.all_customers;
        },
        disableSearchCustomer() {
            this.isSearchCustomer = false;
        },
        activateSearchServices() {
            this.filteredServices=this.services;
            this.isSearchServices = true;
        },
        disableSearchServices() {
            this.isSearchServices = false;
        },
        activateProfessionalServices() {
            this.filteredProfessional=this.all_professionals;
            this.isSearchProfessional = true;
        },
        disableProfessionalServices() {
            this.isSearchProfessional = false;
        },
        showBannerFor3Seconds() {
            this.showBanner = true;
            setTimeout(() => {
                this.showBanner = false;
                this.removeNotification()
            }, 3000);
        },

        async editServicePopup(item) {
            this.selectedService = item;
            this.showEditService = true;
            //   await this.getServiceDetails(service);
        },

        async showServiceDetailsPopup(item) {
            this.selectedService = item;
            this.showServiceDetails = true;
        },

        async showProfessionalDetailsPopup(item) {
            this.selectedProfessional = item;
            this.showProfessionalDetails = true;
        },
        async addNewServicePopup() {
            this.addNewService = true;
        },
        async hideServicePopup() {
            this.showEditService = false;
            this.addNewService = false;
            this.showServiceDetails = false;
            this.selectedService = null;
            await this.getAllServices();
        },
        async hideProfessionalPopup() {
            this.showProfessionalDetails = false;
            this.selectedProfessional = null;
        },

        async getAllServices() {
            try {
                if (this.authToken) {
                    const response = await fetch('http://localhost:8080/api/getAllServices', {
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
                    
                    this.services = data;
                }
            } catch (error) {
                var alertMessage = {
                    "Alert": 'An error occurred, Services fetching failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
            }
        },
        async getAllProfessionals() {
            try {
                if (this.authToken) {
                    const response = await fetch('http://localhost:8080/api/getAllProfessionals', {
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
                    
                    this.all_professionals = data;
                }
            } catch (error) {
                var alertMessage = {
                    "Alert": 'An error occurred, Professionals fetching failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
            }
        },
        async getAllCustomers() {
            try {
                if (this.authToken) {
                    const response = await fetch('http://localhost:8080/api/getAllCustomers', {
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
                    
                    this.all_customers = data;
                }
            } catch (error) {
                var alertMessage = {
                    "Alert": 'An error occurred, Professionals fetching failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
            }
        },
        async getAllServiceRequests() {
            try {
                if (this.authToken) {
                    const response = await fetch('http://localhost:8080/api/getAllServiceRequests', {
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
                    
                    this.all_service_requests = data;
                }
            } catch (error) {
                var alertMessage = {
                    "Alert": 'An error occurred, Service Requests fetching failed',
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
                this.showBannerFor3Seconds();
            }
        },
        async updateService() {
            try {
                const response = await fetch('http://localhost:8080/api/updateService', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                    body: JSON.stringify(this.selectedService),
                });

                const data = await response.json();

                if (response.ok) {
                    var alertMessage = {
                        "Notification": data,
                    };
                    await this.getAllServices();
                    await this.hideServicePopup();
                } else {
                    var alertMessage = {
                        "Alert": data,
                    };
                }
                this.$store.dispatch('updateAlertMessage', alertMessage);
            } catch (error) {
                var alertMessage = {
                    "Alert": `An Error Occurred,updating failed`,
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
            }
            this.showBannerFor3Seconds();
        },
        async deleteService(item_id) {
            try {
                const response = await fetch(`http://localhost:8080/api/deleteService/${item_id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                });
                const data = await response.json();
                if (response.ok) {
                    var alertMessage = {
                        "Notification": data,
                    };
                    await this.getAllServices();
                    // await this.hidePopup();
                } else {
                    var alertMessage = {
                        "Alert": data,
                    };
                }
                this.$store.dispatch('updateAlertMessage', alertMessage);
            } catch (error) {
                var alertMessage = {
                    "Alert": `An Error Occurred,deleting failed`,
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
            }
            this.showBannerFor3Seconds();
        },

        async addService() {
            try {
                const response = await fetch('http://localhost:8080/api/addService', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                    body: JSON.stringify(this.newService),
                });

                const data = await response.json();
                if (response.ok) {
                    var alertMessage = {
                        "Notification": data,
                    };
                    await this.getAllServices();
                    await this.hideServicePopup();
                } else {
                    var alertMessage = {
                        "Alert": data,
                    };
                }
                this.$store.dispatch('updateAlertMessage', alertMessage);
            } catch (error) {
                var alertMessage = {
                    "Alert": `An Error Occurred,creating new service failed`,
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
            }
            this.showBannerFor3Seconds();
        },

        async exportCSV(item_id) {
            try {
                const professionalData = {
                    professional_id: item_id,
                }
                const response = await fetch(`http://localhost:8080/api/exportCSV`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                    body: JSON.stringify(professionalData),
                });

                const data = await response.json();
                if (response.ok) {
                    var alertMessage = {
                        "Notification": data,
                    };
                } else {
                    var alertMessage = {
                        "Alert": data,
                    };
                }
                this.$store.dispatch('updateAlertMessage', alertMessage);
            } catch (error) {
                var alertMessage = {
                    "Alert": `An Error Occurred,exporting as csv failed`,
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
            }
            this.showBannerFor3Seconds();
        },
        async modifyProfessional(item_id, action) {
            try {
                const dict = {
                    id: item_id,
                    action: action,
                };
                const response = await fetch('http://localhost:8080/api/updateProfessional', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                    body: JSON.stringify(dict),
                });

                const data = await response.json();

                if (response.ok) {
                    var alertMessage = {
                        "Notification": data,
                    };
                    await this.getAllProfessionals();
                } else {
                    var alertMessage = {
                        "Alert": data,
                    };
                }
                this.$store.dispatch('updateAlertMessage', alertMessage);
            } catch (error) {
                var alertMessage = {
                    "Alert": `An Error Occurred,updating failed`,
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
            }
            this.showBannerFor3Seconds();
        },
        async modifyCustomer(item_id, action) {
            try {
                const dict = {
                    id: item_id,
                    action: action,
                };
                const response = await fetch('http://localhost:8080/api/updateCustomer', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken,
                    },
                    body: JSON.stringify(dict),
                });

                const data = await response.json();

                if (response.ok) {
                    var alertMessage = {
                        "Notification": data,
                    };
                    await this.getAllCustomers();
                } else {
                    var alertMessage = {
                        "Alert": data,
                    };
                }
                this.$store.dispatch('updateAlertMessage', alertMessage);
            } catch (error) {
                var alertMessage = {
                    "Alert": `An Error Occurred,updating failed`,
                };
                this.$store.dispatch('updateAlertMessage', alertMessage);
            }
            this.showBannerFor3Seconds();
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