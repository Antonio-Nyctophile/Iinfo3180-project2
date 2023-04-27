<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted, onUnmounted, onUpdated } from "vue";
import router from "../router/index";


let logged_in = ref("");
let current_user_id = ref("");

onMounted(() => {
  isLoggedIn();
  getCsrfToken();
  getUserId();
})

let csrf_token = ref("");


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
        })
    }
onUpdated(() => {
  isLoggedIn()

  if(logged_in.value === true){
    const logoutBtn = document.querySelector("#logout-btn");
    logoutBtn.addEventListener('click', () => {
      fetch('/api/v1/auth/logout', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrf_token.value
        }
      }).then((response) => {
        return response.json
      }).then((data) => {
        console.log(data)
      }).catch((error) => {
        console.log(error)
      })
  
    })
  } else {
    const loginBtn = document.querySelector("#login-btn");
    loginBtn.addEventListener('click', () => {
      router.push('/login')
    })
 
  }
})

const isLoggedIn = () => {
  fetch('/api/v1/authenticated')
  .then((response) => response.json())
  .then((data) => {
    logged_in.value = data.logged_in
  })
}
</script>

<template>
  <header>
      <nav>
        <ul>
            <div class="logo">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/"><span><i class="fa-solid fa-camera-retro camera-icon"></i></span>Photogram</RouterLink>
              </li>
            </div>
            <div class="secondary-navs">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/">Home</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" :to="'/users/' + current_user_id">My Profile</RouterLink>
              </li>
              <li v-if="logged_in==true" class="nav-item">
                <RouterLink class="nav-link" to="/" id="logout-btn">Logout</RouterLink>
              </li>
              <li v-else class="nav-item">
                <RouterLink class="nav-link" to="/" id="login-btn">Login</RouterLink>
              </li>
            </div>
        </ul>
      </nav>
  </header>
</template>

