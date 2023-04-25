<script setup>
    import { ref, onMounted } from "vue";

    onMounted(() => {
        getCsrfToken();
    });

    let csrf_token = ref("");

    function getCsrfToken(){
        fetch('/api/v1/csrf-token')
            .then((response) => response.json())
            .then((data) => {
                csrf_token.value = data.csrf_token;
            })
    }
    let makePost = () => {
        let postForm = document.querySelector('#postForm');
        let form_data = new FormData(postForm);
        fetch("/api/v1/auth/login", {
            method: 'POST',
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value
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