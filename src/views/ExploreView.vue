<script setup>
    import { ref, onMounted } from "vue";

    let posts = ref([]);
    let logged_in = ref("");
    let csrf_token = ref("");
    let jwt_token = ref("");

    onMounted(() => {
        fetchPosts();
        isLoggedIn();
        getCsrfToken();
        getJWTToken();
    });

    const likePost = (postID) => {
        fetch(`/api/v1/posts/${postID}/like`, {
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
                }).catch(function (error) {
                    console.log(error);
                });
    }

    const fetchPosts = () => {
        fetch('/api/v1/posts')
        .then((response) => response.json())
        .then((data) => {
            for(const post of data){
                posts.value.push(post)
            }
        })
    }

    function getCsrfToken(){
        fetch('/api/v1/csrf-token')
            .then((response) => response.json())
            .then((data) => {
                csrf_token.value = data.csrf_token;
            })
    }

    let getJWTToken = () => {
        fetch('/api/v1/jwt-token')
        .then((response) => response.json())
        .then((data) => {
            jwt_token.value = data.jwt_token;
        })
    }


    const isLoggedIn = () => {
        fetch('/api/v1/authenticated')
        .then((response) => response.json())
        .then((data) => {
            logged_in.value = data.logged_in
        })
    }
</script>


<template>
    <div class="explore-page">
    <div class="explore-container">
        
        <div v-for="post in posts" class="photo-card explore-card">
            <div class="explore-header">
                <span><i class="fa-solid fa-user-astronaut"></i></span>
                <RouterLink :to="'/users/' + post.user_id"><p class="explore-username">{{ post.username }}</p></RouterLink>
            </div>
            <img :src="post.photo" alt="">
            <div class="explore-footer">
                <p class="explore-desc">{{ post.caption }}</p>
                <div class="explore-stats">
                    <div class="explore-likes">
                        <span><i class="fa-regular fa-heart like-post-btn" id="like-post" @click="likePost(post.id)"></i></span>
                        <p class="explore-num-likes">{{ post.likes }}</p>
                    </div>
                    <p class="explore-date">{{ post.created_on }}</p>
                </div>
            </div>
        </div>

    </div>

    <button class="btn btn-login explore-btn"><RouterLink to="/post">New Post</RouterLink></button>
</div>
</template>