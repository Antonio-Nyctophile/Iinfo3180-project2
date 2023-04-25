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
                <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
              </li>
            </div>
        </ul>
      </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>