import React, { useState, useRef, useEffect } from 'react';
import './App.css';

const App = () => {
  const [currentView, setCurrentView] = useState('camera'); // 'camera', 'capture', 'results'
  const [capturedImage, setCapturedImage] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [randomDrink, setRandomDrink] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Initialize camera
  useEffect(() => {
    if (currentView === 'camera') {
      startCamera();
    }
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [currentView]);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { 
          facingMode: { ideal: 'environment' }, // Use back camera on mobile
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      setError('Camera access denied. Please allow camera permissions.');
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      const context = canvas.getContext('2d');
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0);
      
      const imageData = canvas.toDataURL('image/jpeg', 0.8);
      setCapturedImage(imageData);
      setCurrentView('capture');
      
      // Stop camera stream
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    }
  };

  const analyzeMenu = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('image_data', capturedImage);
      
      const response = await fetch(`${backendUrl}/api/analyze-menu`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setAnalysisData(data);
      setCurrentView('results');
    } catch (err) {
      setError(`Failed to analyze menu: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const getRandomDrink = async () => {
    if (!analysisData) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('analysis_id', analysisData.analysis_id);
      
      const response = await fetch(`${backendUrl}/api/random-drink`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setRandomDrink(data);
    } catch (err) {
      setError(`Failed to get random drink: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const resetApp = () => {
    setCurrentView('camera');
    setCapturedImage(null);
    setAnalysisData(null);
    setRandomDrink(null);
    setError(null);
  };

  const retakePhoto = () => {
    setCurrentView('camera');
    setCapturedImage(null);
    setError(null);
  };

  if (error) {
    return (
      <div className="app error-view">
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <h2>Oops!</h2>
          <p>{error}</p>
          <button onClick={resetApp} className="btn btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🍹 Menu Drink Selector</h1>
        <p>Snap a menu photo and get a random drink suggestion!</p>
      </header>

      {currentView === 'camera' && (
        <div className="camera-view">
          <div className="camera-container">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="camera-video"
            />
            <canvas ref={canvasRef} style={{ display: 'none' }} />
            <div className="camera-overlay">
              <div className="viewfinder">
                <div className="corner top-left"></div>
                <div className="corner top-right"></div>
                <div className="corner bottom-left"></div>
                <div className="corner bottom-right"></div>
              </div>
            </div>
          </div>
          <div className="camera-controls">
            <button onClick={capturePhoto} className="capture-btn">
              <div className="capture-inner"></div>
            </button>
          </div>
          <p className="camera-hint">Position the menu in the viewfinder and tap to capture</p>
        </div>
      )}

      {currentView === 'capture' && (
        <div className="capture-view">
          <div className="captured-image-container">
            <img src={capturedImage} alt="Captured menu" className="captured-image" />
          </div>
          <div className="capture-controls">
            <button onClick={retakePhoto} className="btn btn-secondary">
              📸 Retake Photo
            </button>
            <button 
              onClick={analyzeMenu} 
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing Menu...
                </>
              ) : (
                '🔍 Analyze Menu'
              )}
            </button>
          </div>
        </div>
      )}

      {currentView === 'results' && (
        <div className="results-view">
          <div className="results-container">
            <h2>Menu Analysis Results</h2>
            
            {analysisData && analysisData.drinks.length > 0 ? (
              <>
                <div className="drinks-found">
                  <h3>🍹 Found {analysisData.total_drinks} drinks:</h3>
                  <div className="drinks-list">
                    {analysisData.drinks.map((drink, index) => (
                      <div key={index} className="drink-item">
                        <h4>{drink.name}</h4>
                        {drink.description && <p className="drink-description">{drink.description}</p>}
                        {drink.price && <p className="drink-price">{drink.price}</p>}
                      </div>
                    ))}
                  </div>
                </div>

                {randomDrink && (
                  <div className="random-drink-result">
                    <h3>🎲 Your Random Selection:</h3>
                    <div className="selected-drink">
                      <h2>{randomDrink.selected_drink.name}</h2>
                      {randomDrink.selected_drink.description && (
                        <p className="drink-description">{randomDrink.selected_drink.description}</p>
                      )}
                      {randomDrink.selected_drink.price && (
                        <p className="drink-price">{randomDrink.selected_drink.price}</p>
                      )}
                    </div>
                    <p className="selection-message">{randomDrink.message}</p>
                  </div>
                )}

                <div className="results-controls">
                  <button 
                    onClick={getRandomDrink} 
                    className="btn btn-primary"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner"></span>
                        Selecting...
                      </>
                    ) : (
                      '🎲 Get Random Drink'
                    )}
                  </button>
                  <button onClick={resetApp} className="btn btn-secondary">
                    📸 Scan New Menu
                  </button>
                </div>
              </>
            ) : (
              <div className="no-drinks">
                <h3>😔 No drinks found in this menu</h3>
                <p>Try taking a clearer photo of the drinks section</p>
                <button onClick={resetApp} className="btn btn-primary">
                  📸 Try Again
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;