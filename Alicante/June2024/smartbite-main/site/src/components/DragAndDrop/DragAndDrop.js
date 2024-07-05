'use client'
import React, { useState, useRef } from 'react';
import Image from "next/image";
import "./DragAndDrop.css";

const DragAndDrop = ({onSubmit}) => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState(null);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    const { files } = event.dataTransfer;
    if (files && files.length > 0) {
      const firstFile = files[0];
      if (validateFile(firstFile)) {
        setFile(firstFile);
        setPreview(URL.createObjectURL(firstFile));
        setError('');
      } else {
        setError('Please upload a valid JPG or PNG file.');
      }
    }
    setIsDragging(false);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(false);
  };

  const handleFileChange = (event) => {
    const { files } = event.target;
    if (files && files.length > 0) {
      const firstFile = files[0];
      if (validateFile(firstFile)) {
        setFile(firstFile);
        setPreview(URL.createObjectURL(firstFile));
        setError('');
      } else {
        setError('Please upload a valid JPG or PNG file.');
      }
    }
  };

  const handleClick = (event) => {
    event.stopPropagation();
    document.querySelector('#fileInput').click();
  };

  const validateFile = (file) => {
    const validTypes = ['image/jpeg', 'image/png'];
    return validTypes.includes(file.type);
  };

  const handleCameraClick = async (event) => {
    event.stopPropagation();
    setIsCameraOpen(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    } catch (error) {
      console.error('Error accessing camera:', error);
      setError('Could not access the camera.');
      setIsCameraOpen(false);
    }
  };

  const capturePhoto = () => {
    const context = canvasRef.current.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
    canvasRef.current.toBlob((blob) => {
      const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
      setFile(file);
      setPreview(URL.createObjectURL(file));
      setError('');
      stopCamera();
    });
  };

  const stopCamera = () => {
    const stream = videoRef.current.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    setIsCameraOpen(false);
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      await onSubmit(file);
    } else {
      console.error('No file selected');
    }
    setIsSubmitting(false);
  };

  const clearFile = () => {
    setFile(null);
    setPreview(null);
    setError('');
  };

  return (
    <div className="uploadInput">
      {isCameraOpen ? (
        <div className="cameraContainer">
          <video ref={videoRef} autoPlay style={{ width: '100%' }} />
          <div className="button-wrapper">
          <button className="custom-btn primary" onClick={capturePhoto}>Capturar</button>
          <button className="custom-btn secondary" onClick={stopCamera}>Cancelar</button>
          </div>
        </div>
      ) : (
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={handleClick}
          className={isDragging ? 'dragDrop dragging' : 'dragDrop'}
        >
          <input
            id="fileInput"
            type="file"
            accept="image/jpeg, image/png"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
          {preview ? (
            <div>
              <p>Archivo seleccionado: {file.name}</p>
              <Image src={preview} alt="Preview" width={300} height={300} style={{ objectFit: 'contain' }} />
            </div>
          ) : (
            <div>
              <p style={{ cursor: 'pointer' }} onClick={handleClick}>
                Arrastra una imagen <br/>
                - o - <br/>
                Pulsa para subir una desde tu equipo
              </p>
            </div>
          )}
         
        </div>
      )}
      <canvas ref={canvasRef} style={{ display: 'none' }} width="640" height="480"></canvas>
      {!isCameraOpen ? (
        <div className="button-wrapper">
          <button 
            className="icon-btn" 
            title="Sube una foto desde tu equipo"
            onClick={handleClick}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
          </button>
          <button 
            className="icon-btn" 
            title="Toma una foto desde la cámara"
            onClick={handleCameraClick}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2c-4.963 0-9 4.038-9 9c0 3.328 1.82 6.232 4.513 7.79l-2.067 1.378A1 1 0 0 0 6 22h12a1 1 0 0 0 .555-1.832l-2.067-1.378C19.18 17.232 21 14.328 21 11c0-4.962-4.037-9-9-9zm0 16c-3.859 0-7-3.141-7-7c0-3.86 3.141-7 7-7s7 3.14 7 7c0 3.859-3.141 7-7 7z"></path><path fill="currentColor" d="M12 6c-2.757 0-5 2.243-5 5s2.243 5 5 5s5-2.243 5-5s-2.243-5-5-5zm0 8c-1.654 0-3-1.346-3-3s1.346-3 3-3s3 1.346 3 3s-1.346 3-3 3z"></path></svg>
          </button>
        </div>
      ) : ''}
      <div className="button-wrapper">
        {isSubmitting ? 
          <button className="custom-btn primary" disabled>Procesando... </button>:
          <button className="custom-btn primary" onClick={handleSubmit}>Enviar</button>
        }
        {file && !isSubmitting && (
          <button className="custom-btn secondary" onClick={clearFile}>Borrar</button>
        )}
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default DragAndDrop;
