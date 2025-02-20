<template>
    <div class="container scrollbar-primary">
        <div class="jumbotron d-flex flex-column flex-wrap">
            <div class="p-3 m-auto">
                <li style="font-size: 1.3rem;">Service Requests</li>

                <img class="content" :src="serviceRequestChartImageUrl" alt="Bar Chart" />
            </div>

        </div>
    </div>
</template>
  
<script>
import { mapGetters, mapState } from 'vuex';

export default {
    name: 'summaryPage',
    data() {
        return {
            authToken : '',
            serviceRequestChartImageUrl: '',
        };
    },
    computed: {
        ...mapGetters(['alertMessage']),
        },
    async mounted() {
        await this.authTokenAssign();
        await this.loadChartServiceRequests();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        async loadChartServiceRequests() {
            try {
                const response = await fetch('http://localhost:8080/api/loadChartServiceRequests', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.authToken, 
                    },
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const imageBlob = await response.blob();
                this.serviceRequestChartImageUrl = URL.createObjectURL(imageBlob);
            } catch (error) {
                console.error('Error loading chart image:', error);
            }
        },
    },
};
</script>
  
<style scoped>

.content {
    width: 100%;
}

@media (max-width: 600px) {
    .content {
        width: max-content;
    }
}
</style>
  