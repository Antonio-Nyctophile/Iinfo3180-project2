<script setup>
    import { ref, onMounted } from "vue";
    import { getCsrfToken, getUserId, getJWTToken } from "../assets/helper";

    let logged_in = ref("");
    let current_user_id = ref("");
    let csrf_token = ref("");
    let jwt_token = ref("");
    let posts = ref([]);

    let dataLoaded = ref(false);

    onMounted(async () => {
        let token = await getCsrfToken();
        csrf_token.value = token.csrf_token;

        let jwt = await getJWTToken();
        jwt_token.value = jwt.jwt_token;

        let user_id = await getUserId();
        current_user_id.value = user_id.id;
        logged_in.value = user_id.logged_in

        fetchPosts()

        console.log(posts.value)
        
        dataLoaded.value = true;
    });

    const likePost = (postID) => {
        const alert = document.querySelector("#alert");
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
                    alert.style.display = 'block'
                    alert.textContent = data.message ? data.message : data.errors[0]
                }).catch(function (error) {
                    console.log(error);
                });
    }

    const fetchPosts = () => {
        fetch('/api/v1/posts', {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrf_token.value,
                Authorization: 'Bearer ' + jwt_token.value,                
            }
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            for(const post of data){
                posts.value.push(post)
            }
        })
    }

    let checkLiked = (post) => {
        for(let like of post.likes){
            if(like.user_id == current_user_id.value){
                return true
            }
        }
        return false
    }

</script>


<template>
    <div class="alert" id="alert"></div>
    <div v-if="dataLoaded" class="explore-page">
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
                            <span v-if="checkLiked(post)"><i class="fa-regular fa-heart like-post-btn liked" id="like-post"></i></span>
                            <span v-else><i class="fa-regular fa-heart like-post-btn" id="like-post" @click="likePost(post.id)"></i></span>
                            <p class="explore-num-likes">{{ post.likes.length }}</p>
                        </div>
                        <p class="explore-date">{{ post.created_on }}</p>
                    </div>
                </div>
            </div>
        </div>
    <button class="btn btn-login explore-btn"><RouterLink to="/posts/new">New Post</RouterLink></button>
</div>
</template>