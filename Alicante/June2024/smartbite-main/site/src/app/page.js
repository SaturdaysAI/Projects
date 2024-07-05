'use client'

import { Client } from "@gradio/client";
import { useState } from 'react';
import {v4 as uuidv4} from 'uuid';
import Card from '../components/Card/Card';
import DragAndDrop from '../components/DragAndDrop/DragAndDrop';
import './page.css';

const getClient = (() => {
  let model;
  return async () => {
    if (!model) {
      model = await Client.connect("sergiolms/smartbite");
    }

    return model;
  }
})();



export default function Home() {
  const [items, setItems] = useState([]);
  const [registeredDishes, setRegisteredDishes] = useState([]);
  
  const addItemToList = (image, data) => {
   setItems([...items, <Card
      key={uuidv4()}
      image={image}
      data={data}
    />]);
    setRegisteredDishes([...registeredDishes, data]);
  }

  const makePrediction = async (file) => {
      const blob = new Blob([file], { type: file.type });
      const formData = new FormData();
      formData.append('data',[{"path": blob}]);

      try {
        const client = await getClient()
        const result = await client.predict("/predict", { 
          img: blob, 
        });
        addItemToList(file, result.data[0]);
      } catch (error) {
        console.error('Error uploading file:', error);
      }
  }

  return (
    <div id="main">
      <h1><span className="text-gradient">SmartBite</span> <small>eat wiser</small></h1>
      <DragAndDrop onSubmit={makePrediction}/>
      {
        registeredDishes.length > 0 && <p className="calorie-intake">Calorías registradas hasta ahora: <span className="kcal">{
          registeredDishes.reduce((acc, it)=> {
            console.log(registeredDishes, it, acc)
            return acc + it.kcal
          }, 0)
        }</span></p>
      }
      <ul className="link-card-grid">
        {items}
      </ul>
    </div>
  );
}
