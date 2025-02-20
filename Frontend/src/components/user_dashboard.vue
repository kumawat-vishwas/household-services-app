<template>
  <div class="container">
    <div class="jumbotron">
      <div class="d-flex flex-row">
      </div>

    </div>
    <div>
      <div v-if="showBanner" class="d-flex banner" style="justify-content: center;">
        <div v-if="alertMessage" class="d-flex flex-row flex-wrap alert container bg-warning text-dark w-50"
          role="alert" style="position: fixed;bottom: 0px; z-index: 99999; justify-content: center; align-items: end;">
          <span v-for="value, key in alertMessage" class="mx-1" style="width: auto;gap: 16px">
            <strong>{{ key }}:</strong> {{ value }};
          </span>
          <span type="button" class="position-absolute btn btn-link btn-sm text-dark" @click="removeNotification()"
            style="right: 0; font-size: 1.2rem;"><i class="bi bi-x-circle"></i></span>
        </div>
      </div>
    </div>

    <div class="row mb-4">

      <!-- Filter by services Block -->
      <div>
        <div v-if='(all_services_name_list.length) > 0'>
          <div class="d-flex">
            <h2 class="my-2 mx-2">Looking For?</h2>
            <div class="text-end">
            </div>
          </div>

        </div>
        <div v-else class="card p-4" style="font-size: 1.2rem;">
          No service category available right now. Please try again later.</div>
        <div class="d-flex container flex-row mb-3 scrollbar-primary mobile" style="gap: 5px;">
          <div v-for="service in all_services_name_list" :key="service.id"
            class="col-md-5 card albums mb-3 itemBlockClickable" style="width: 35%;" @click="showServicePopup(service)">
            <div class="card-body m-auto">
              <div class="d-flex">
                <div class="p-2 rounded" style="max-width: max-content;">
                  <span class="" style="font-weight: 700; font-size: 1.5rem;">
                    {{ service }}
                  </span>

                </div>
              </div>

            </div>

          </div>
        </div>
      </div>

      <!-- Services History Block -->
      <div class="jumbotron">
        <div class="d-flex flex-row my-2">
          <h2>Service History</h2>
          <div v-if="isSearchServices" class="d-flex">
            <input type="text" v-model="serviceSearch" placeholder="Search Services..." @input="serviceSearchFilter"
              class="search-input form-control w-75 mr-sm-2 mx-2" />
            <button class="btn btn-dark" @click="disableSearchServices">Back</button>
          </div>
          <div v-else class=mx-2>
            <button class="btn btn-dark" @click="activateSearchServices">Search</button>
          </div>
        </div>
      </div>
      <div v-if="isSearchServices">
        <div v-if='Object.keys(filteredServices).length > 0'>
          <div class="container mb-3 scrollbar-primary mobile" style="gap: 5px;">
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Service Name</th>
                  <th scope="col">Professional Name</th>
                  <th scope="col">Date of Request</th>
                  <th scope="col">Experience</th>
                  <th scope="col">Address</th>
                  <th scope="col">Document</th>
                  <th scope="col">Book</th>
                  <th scope="col">Date of Completion</th>
                  <th scope="col">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in filteredServices" :key="index">
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ item.service_name }}</td>
                  <td>{{ item.name }}</td>
                  <td>{{ item.date_of_request }}</td>
                  <td>{{ item.experience }} years</td>
                  <td>{{ item.address }}, {{ item.pincode }}</td>
                  <td><button class="btn text-light bg-dark p-2" style="border-radius: 5px;"
                      @click="downloadFile(item.document)">Download</button></td>
                  <td>
                    <span v-if="item.service_status == 'requested'">
                      Requested
                    </span>
                    <span v-else-if="item.service_status == 'assigned'">
                      <button class="btn text-light bg-danger p-2" style="border-radius: 5px;"
                        @click="showServiceCloseBlockFromeHome(item)">Close it?</button>
                    </span>
                    <span v-else>
                      Closed
                    </span>
                  </td>
                  <td>
                    <span v-if="item.service_status == 'closed'">{{ item.date_of_completion }}</span>
                    <span v-else>Not Closed</span>
                  </td>
                  <td>
                    <button class="btn text-dark bg-warning p-2" style="border-radius: 5px;"
                    @click="updateServiceHistoryCustomerPopup(item)">Update</button>
                    <button class="mx-2 btn text-light bg-danger p-2" style="border-radius: 5px;"
                    @click="deleteServiceHistoryCustomer(item.service_id)">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else class="card p-4">
          <div class="p-3 rounded">
            <p class="my-auto">No matching results.</p>
          </div>
        </div>

      </div>
      <div v-else>
        <div v-if='Object.keys(allServices).length > 0'>
          <div class="container mb-3 scrollbar-primary mobile" style="gap: 5px;">
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Service Name</th>
                  <th scope="col">Professional Name</th>
                  <th scope="col">Date of Request</th>
                  <th scope="col">Experience</th>
                  <th scope="col">Address</th>
                  <th scope="col">Document</th>
                  <th scope="col">Book</th>
                  <th scope="col">Date of Completion</th>
                  <th scope="col">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in allServices" :key="index">
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ item.service_name }}</td>
                  <td>{{ item.name }}</td>
                  <td>{{ item.date_of_request }}</td>
                  <td>{{ item.experience }} years</td>
                  <td>{{ item.address }}, {{ item.pincode }}</td>
                  <td><button class="btn text-light bg-dark p-2" style="border-radius: 5px;"
                      @click="downloadFile(item.document)">Download</button></td>
                  <td>
                    <span v-if="item.service_status == 'requested'">
                      Requested
                    </span>
                    <span v-else-if="item.service_status == 'assigned'">
                      <button class="btn text-light bg-danger p-2" style="border-radius: 5px;"
                        @click="showServiceCloseBlockFromeHome(item)">Close it?</button>
                    </span>
                    <span v-else>
                      Closed
                    </span>
                  </td>
                  <td>
                    <span v-if="item.service_status == 'closed'">{{ item.date_of_completion }}</span>
                    <span v-else>Not Closed</span>
                  </td>
                  <td>
                    <button class="btn text-dark bg-warning p-2" style="border-radius: 5px;"
                    @click="updateServiceHistoryCustomerPopup(item)">Update</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else class="card p-4">
          <div class="p-3 rounded">
            <p class="my-auto">You haven't booked any service yet. Book now under <strong>Looking For</strong> section
              above.</p>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- Show Service Popup -->
  <div v-if="showServiceDetails" class="modal-overlay" @click.self="hidePopup">
    <div class="modal-content scrollbar-primary w-75">
      <span class="close-btn" @click="hidePopup">&times;</span>

      <div>
        <div v-if="showAll">
          <h2>{{ selectedService }}</h2>

          <p><b>Price:</b> {{ selectedServiceDetail.price }}
            <br> <b>Time Required:</b> {{ selectedServiceDetail.time_required }}
            <br> <b>Service Description:</b> {{ selectedServiceDetail.description }}
          </p>
          <div v-if="(selectedServiceDetail.professionals?.length) > 0">
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Name</th>
                  <th scope="col">Experience</th>
                  <th scope="col">Address</th>
                  <th scope="col">Document</th>
                  <th scope="col">Book</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in selectedServiceDetail.professionals" :key="index">
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ item.name }}</td>
                  <td>{{ item.experience }} years</td>
                  <td>{{ item.address }}, {{ item.pincode }}</td>
                  <td><button class="btn text-light bg-dark p-2" style="border-radius: 5px;"
                      @click="downloadFile(item.document)">Download</button></td>
                  <td>
                    <span v-if="item.service_status == 'requested'">
                      Requested
                    </span>
                    <span v-else-if="item.service_status == 'assigned'">
                      <button class="btn text-light bg-danger p-2" style="border-radius: 5px;"
                        @click="showServiceCloseBlock(item)">Close it?</button>
                    </span>
                    <span v-else-if="item.service_status == 'closed'">
                      Closed
                    </span>
                    <span v-else>
                      <button class="btn text-light bg-dark p-2" style="border-radius: 5px;"
                        @click="bookProfessional(item.id)">Book</button>
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>

          </div>
          <div v-else>There are no professionals avaiable for this as of now. Please try again later.</div>
        </div>
        <div v-else>
          <h2>Service Remarks</h2>
          <div class="d-flex flex-wrap container">
            <div class="m-2 p-2 col-md-2 card"><b>Service Name:</b> 
              <span v-if="selectedServiceDetail.service">{{ selectedServiceDetail.service }} </span>
              <span v-else>{{ selectedServiceForClose.service_name }}</span>
            </div>
            <div class="m-2 p-2 col-md-2 card"><b>Description:</b> <span v-if="selectedServiceDetail.service">{{ selectedServiceDetail.service }} </span>
              <span v-else>{{ selectedServiceForClose.service_description }}</span>
            </div>
            <div class="m-2 p-2 col-md-2 card"><b>Date of Request:</b> {{ selectedServiceForClose.date_created }}</div>
            <div class="m-2 p-2 col-md-2 card"><b>Professional ID:</b> {{ selectedServiceForClose.id }}</div>
            <div class="m-2 p-2 col-md-2 card"><b>Professional Name:</b> {{ selectedServiceForClose.name }}</div>
          </div>
          <div class="container">

            <form v-if="selectedServiceForClose.service_request_id" @submit.prevent=" closeServiceBooking(selectedServiceForClose.service_request_id)">
              <div class="form-group">
                <label for="rating">Rating</label>
                <input v-model="rating.rating" type="number" class="form-control" id="rating" placeholder="Enter rating"
                  required>
              </div>
              <div class="form-group">
                <label for="remarks">Remarks (If any)</label>
                <input v-model="rating.remarks" type="text" class="form-control" id="remarks"
                  placeholder="Enter remarks">
              </div>
              <button type="submit" class="mt-2 btn btn-dark btn-block">Submit</button>
              <button v-if="!home" @click="hideServiceCloseBlock()"
                class="mt-2 mx-2 btn btn-danger btn-block">Back</button>
            </form>
            <form v-else @submit.prevent=" closeServiceBooking(selectedServiceForClose.service_request_id)">
              <div class="form-group">
                <label for="rating">Rating</label>
                <input v-model="rating.rating" type="number" class="form-control" id="rating" placeholder="Enter rating"
                  required>
              </div>
              <div class="form-group">
                <label for="remarks">Remarks (If any)</label>
                <input v-model="rating.remarks" type="text" class="form-control" id="remarks"
                  placeholder="Enter remarks">
              </div>
              <button type="submit" class="mt-2 btn btn-dark btn-block">Submit</button>
              <button v-if="!home" @click="hideServiceCloseBlock()"
                class="mt-2 mx-2 btn btn-danger btn-block">Back</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Show Service Update Popup -->
  <div v-if="showServiceUpdate" class="modal-overlay" @click.self="hidePopup">
    <div class="modal-content scrollbar-primary w-75">
      <span class="close-btn" @click="hidePopup">&times;</span>

      <div>
         <h2>{{ selectedServiceForUpdation.service_name }}</h2>
         <div class="d-flex flex-wrap container">
                    <div class="m-2 p-2 col-md-2 card"><b>Professional Name:</b> {{ selectedServiceForUpdation.name }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Date of Request:</b> {{ selectedServiceForUpdation.date_of_request }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Service Name:</b> {{ selectedServiceForUpdation.service_name
                        }}</div>
                    <div class="m-2 p-2 col-md-2 card"><b>Status:</b> {{ selectedServiceForUpdation.service_status }}</div>
                </div>
         <form @submit.prevent="updateServiceHistoryCustomer(selectedServiceForUpdation.service_id)">
              <div class="form-group">
                <label for="date_of_request">Date of Request</label>
                <input v-model="date_of_request" type="date" class="form-control" id="rating" placeholder="Enter date"
                  required>
              </div>
              <button type="submit" class="mt-2 btn btn-dark btn-block">Submit</button>
            </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'UserPortal',
  data() {
    return {
      all_services_name_list: '',
      selectedService: '',
      selectedServiceDetail: '',
      showServiceDetails: false,
      showServiceUpdate: false,
      showAll: true,
      selectedServiceForClose: '',
      rating: {
        remarks: null,
        rating: null,
      },
      allServices: '',
      home: false,
      isSearchServices: false,
      serviceSearch: '',
      filteredServices: '',
      selectedServiceForUpdation: '',
      date_of_request: '',
      authToken : '',
      showBanner: false,
    };
  },
  computed: {
    ...mapGetters(['alertMessage']),

  },
  async mounted() {
    await this.authTokenAssign();
    await this.getAllServiceTypesName();
    await this.allServicesbyUser();

  },
  methods: {
    async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
    async updateServiceHistoryCustomer(item_id) {
            try {
                const dict = {
                    id: item_id,
                    date_of_request: this.date_of_request,
                };
                const response = await fetch('http://localhost:8080/api/updateServiceHistoryCustomer', {
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
                    await this.allServicesbyUser();
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

    async deleteServiceHistoryCustomer(item_id) {
            try {
                const response = await fetch(`http://localhost:8080/api/deleteServiceHistoryCustomer/${item_id}`, {
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
                    await this.allServicesbyUser();
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

    serviceSearchFilter() {
            const query = this.serviceSearch.toLowerCase();
            this.filteredServices = this.allServices.filter(item => {
                const nameMatches = item.name && item.name.toLowerCase().includes(query);
                const service_statusMatches = item.service_status && item.service_status.toLowerCase().includes(query);
                const addressMatches = item.address && item.address.toLowerCase().includes(query);
                const experienceMatches = item.experience !== undefined && item.experience.toString().includes(query);
                const pincodeMatches = item.pincode !== undefined && item.pincode.toString().includes(query);

                return nameMatches || service_statusMatches || addressMatches || experienceMatches || pincodeMatches; // Use OR to match any field
            });

            
        },
        activateSearchServices() {
            this.isSearchServices = true;
        },
        disableSearchServices() {
            this.isSearchServices = false;
        },
    showBannerFor3Seconds() {
      this.showBanner = true;
      setTimeout(() => {
        this.showBanner = false;
        this.removeNotification()
      }, 3000);
    },
    async showServicePopup(service) {
      this.selectedService = service;
      this.showServiceDetails = true;
      await this.getServiceDetails(service);
    },

    async showServiceCloseBlockFromeHome(item) {
      this.showAll = false;
      this.home = true;
      this.showServiceDetails = true;
      this.selectedServiceForClose = item;
    },

    async updateServiceHistoryCustomerPopup(item) {
      this.showServiceUpdate = true;
      this.selectedServiceForUpdation = item;
    },

    async showServiceCloseBlock(item) {
      this.home = false;
      this.showAll = false;
      this.selectedServiceForClose = item;
    },
    async hideServiceCloseBlock() {
      this.showAll = true;
      this.home = false;
      this.selectedServiceForClose = '';

    },
    async hidePopup() {
      this.showServiceUpdate=false;
      this.showServiceDetails = false;
      this.showAll = true;
      this.selectedService = '';
      this.selectedServiceDetail = '';
      await this.allServicesbyUser();
    },
    downloadFile(filePath) {
      // Replace 'your-backend-url' with your actual backend address
      const downloadUrl = `http://localhost:8080/download/${filePath}`;
      
      // Trigger file download by opening the URL in a new tab
      window.open(downloadUrl, '_blank');
    },
    async getServiceDetails(service) {
      try {
        if (this.authToken) {
          const response = await fetch(`http://localhost:8080/api/getServiceDetails/${service}`, {
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
          
          await this.clearCache();
          this.selectedServiceDetail = data;
        }
      } catch (error) {
        var alertMessage = {
          "Alert": 'An error occurred, Service details fetching failed',
        };
        this.$store.dispatch('updateAlertMessage', alertMessage);
        this.showBannerFor3Seconds();
      }
    },
    async getAllServiceTypesName() {
      try {
        if (this.authToken) {
          const response = await fetch('http://localhost:8080/api/getAllServiceTypesName', {
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
          
          this.all_services_name_list = data.services;
        }
      } catch (error) {
        var alertMessage = {
          "Alert": 'An error occurred, Service types fetching failed',
        };
        this.$store.dispatch('updateAlertMessage', alertMessage);
        this.showBannerFor3Seconds();
      }
    },
    async allServicesbyUser() {
      try {
        if (this.authToken) {
          const response = await fetch('http://localhost:8080/api/allServicesbyUser', {
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
          
          this.allServices = data;
        }
      } catch (error) {
        var alertMessage = {
          "Alert": 'An error occurred, Services fetching failed',
        };
        this.$store.dispatch('updateAlertMessage', alertMessage);
        this.showBannerFor3Seconds();
      }
    },
    async bookProfessional(item_id) {
      try {
        const professionalData = {
          professional_id: item_id,
        };

        const response = await fetch('http://localhost:8080/api/bookProfessional', {
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
          await this.clearCache();
          await this.getServiceDetails(this.selectedService);

        } else {
          var alertMessage = {
            "Alert": data,
          };
        }
        this.$store.dispatch('updateAlertMessage', alertMessage);
      } catch (error) {
        var alertMessage = {
          "Alert": `An Error Occurred,booking failed`,
        };
        this.$store.dispatch('updateAlertMessage', alertMessage);
      }
      this.showBannerFor3Seconds();
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
    async closeServiceBooking(item_id) {
      try {
        const serviceRequest = {
          service_request_id: item_id,
          ratingDict: this.rating,
        };

        const response = await fetch('http://localhost:8080/api/closeServiceBooking', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
          body: JSON.stringify(serviceRequest),
        });

        const data = await response.json();
        if (response.ok) {
          var alertMessage = {
            "Notification": data,
          };
          await this.getServiceDetails(this.selectedService);
          await this.hideServiceCloseBlock();
        } else {
          var alertMessage = {
            "Alert": data,
          };
        }
        this.$store.dispatch('updateAlertMessage', alertMessage);
      } catch (error) {
        var alertMessage = {
          "Alert": `An Error Occurred,booking cancelling failed`,
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

  .albums {
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


.itemBlockClickable:hover {
  background-color: #ffffd1;
  /* width: 30% !important; */
  cursor: pointer;
}
</style>