<script setup>
import { RouterLink } from "vue-router";
import { onMounted, onUnmounted } from "vue";
import router from "../router/index";

onMounted(() => {
  const logoutLoginBtn = document.querySelector("#header-logout-login-btn");
  // const loginBtn = document.querySelector("#header-login-btn");
  


  // loginBtn.addEventListener('click', () => {
  //   logoutBtn.style.display = 'block';
  //   loginBtn.style.display = 'none';
  // })
    
  let isLoggedIn = () => {
    fetch('/api/v1/authenticated')
    .then((response) => response.json())
    .then((data) => {
    console.log(data.logged_in);

    if(data.logged_in){
      logoutLoginBtn.textContent = 'Logout';
      logoutLoginBtn.addEventListener('click', () => {
        fetch('/api/v1/auth/logout')
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
        })
      })
    } else{
      logoutLoginBtn.textContent = 'Login'
      logoutLoginBtn.addEventListener('click', () => {
        router.push('/login')
      })
    }

    })
  }

  // isLoggedIn()

})
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
                <RouterLink class="nav-link" to="/profile">My Profile</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/" id="header-logout-login-btn">Login</RouterLink>
              </li>
            </div>
        </ul>
      </nav>
  </header>
</template>

