<script setup>
    import ProfileHeader from "@/components/ProfileHeader.vue";

    import { onMounted, onUnmounted } from "vue";
    onMounted(() => {
        const followBtn = document.querySelector("#follow-btn");
        followBtn.addEventListener('click', () => {
            if(followBtn.classList.contains('btn-register')){
                followBtn.classList.remove('btn-register')
                followBtn.classList.add('btn-login')
                followBtn.textContent = 'Follow'
            } else{
                followBtn.classList.remove('btn-login')
                followBtn.classList.add('btn-register')
                followBtn.textContent = 'Following'
            }
        })
    })
</script>

<template>
    <ProfileHeader></ProfileHeader>
<div class="profile-uploads">
    <div class="uploaded-img-container">
        <img class="uploaded-img" src="@/assets/images/temp-imgs/one.jpg" alt="">
    </div>
    <div class="uploaded-img-container">
        <img class="uploaded-img" src="@/assets/images/temp-imgs/seven.jpg" alt="">
    </div>
    <div class="uploaded-img-container">
        <img class="uploaded-img" src="@/assets/images/temp-imgs/one.jpg" alt="">
    </div>
    <div class="uploaded-img-container">
        <img class="uploaded-img" src="@/assets/images/temp-imgs/two.jpg" alt="">
    </div>
    <div class="uploaded-img-container">
        <img class="uploaded-img" src="@/assets/images/temp-imgs/three.jpg" alt="">
    </div>
    <div class="uploaded-img-container">
        <img class="uploaded-img" src="@/assets/images/temp-imgs/four.jpg" alt="">
    </div>
    <div class="uploaded-img-container">
        <img class="uploaded-img" src="@/assets/images/temp-imgs/five.jpg" alt="">
    </div>
</div>
</template>

