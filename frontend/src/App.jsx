import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import UploadZone from './components/UploadZone';
import ParamControls from './components/ParamControls';
import ResultsDashboard from './components/ResultsDashboard';

function App() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const [params, setParams] = useState({
    cut_speed: 10,
    vector_engrave_speed: 50,
    raster_engrave_speed: 100,
    transit_speed: 200,
    scan_gap: 0.1,
    ppi: 25.4,
    accel: 500,
    junction_delay: 0.05,
    burn_dwell: 0.1
  });

  const handleCalculate = async (svgFile, currentParams) => {
    setIsLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', svgFile);
      
      // Append all params to formdata
      Object.keys(currentParams).forEach(key => {
        formData.append(key, currentParams[key]);
      });

      const response = await fetch('http://127.0.0.1:8000/api/calculate', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Calculation failed');
      }

      const data = await response.json();
      setReport(data);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (file) {
      handleCalculate(file, params);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params, file]); // Re-calculate automatically when file or params change

  return (
    <div className="min-h-screen flex flex-col antialiased selection:bg-blue-500/30">
      <Header />
      
      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Input and Controls */}
        <div className="lg:col-span-7 flex flex-col space-y-8">
          <UploadZone 
            onFileSelected={setFile} 
            isLoading={isLoading} 
          />
          
          <div className="bg-gray-900 border border-gray-800 p-6 md:p-8 rounded-2xl shadow-xl">
            <ParamControls 
              params={params} 
              setParams={setParams} 
            />
          </div>
        </div>

        {/* Right Column: Results Dashboard */}
        <div className="lg:col-span-5 h-full">
          {error ? (
            <div className="bg-red-900/20 border border-red-500/50 text-red-400 p-6 rounded-2xl flex items-center justify-center">
              {error}
            </div>
          ) : (
            <ResultsDashboard report={report} />
          )}
        </div>
        
      </main>
    </div>
  );
}

export default App;
