<template>
    <div class="container scrollbar-primary">
        <div class="jumbotron d-flex flex-column flex-wrap">
            <div class="p-3 m-auto">
                <li style="font-size: 1.3rem;">Service Requests</li>

                <img class="content" :src="serviceRequestChartImageUrl" alt="Bar Chart" />
            </div>
            <div class="p-3 m-auto">
                <li style="font-size: 1.3rem;">Review/Ratings</li>

                <img class="content" :src="reviewRatingChartImageUrl" alt="Pie Chart" />
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
            serviceRequestChartImageUrl: '',
            reviewRatingChartImageUrl: '',
            authToken : '',
        };
    },
    computed: {
        ...mapGetters(['alertMessage']),

    },
    async mounted() {
        await this.authTokenAssign();
        await this.loadChartServiceRequestsProfessional();
        await this.loadChartReviewRatingProfessional();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        async loadChartServiceRequestsProfessional() {
            try {
                const response = await fetch('http://localhost:8080/api/loadChartServiceRequestsProfessional', {
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
        async loadChartReviewRatingProfessional() {
            try {
                const response = await fetch('http://localhost:8080/api/loadChartReviewRatingProfessional', {
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
                this.reviewRatingChartImageUrl = URL.createObjectURL(imageBlob);
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
  