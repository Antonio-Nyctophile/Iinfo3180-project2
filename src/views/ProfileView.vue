<script setup>
    import ProfileHeader from "@/components/ProfileHeader.vue";
    import { ref, onMounted } from "vue";
    import { useRoute } from 'vue-router'
    import { getCsrfToken, getUserId, getJWTToken } from "../assets/helper";

    const route = useRoute();

    let current_user_id = ref("");
    let jwt_token = ref("");
    let csrf_token = ref("");
    let current_user_info = ref({});
    let posts = ref([]);

    let profile_id = ref("");
    profile_id.value = route.params.id;

    let dataLoaded = ref(false);

    onMounted(async () => {
        let token = await getCsrfToken();
        csrf_token.value = token.csrf_token;

        let user_id = await getUserId();
        current_user_id.value = user_id.id;

        let jwt = await getJWTToken();
        jwt_token.value = jwt.jwt_token;

        loadProfileHeader()

        dataLoaded.value = true;
    })
    
    let loadProfileHeader = () => {
        const alert = document.querySelector("#alert");
        fetch(`/api/v1/users/${profile_id.value}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrf_token.value,
                Authorization: 'Bearer ' + jwt_token.value,
            }
        }).then((response) => {
            return {status: response.status, resp: response.json()};
        }).then(async (data) => {
            let response = await data.resp
            console.log(response)
            if(data.status != 401){
                for(let key in response){
                    current_user_info.value[key] = response[key]
                }
                posts.value = current_user_info.value["posts"];
            } else{
                alert.style.display = 'block'
                alert.textContent = "Authorization error. Please try logging in again. If the problem persists, contact your system administrator."
            }
        }).catch(function (error) {
            console.log(error);
        });
    }
</script>

<template>
    <div class="alert" id="alert"></div>
    <ProfileHeader v-if="dataLoaded"></ProfileHeader>
<div v-if="dataLoaded" class="profile-uploads">
    <div v-for="post in posts" class="uploaded-img-container">
        <img class="uploaded-img" :src="post.photo" alt="">
    </div>
</div>
</template>

