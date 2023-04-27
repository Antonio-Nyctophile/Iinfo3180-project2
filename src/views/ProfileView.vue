<script setup>
    import ProfileHeader from "@/components/ProfileHeader.vue";
    import { ref, onMounted } from "vue";
    import { useRoute } from 'vue-router'
    const route = useRoute();

    let current_user_id = ref("");
    let jwt_token = ref("");
    let csrf_token = ref("");
    let current_user_info = ref({});
    let posts = ref([]);
    let profile_id = ref("");
    profile_id.value = route.params.id;

    onMounted(() => {
        getCsrfToken();
        getUserId();
        getJWTToken();
    })
    
    let loadProfileHeader = () => {
        fetch(`/api/v1/users/${profile_id.value}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrf_token.value,
                Authorization: 'Bearer ' + jwt_token.value,
            }
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            for(let d in data){
                current_user_info.value[d] = data[d]
            }
            posts.value = current_user_info.value["posts"];
            console.log(posts.value)
        }).catch(function (error) {
            console.log(error);
        });
    }

    function getCsrfToken(){
        fetch('/api/v1/csrf-token')
            .then((response) => response.json())
            .then((data) => {
                csrf_token.value = data.csrf_token;
            })
    }

    let getUserId = () => {
        fetch('/api/v1/authenticated')
        .then((response) => response.json())
        .then((data) => {
            current_user_id.value = data.id;
            loadProfileHeader()
        })
    }

    let getJWTToken = () => {
        fetch('/api/v1/jwt-token')
        .then((response) => response.json())
        .then((data) => {
            jwt_token.value = data.jwt_token;
        })
    }
</script>

<template>
    <ProfileHeader></ProfileHeader>
<div class="profile-uploads">
    <div v-for="post in posts" class="uploaded-img-container">
        <img class="uploaded-img" :src="post.photo" alt="">
    </div>
</div>
</template>

