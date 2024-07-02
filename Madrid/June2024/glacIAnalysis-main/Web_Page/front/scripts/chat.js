document.addEventListener('DOMContentLoaded', (event) => {
          const input = document.getElementById('chat-input');
          const sendButton = document.getElementById('send-button');
          const responseElement = document.getElementById('response');
          const audioPlayer = document.getElementById('audioPlayer');

          sendButton.addEventListener('click', function (e) {
              e.preventDefault();
              const message = input.value.trim();
              if (message) {
                  responseElement.innerHTML = 'Procesando...';
                  fetch('https://webextendida.es/chatOso.php?question=' + encodeURIComponent(message), {
                      method: 'GET',
                      headers: {
                          'Content-Type': 'application/json',
                      }
                  })
                  .then(response => response.text())
                  .then(text => {
                      input.value = '';
                      responseElement.innerHTML = text;
                      const formData = new URLSearchParams();
                      formData.append('text', text);

                      // Definir la función async que hará la solicitud fetch
                      async function fetchAudio() {
                          try {
                              const response = await fetch('https://webextendida.es/chatOsoAudio.php', {
                                  method: 'POST',
                                  headers: {
                                      'Content-Type': 'application/x-www-form-urlencoded'
                                  },
                                  body: formData.toString()
                              });
                      
                              if (!response.ok) {
                                  throw new Error('Network response was not ok ' + response.statusText);
                              }
                      
                              const audioBlob = await response.blob();
                              const audioUrl = URL.createObjectURL(audioBlob);
                              audioPlayer.src = audioUrl;
                              audioPlayer.play();
                          } catch (error) {
                              console.error('Error generating audio:', error);
                          }
                      }

                      // Llamar la función async
                      fetchAudio();
                  })
                  .catch((error) => {
                      console.error('Error:', error);
                      responseElement.innerHTML = 'Ocurrió un error: ' + error.message;
                  });
              }
          });
      });

document.addEventListener('DOMContentLoaded', function () {
          const voiceInput = document.getElementById('chat-input');
          const microphoneButton = document.getElementById('microphoneButton');

          // Verifica si el navegador soporta la API de Web Speech
          if (!('webkitSpeechRecognition' in window)) {
              alert('Tu navegador no soporta la API de reconocimiento de voz.');
              return;
          }

          const recognition = new webkitSpeechRecognition();
          recognition.continuous = false;
          recognition.interimResults = false;
          recognition.lang = 'es-ES';

          recognition.onstart = function() {
              microphoneButton.textContent = '🎙️';
          };

          recognition.onend = function() {
              microphoneButton.textContent = '🎤';
          };

          recognition.onresult = function(event) {
              const transcript = event.results[0][0].transcript;
              voiceInput.value = transcript;
          };

          microphoneButton.addEventListener('click', function () {
              recognition.start();
          });
      });