// Instantiate Vue Application
const app = new Vue({
    vuetify: new Vuetify(), //TODO: lag en egen vuetify.js fil for konfig tilhørende vuetify (options object)
    router,
    store
}).$mount('#app');