<template>
    <div class="container border w-85 mt-5 p-4">
        <h1>Logout successful</h1>
    </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';

export default {
    name: 'logout',
    data() {
        return {
            showsBooked: '',
            authToken : '',
        };
    },

    async mounted() {
        await this.authTokenAssign();
        await this.logout();
    },
    methods: {
        async authTokenAssign() {
            this.authToken = localStorage.getItem('authToken');
        },
        async logout() {
            try {
                const response = await fetch('http://localhost:8080/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    localStorage.removeItem('authToken');
                    this.$store.dispatch('setAuthentication', false);
                    this.$router.push('/');
                } else {
                    console.error('Logout failed:', response.statusText);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },
    },
};
</script>