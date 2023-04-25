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
                console.log(data)
            })
    }
    let loginUser = () => {
        let loginForm = document.querySelector('#loginForm');
        let form_data = new FormData(loginForm);
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
    <form @submit.prevent="loginUser" enctype="multipart/form-data" id="loginForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" name="username" class="formcontrol">
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" name="password" class="formcontrol">
            </div>
           
            <div class="form-group">
                <button type="submit" class="btn btn-register">Login</button>
            </div>
    </form>
</template>