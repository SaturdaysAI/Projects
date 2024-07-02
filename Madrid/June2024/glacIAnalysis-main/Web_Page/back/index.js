import { exec } from "child_process";
import cors from "cors";
import dotenv from "dotenv";
import express from "express";
import fs from "fs";
import OpenAI from "openai";
import axios from "axios";

dotenv.config();

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY || "-",
});

const elevenLabsApiKey = process.env.ELEVEN_LABS_API_KEY;

const voiceID = "Nh2zY9kknu6z4pZy6FhD";

const app = express();
app.use(express.json());
app.use(cors());
const port = 3000;

app.get("/", (req, res) => {
    res.send("Hello World!");
});

app.get("/voices", async (req, res) => {
    try {
        const voices = await axios.get("https://api.elevenlabs.io/v1/voices", {
            headers: {
                'xi-api-key': elevenLabsApiKey,
            },
        });
        res.send(voices.data);
    } catch (error) {
        console.error("Error fetching voices:", error);
        res.status(500).send({ error: "Failed to fetch voices" });
    }
});

const execCommand = (command) => {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error("Error executing command:", error);
                return reject(error);
            }
            console.log(`Command executed successfully: ${command}`);
            resolve(stdout);
        });
    });
};

const generateAudio = async (text, fileName) => {
    const apiUrl = `https://api.elevenlabs.io/v1/text-to-speech/${voiceID}`;
    const payload = {
        text: text,
        voice_settings: {
            stability: 0,
            similarity_boost: 0
        },
          model_id: "eleven_multilingual_v2"
    };
    const headers = {
        'Content-Type': 'application/json',
        'xi-api-key': elevenLabsApiKey,
        'Accept': 'audio/mpeg'
    };

    try {
        const response = await axios.post(apiUrl, payload, { headers, responseType: 'stream' });
        const writer = fs.createWriteStream(fileName);
        response.data.pipe(writer);

        return new Promise((resolve, reject) => {
            writer.on('finish', resolve);
            writer.on('error', reject);
        });
    } catch (error) {
        console.error('Error generating audio:', error);
        if (error.response) {
            console.error('Error response data:', error.response.data);
        }
        throw error;
    }
};

const lipSyncMessage = async (messageIndex) => {
    const inputFilePath = `audios/message_${messageIndex}.mp3`;
    const outputFilePath = `audios/message_${messageIndex}.wav`;
    const jsonFilePath = `audios/message_${messageIndex}.json`;

    try {
        await fs.promises.access(inputFilePath);

        console.log(`Starting conversion for message_${messageIndex}`);
        await execCommand(`ffmpeg -y -i ${inputFilePath} ${outputFilePath}`);
        console.log(`Conversion done for message_${messageIndex}`);

        await execCommand(`/Users/Jorge/Desktop/Rhubarb-Lip-Sync-1.13.0-macOS/rhubarb -f json -o ${jsonFilePath} ${outputFilePath} -r phonetic`);
        console.log(`Lip sync done for message_${messageIndex}`);
    } catch (error) {
        console.error(`Error in lip sync for message_${messageIndex}:`, error);
        throw error;
    }
};

app.post("/chat", async (req, res) => {
    const userMessage = req.body.message;

    try {
        const completion = await openai.chat.completions.create({
            model: "gpt-3.5-turbo-1106",
            max_tokens: 1000,
            temperature: 0.6,
            response_format: {
                type: "json_object",
            },
            messages: [
                {
                    role: "system",
                    content: `
            You are a polar beard.
            You will always reply with a JSON array of messages. With a maximum of 3 messages.
            Each message has a text, facialExpression, and animation property.
            The different facial expressions are: smile, sad, angry, surprised, funnyFace, and default.
            The different animations are: Talking_0, Talking_1, Talking_2, Crying, Laughing, Rumba, Idle, Terrified, and Angry. 
            `,
                },
                {
                    role: "user",
                    content: userMessage || "Hello",
                },
            ],
        });

        let messages = JSON.parse(completion.choices[0].message.content);
        if (messages.messages) {
            messages = messages.messages;
        }
        for (let i = 0; i < messages.length; i++) {
            const message = messages[i];
            const fileName = `audios/message_${i}.mp3`;
            const textInput = message.text;

            // Generate audio file
            console.log(`Generating audio for message_${i}: ${textInput}`);
            await generateAudio(textInput, fileName);

            // Check if the audio file was created successfully
            try {
                await fs.promises.access(fileName);
                console.log(`Audio file created: ${fileName}`);
            } catch (error) {
                console.error(`Audio file not found: ${fileName}`, error);
                throw error;
            }

            // Generate lipsync
            await lipSyncMessage(i);

            message.audio = await audioFileToBase64(fileName);
            message.lipsync = await readJsonTranscript(`audios/message_${i}.json`);
        }

        res.send({ messages });
    } catch (error) {
        console.error("Error handling chat request:", error);
        if (error.response) {
            console.error('Error response data:', error.response.data);
        }
        res.status(500).send({ error: "Failed to handle chat request" });
    }
});

const readJsonTranscript = async (file) => {
    try {
        const data = await fs.promises.readFile(file, "utf8");
        return JSON.parse(data);
    } catch (error) {
        console.error("Error reading JSON transcript:", error);
        throw error;
    }
};

const audioFileToBase64 = async (file) => {
    try {
        const data = await fs.promises.readFile(file);
        return data.toString("base64");
    } catch (error) {
        console.error("Error converting audio file to base64:", error);
        throw error;
    }
};

app.listen(port, () => {
    console.log(`Bear listening on port ${port}`);
});
