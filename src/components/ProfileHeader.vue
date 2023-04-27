<script setup>
    import { ref, onMounted } from "vue";
     import { useRoute } from 'vue-router'
    const route = useRoute();

    let profile_id = ref("");
    profile_id.value = route.params.id;

    onMounted(() => {
        getCsrfToken();
        getUserId();
        getJWTToken();

        const followBtn = document.querySelector("#follow-btn");
        const alert = document.querySelector("#alert");
        followBtn.addEventListener('click', () => {
            if(followBtn.classList.contains('btn-register')){
                followBtn.classList.remove('btn-register')
                followBtn.classList.add('btn-login')
                followBtn.textContent = 'Follow'
            } else{
                followBtn.classList.remove('btn-login')
                followBtn.classList.add('btn-register')
                followBtn.textContent = 'Following'
                fetch(`/api/v1/users/${profile_id.value}/follow`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrf_token.value,
                        Authorization: 'Bearer ' + jwt_token.value,
                    }
                    }).then(function (response) {
                        return response.json();
                    }).then(function (data) {
                    // display a success message
                        console.log(data);
                        alert.style.display = 'block'
                        alert.textContent = data.message ? data.message : data.errors[0]
                    }).catch(function (error) {
                        console.log(error);
                    });
            }
        })
    });

    let current_user_id = ref("");
    let jwt_token = ref("");
    let csrf_token = ref("");
    let current_user_info = ref({});
    let num_posts = ref("");

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
            num_posts.value = current_user_info.value['posts'].length;
        }).catch(function (error) {

        });
    }
</script>

<template>
    <div class="alert" id="alert"></div>
    <div class="photo-card profile-header">
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
                    <p class="num-followers stats-count">{{ current_user_info['followers'] }}</p>
                    <p class="stats-label">Followers</p>
                </div>
            </div>

            <div class="btn btn-login" id="follow-btn">Follow</div>
        </div>
    </div>
</template>