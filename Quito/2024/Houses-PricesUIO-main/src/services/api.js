export async function fetchRecommendations(inputValue) {
  try {
    console.log("Preparando solicitud a LangFlow con:", inputValue); // Depuración
    const response = await fetch(
      "http://127.0.0.1:7860/api/v1/run/33b89d7d-4a4e-4be5-b837-16062fee63a3?stream=false",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          input_value: inputValue, // Texto ingresado por el usuario
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`Error en la respuesta del servidor: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Respuesta cruda del backend:", data); // Depuración

    // Formatear el texto crudo del backend
    const formattedText = formatText(data.outputs[0]?.outputs[0]?.results?.message?.text || "");
    return formattedText;
  } catch (error) {
    console.error("Error al interactuar con LangFlow:", error);
    throw error;
  }
}

// Función para formatear el texto
function formatText(rawText) {
  return rawText
    .replace(/["“”]/g, "") // Elimina comillas dobles o tipográficas
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>") // Convierte **texto** en <strong>texto</strong>
    .replace(/\* (.+?)(?=\n|$)/g, "<li>$1</li>") // Convierte "* texto" en <li>texto</li>
    .replace(/(<li>.*?<\/li>)/g, "<ul>$1</ul>") // Encierra <li> en listas <ul>
    .replace(/\n/g, "<br>") // Reemplaza saltos de línea con <br>
    .replace(/\s+/g, " ") // Reemplaza espacios múltiples por uno solo
    .trim(); // Elimina espacios iniciales y finales
}

