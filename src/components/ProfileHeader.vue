<script setup>
    import { ref, onMounted, onUpdated } from "vue";
    import { useRoute } from 'vue-router';
    import { getCsrfToken, getUserId, getJWTToken } from "../assets/helper";

    const route = useRoute();

    let profile_id = ref("");
    profile_id.value = route.params.id;

    let csrf_token = ref("");
    let current_user_id = ref("");
    let jwt_token = ref("");
    let following_flag = ref(false);

    let current_user_info = ref({});
    let num_posts = ref("");
    let num_followers = ref("");

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

    onUpdated(() => {
        const followBtn = document.querySelector("#follow-btn");
        const alert = document.querySelector("#alert");
        followBtn.addEventListener('click', () => {
            if(!following_flag.value){
                fetch(`/api/v1/users/${profile_id.value}/follow`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf_token.value,
                    Authorization: 'Bearer ' + jwt_token.value,
                }
                }).then(function (response) {
                    return {status: response.status, resp: response.json()};
                }).then(async (data) => {
                // display a success message
                    if(data.status == 201){
                        followBtn.classList.remove('btn-login')
                        followBtn.classList.add('btn-register')
                        followBtn.textContent = 'Following'
                    }
                    let response = await data.resp
                    alert.style.display = 'block'
                    alert.textContent = response.message ? response.message : response.errors[0]
                }).catch(function (error) {
                    console.log(error);
                })
            } else {
                alert.style.display = 'block'
                alert.textContent = "You are already following this user."
            }
        })
    })

    let loadProfileHeader = () => {
        fetch(`/api/v1/users/${profile_id.value}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrf_token.value,
                Authorization: 'Bearer ' + jwt_token.value,
            }
        }).then((response) => {
            return response.json();
        }).then((data) => {
            for(let key in data){
                current_user_info.value[key] = data[key]
            }

            for(let follower of current_user_info.value['followers']){
                console.log(follower.follower_id)
                console.log(current_user_id.value, 'd')
                if(follower.follower_id === current_user_id.value){
                    console.log('dd')
                    following_flag.value = true;
                } else {
                    following_flag.value = false;
                }
            }

            num_posts.value = current_user_info.value['posts'].length;
            num_followers.value = current_user_info.value['followers'].length;
           
        }).catch((error) => {
            console.log(error)
        });       
    }
</script>

<template>
    <div class="alert" id="alert"></div>
    <div v-if="dataLoaded" class="photo-card profile-header">
        <img :src="current_user_info['profile_photo']" alt="" class="profile-photo">
        
        <div class="profile-about">
            <p class="profile-name">{{ `${current_user_info['firstname']} ${current_user_info['lastname']}` }}</p>
            <div class="profile-more-info">
                <p class="profile-location">{{ current_user_info['location'] }}</p>
                <p class="profile-member">{{ `Member since ${current_user_info['joined_on']} `}}</p>
            </div>
            <div class="profile-bio">
                <p>{{ current_user_info['biography'] }}</p>
            </div>
        </div>

        <div class="profile-stats">
            <div class="posts-and-followers">
                <div class="posts">
                    <p class="num-posts stats-count">{{ num_posts }}</p>
                    <p class="stats-label">Posts</p>
                </div>
                <div class="followers">
                    <p class="num-followers stats-count">{{ num_followers }}</p>
                    <p class="stats-label">Followers</p>
                </div>
            </div>
            {{ following_flag }}
            <div v-if="following_flag" class="btn btn-register" id="follow-btn">Following</div>
            <div v-else class="btn btn-login" id="follow-btn">Follow</div>
        </div>
    </div>
</template>