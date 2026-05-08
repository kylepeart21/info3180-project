<script>
    import RegisterForm from '../components/Register.vue';

    export default {
    name: 'RegisterView',
    components: {
        RegisterForm
    },
    };
</script>

<template>
    <div class="add-container">
      <h1>Register Account</h1>
      <RegisterForm />
    </div>
</template>
  

  
<style scoped>
    .add-container {
    max-width: 600px;
    margin: auto;
    padding: 50px;
    min-height: 80vh;
    }
</style>