<script setup>
    import { ref, onMounted } from "vue";
    import router from "../router/index";

    onMounted(() => {
        getCsrfToken();
        getUserId();
        getJWTToken();
    });

    let csrf_token = ref("");
    let current_user_id = ref("");
    let jwt_token = ref("");

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
            current_user_id.value = data.current_user_id;
        })
    }
    let getJWTToken = () => {
        fetch('/api/v1/jwt-token')
        .then((response) => response.json())
        .then((data) => {
            jwt_token.value = data.jwt_token;
        })
    }

    let makePost = () => {
        let postForm = document.querySelector('#postForm');
        let form_data = new FormData(postForm);
        fetch(`/api/v1/users/${current_user_id.value}/posts`, {
            method: 'POST',
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value,
                Authorization: 'Bearer ' + jwt_token.value,
            }
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
        // display a success message
            router.push('/explore');
            console.log(data);
        }).catch(function (error) {
            console.log(error);
        });
    }
</script>

<template>
    <form @submit.prevent="makePost" enctype="multipart/form-data" id="postForm">
            <div class="form-group">
                <label for="photo">Photo</label>
                <input type="file" name="photo" class="formcontrol" accept="image/*">
            </div>
            <div class="form-group">
                <label for="caption">Caption</label>
                <input type="text" name="caption" class="formcontrol">
            </div> 
            <div class="form-group">
                <button type="submit" class="btn btn-register">Submit</button>
            </div> 
        </form>
</template>