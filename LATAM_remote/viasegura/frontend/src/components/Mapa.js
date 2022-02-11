import React, { Component } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import '../leaflet/react-leaflet.css';
import {MarkerIcon} from '../leaflet/react-leaflet-icon.js';

export default class Mapa extends Component {
    render() {
        return <MapContainer center={[-2.189352, -79.889095]} zoom={14} scrollWheelZoom={false}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <Marker position={[-2.189352, -79.889095]} icon={MarkerIcon}>
                <Popup>
                    A pretty CSS3 popup. <br /> Easily customizable.
                </Popup>
            </Marker>
        </MapContainer>;
    }
}
