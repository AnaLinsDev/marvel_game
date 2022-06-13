<template>
  <v-app dark>
    <Menu />
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer
      :absolute="!fixed"
      app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import Menu from '@/components/common/Menu.vue'
export default {
  name: 'DefaultLayout',
  components: { Menu }
}
</script>
