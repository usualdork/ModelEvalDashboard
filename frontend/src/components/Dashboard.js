// components/Dashboard.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard({ setIsAuthenticated }) {
  const [models, setModels] = useState([]);
  const [selectedModels, setSelectedModels] = useState([]);
  const [prompt, setPrompt] = useState('');
  const [responseLength, setResponseLength] = useState('medium');
  const [responses, setResponses] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await fetch('${process.env.REACT_APP_API_URL}/api/models', {
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch models');
      }
      
      const data = await response.json();
      setModels(data.models);
    } catch (err) {
      setError('Failed to load models');
    }
  };

  const handleLogout = async () => {
    try {
      await fetch('${process.env.REACT_APP_API_URL}/api/logout', {
        method: 'POST',
        credentials: 'include',
      });
      setIsAuthenticated(false);
      navigate('/login');
    } catch (err) {
      setError('Logout failed');
    }
  };

  const handleModelSelection = (index) => {
    setSelectedModels(prev => {
      if (prev.includes(index)) {
        return prev.filter(i => i !== index);
      }
      return [...prev, index];
    });
  };

  const handleSubmit = async () => {
    if (!prompt || selectedModels.length === 0) {
      setError('Please enter a prompt and select at least one model');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('${process.env.REACT_APP_API_URL}/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          prompt,
          models: selectedModels,
          responseLength,
        }),
      });

      if (!response.ok) {
        throw new Error('Generation failed');
      }

      const data = await response.json();
      setResponses(data.responses);
    } catch (err) {
      setError('Failed to generate responses');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">LLM Dashboard</h1>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Logout
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="col-span-1">
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-bold mb-4">Available Models</h2>
              <div className="space-y-2">
                {models.map((model, index) => (
                  <div key={index} className="flex items-center">
                    <input
                      type="checkbox"
                      id={`model-${index}`}
                      checked={selectedModels.includes(index)}
                      onChange={() => handleModelSelection(index)}
                      className="mr-2"
                    />
                    <label htmlFor={`model-${index}`}>Model {index + 1}</label>
                  </div>
                ))}
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700">
                  Response Length
                </label>
                <select
                  value={responseLength}
                  onChange={(e) => setResponseLength(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="short">Short</option>
                  <option value="medium">Medium</option>
                  <option value="detailed">Detailed</option>
                </select>
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700">
                  Prompt
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  rows="4"
                />
              </div>

              <button
                onClick={handleSubmit}
                disabled={isLoading}
                className="mt-4 w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
              >
                {isLoading ? 'Generating...' : 'Generate Responses'}
              </button>
            </div>
          </div>

          <div className="col-span-2">
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-bold mb-4">Responses</h2>
              <div className="space-y-4">
                {Object.entries(responses).map(([modelIndex, response]) => (
                  <div key={modelIndex} className="bg-gray-50 p-4 rounded">
                    <h3 className="font-bold mb-2">Model {parseInt(modelIndex) + 1}</h3>
                    <pre className="whitespace-pre-wrap">{response}</pre>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;