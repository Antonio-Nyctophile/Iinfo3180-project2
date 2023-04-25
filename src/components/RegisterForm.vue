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
    let saveUser = () => {
        let registerForm = document.querySelector('#registerForm');
        let form_data = new FormData(registerForm);
        fetch("api/v1/register", {
            method: 'POST',
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value
            }
        }).then(function (response) {
            console.log(response)
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
    <form @submit.prevent="saveUser" enctype="multipart/form-data" id="registerForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" name="username" class="formcontrol">
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" name="password" class="formcontrol">
            </div>
            <div class="form-group">
                <label for="first_name">First Name</label>
                <input type="text" name="first_name" class="formcontrol">
            </div>
            <div class="form-group">
                <label for="last_name">Last Name</label>
                <input type="text" name="last_name" class="formcontrol">
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" name="email" class="formcontrol">
            </div>
            <div class="form-group">
                <label for="location">Location</label>
                <input type="text" name="location" class="formcontrol">
            </div>
            <div class="form-group">
                <label for="bio">Biography</label>
                <input type="text" name="bio" class="formcontrol">
            </div>
            <div class="form-group">
                <label for="photo">Photo</label>
                <input type="file" name="photo" class="formcontrol" accept="image/*">
            </div>
            <div class="form-group">
                <button type="submit" class="btn btn-register">Register</button>
            </div>
    </form>
</template>