<template>
  <div class="page-container">
    <!-- Encabezado -->

    <header class="banner">
      <img src="@/assets/logoHousesP.png" alt="Logo" class="banner-image" />
      <h1 class="banner-title">Recomendador de adquisición de Inmuebles</h1>
    </header>

    <!-- Chatbox -->
    <section class="chatbox">
      <div class="messages-container">
        <div v-for="(message, index) in messages" :key="index"
        :class="['message', message.isUser ? 'user-message' : 'bot-message']">
          <p v-html="message.text"></p>
        </div>
      </div>

      <!-- Entrada del usuario -->
      <form @submit.prevent="sendMessage" class="chat-input-container">
        <input type="text" v-model="userInput" placeholder="Escribe aquí..." class="chat-input" />
        <button type="submit" class="chat-send-button">Enviar</button>
      </form>
    </section>

    <!-- Autores -->
    <section class="authors-section">
      <h2 class="authors-title">Autores</h2>
      <div class="authors-container">
        <div v-for="author in authors" :key="author.name" class="author-card">
          <img :src="author.image" alt="Author Photo" class="author-photo" />
          <h3 class="author-name">{{ author.name }}</h3>
          <p class="author-description">{{ author.description }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
// Importa la función desde el archivo `api.js`
import { fetchRecommendations } from "@/services/api";

export default {
  name: "PropertyRecommendation",
  data() {
    return {
      userInput: "", // Entrada del usuario
      messages: [
        { text: "¡Hola! Soy tu recomendador de inmuebles. ¿Qué características buscas?", isUser: false },
      ],
      authors: [
        { name: "Daniela Tupiza", description: "Ingeniería en Computación Gráfica.", image: require('@/assets/Daniela.png') },
        { name: "Esteven Pérez", description: "Economía", image: require('@/assets/Steven.jpg') },
        { name: "Salome Polanco", description: "Sistemas de la Información", image: require('@/assets/salome_polanco.jpg') },
        { name: "María Rosa Camacho", description: "Diseño Industrial", image: require('@/assets/mariaRosa.jpg') },
      ],

    };
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim()) {
        return;
      }

      // Agrega el mensaje del usuario al chat
      this.messages.push({ text: this.userInput, isUser: true });
      const userQuery = this.userInput;
      this.userInput = ""; // Limpia la entrada del usuario

      // Agrega un mensaje de carga
      this.messages.push({ text: "Buscando recomendaciones...", isUser: false });

      try {
        // Llama a la función para obtener recomendaciones desde LangFlow
        const botReply = await fetchRecommendations(userQuery);

        // Reemplaza el mensaje de carga con la respuesta del bot
        this.messages[this.messages.length - 1].text = botReply;
      } catch (error) {
        console.error("Error al obtener recomendaciones:", error);
        this.messages[this.messages.length - 1].text = "Hubo un problema al conectar con LangFlow. Intenta nuevamente.";
      }
    },
  },
};
</script>