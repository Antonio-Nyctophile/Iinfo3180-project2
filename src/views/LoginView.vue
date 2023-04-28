<script setup>
    import LForm from "@/components/LoginForm.vue";

    import { ref, onMounted } from "vue";
    import {getCsrfToken, getUserId} from "../assets/helper";

    let csrf_token = ref("");
    let logged_in = ref("");

    let dataLoaded = ref(false);

    onMounted(async () => {
        let token = await getCsrfToken();
        csrf_token.value = token.csrf_token;

        let user_id = await getUserId();
        logged_in.value = user_id.logged_in;

        dataLoaded.value = true;
    });
</script>

<template>
    <div v-if="!logged_in" class="photo-container photo-container-login">
        <p class="photo-title">Login</p>
        <div class="photo-card photo-card-solid">
            <LForm></LForm>
        </div>
    </div>
    <div v-else class="photo-container photo-container-login">
    <div class="logged-in-icon"><i class="fa-solid fa-square-check" style="color: #7fd220;"></i></div>
    <p class="logged-in-text">You are already logged in. <br>
        Click <RouterLink to="/logout" class="logout-link">here</RouterLink> to log out.</p>
    </div>
</template>