<script>
    import LoginForm from '../components/Login.vue';

    export default {
        name: 'LoginView',
        components: {
            LoginForm
        },
    };    
</script>

<template>
    <div class="add-container">
      <h1>Login</h1>
      <LoginForm />
    </div>
</template>
  

  
<style scoped>
    .add-container {
    max-width: 600px;
    margin: auto;
    padding: 100px;
    }
</style>